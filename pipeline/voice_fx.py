"""Original 'dark narrator' voices: blend free Kokoro voices, vary delivery per sentence,
then deepen + add grit with ffmpeg. NOT a clone of any real actor; an original voice with a similar mood.
Usage: python pipeline/voice_fx.py <preset> <text_file> <out.wav>"""
import sys, re, pathlib, subprocess, random, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRESETS = {
    # blend weights, base speed, pitch shift (semitones), ffmpeg colour chain
    "dark":   dict(mix={"am_onyx": .6, "am_fenrir": .4}, speed=.92, semis=-2.0,
                   fx="equalizer=f=120:t=q:w=1:g=4,equalizer=f=3000:t=q:w=1:g=2,acompressor=threshold=-18dB:ratio=3:attack=5:release=80"),
    "gravel": dict(mix={"am_fenrir": .5, "am_adam": .5}, speed=.9, semis=-3.0,
                   fx="equalizer=f=100:t=q:w=1:g=5,asoftclip=type=tanh:threshold=0.6,equalizer=f=2500:t=q:w=1:g=3,acompressor=threshold=-20dB:ratio=4:attack=3:release=60"),
    # sleep: same dark timbre, softened: slower, gentle pitch drop, no grit, warm low-mids, airy top rolled off
    "dark_soft": dict(mix={"am_onyx": .7, "am_fenrir": .3}, speed=.84, semis=-1.5,
                   fx="equalizer=f=200:t=q:w=1:g=2,highshelf=f=6000:g=-5,acompressor=threshold=-22dB:ratio=2:attack=20:release=200"),
    "george_plus": dict(mix={"bm_george": 1.0}, speed=.97, semis=-0.5,
                   fx="acompressor=threshold=-18dB:ratio=2.5:attack=5:release=80"),
    # owner voice notes 2026-11-27: slight (not full) British accent = 60/40 blend of a deep US and a UK voice on UK phonemes;
    # tiny pitch drop only (the old -2 st asetrate shift smeared consonants); tight=True swaps pauses for last-word emphasis
    "narrator": dict(mix={"bm_george": .4, "am_onyx": .6}, lang="en-gb", speed=.95, semis=-0.5, tight=True,
                   fx="equalizer=f=140:t=q:w=1:g=2.5,equalizer=f=3200:t=q:w=1:g=1.5,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=80"),
}

# espeak gives a mid-word open 'ɐ' (galaxy → ɡˈælɐksi, heard as "gal-AH-xy"); Kokoro's own G2P uses schwa there.
# Word-initial ɐ ("about") is fine and kept. Per-word overrides win.
OVERRIDES = {"galaxy": "ɡˈæləksi", "galaxies": "ɡˈæləksiz"}
def phonemes(k, text, lang):
    ph = k.tokenizer.phonemize(text, lang)   # whole sentence keeps connected-speech forms
    for w, fix in OVERRIDES.items():
        if re.search(rf"\b{w}\b", text, re.I):
            ph = ph.replace(k.tokenizer.phonemize(w, lang), fix.replace("æ", "a") if lang == "en-gb" else fix)
    return re.sub(r"(?<=[^\sˈˌ])ɐ", "ə", ph)

def tighten(a, sr, gap=0.07, thr_db=-38, min_pause=0.12, tail=0.30):
    """Owner note: instead of long pauses, lean on the last word before the break, then keep going.
    Finds pauses ≥ min_pause, shortens each to `gap`, and gives the ~300 ms before it +2.5 dB and an 8% stretch."""
    import tempfile
    hop = int(sr * 0.01); e = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2) + 1e-12) for i in range(0, len(a), hop)])
    quiet = 20 * np.log10(e / (e.max() + 1e-9)) < thr_db
    runs, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]: j += 1
            if (j - i) * 0.01 >= min_pause and i > 0 and j < len(quiet): runs.append((i * hop, j * hop))
            i = j
        else: i += 1
    out, pos = [], 0
    for s0, s1 in runs:
        seg = a[pos:s0]; t0 = max(0, len(seg) - int(tail * sr)); head, last = seg[:t0], seg[t0:]
        with tempfile.TemporaryDirectory() as d:
            fi, fo = f"{d}/i.wav", f"{d}/o.wav"; sf.write(fi, last, sr)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", fi, "-af", "atempo=0.92,volume=2.5dB", fo], check=True)
            last = sf.read(fo, dtype="float32")[0]
        n = min(len(head), int(0.01 * sr))   # 10 ms crossfade into the stretched tail
        if n: last[:n] = last[:n] * np.linspace(0, 1, n) + head[-n:] * np.linspace(1, 0, n); head = head[:-n]
        out += [head, last, np.zeros(int(gap * sr), np.float32)]; pos = s1
    out.append(a[pos:])
    return np.concatenate(out).astype(np.float32)


def render(preset, text, out, seed=3):
    p = PRESETS[preset]; rnd = random.Random(seed)
    global _K
    if "_K" not in globals() or _K is None:
        _K = Kokoro(str(ROOT / "models/kokoro-v1.0.onnx"), str(ROOT / "models/voices-v1.0.bin"))
    k = _K
    style = sum(k.get_voice_style(v) * w for v, w in p["mix"].items())
    lang = p.get("lang") or ("en-gb" if next(iter(p["mix"]))[0] == "b" else "en-us")
    parts, sr = [], 24000
    for sent in re.split(r"(?<=[.!?])\s+", text.strip()):
        if not sent: continue
        short = len(sent.split()) <= 4  # short punchy lines: slower, lower = emphasis
        a, sr = k.create(phonemes(k, sent, lang), voice=style, speed=p["speed"] * (0.88 if short else rnd.uniform(0.96, 1.05)),
                         lang=lang, is_phonemes=True)
        if p.get("tight"): a = tighten(a, sr)
        shift = p["semis"] + (-0.8 if short else rnd.uniform(-0.6, 0.6))  # per-sentence pitch movement
        parts.append((a, shift, 0.07 if p.get("tight") else (0.55 if short else 0.3)))
    tmp = pathlib.Path(out).with_suffix(".parts"); tmp.mkdir(exist_ok=True); files = []
    for i, (a, shift, pause) in enumerate(parts):
        raw = tmp / f"{i}.wav"; sf.write(raw, np.concatenate([a, np.zeros(int(sr * pause), a.dtype)]), sr)
        r = 2 ** (shift / 12)  # pitch shift keeping tempo: resample then correct tempo
        o = tmp / f"{i}_fx.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                        f"asetrate={int(sr * r)},aresample={sr},atempo={1 / r:.4f}", o], check=True)
        files.append(o)
    lst = tmp / "list.txt"; lst.write_text("".join(f"file '{f.resolve()}'\n" for f in files))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-af", p["fx"] + ",loudnorm=I=-16:TP=-1.5", out], check=True)
    return out

if __name__ == "__main__":
    render(sys.argv[1], pathlib.Path(sys.argv[2]).read_text(), sys.argv[3])
