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
    "george_plus": dict(mix={"bm_george": 1.0}, speed=.97, semis=-0.5,
                   fx="acompressor=threshold=-18dB:ratio=2.5:attack=5:release=80"),
}

def render(preset, text, out, seed=3):
    p = PRESETS[preset]; rnd = random.Random(seed)
    k = Kokoro(str(ROOT / "models/kokoro-v1.0.onnx"), str(ROOT / "models/voices-v1.0.bin"))
    style = sum(k.get_voice_style(v) * w for v, w in p["mix"].items())
    lang = "en-gb" if next(iter(p["mix"]))[0] == "b" else "en-us"
    parts, sr = [], 24000
    for sent in re.split(r"(?<=[.!?])\s+", text.strip()):
        if not sent: continue
        short = len(sent.split()) <= 4  # short punchy lines: slower, lower = emphasis
        a, sr = k.create(sent, voice=style, speed=p["speed"] * (0.88 if short else rnd.uniform(0.96, 1.05)), lang=lang)
        shift = p["semis"] + (-0.8 if short else rnd.uniform(-0.6, 0.6))  # per-sentence pitch movement
        parts.append((a, shift, 0.55 if short else 0.3))
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
