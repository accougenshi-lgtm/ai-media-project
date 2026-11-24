"""Code-only sound design (owner's Audio Director brief, 2026-11-24). Every asset is synthesized here, so it's 100% original.
Builds a JSON manifest (stems: atmosphere / hard_sfx / micro_sfx, ducked under VO) from scene timings, then mixes it.
  python pipeline/sound.py <episode_work_dir> <in.mp4> <out.mp4> --key Bb --reveals 2,3 [--pops 3]
Scene times come from <work_dir>/captions.srt (one cue per scene, written by engine.build)."""
import sys, json, re, argparse, subprocess, pathlib, numpy as np, soundfile as sf
SR = 48000
KEYS = {"C": 65.41, "D": 73.42, "Eb": 77.78, "E": 82.41, "F": 87.31, "G": 98.0, "A": 55.0, "Bb": 58.27, "B": 61.74}
rng = np.random.default_rng(7)
def t(n): return np.arange(n) / SR
def env(n, a, r):  # attack/release envelope in samples
    e = np.ones(n); a, r = max(1, a), max(1, r); e[:a] = np.linspace(0, 1, a); e[-r:] *= np.linspace(1, 0, r); return e
def lp(x, k):  # cheap one-pole low-pass, k in 0..1 (smaller = darker)
    y = np.empty_like(x); acc = 0.0; kk = np.broadcast_to(np.asarray(k, float), x.shape)
    for i, v in enumerate(x): acc += kk[i] * (v - acc); y[i] = acc
    return y

def bed(dur, root):  # atmospheric drone: root + fifth + octave, slow LFOs, brown noise, low-passed (key-locked)
    n = int(dur * SR); tt = t(n)
    x = sum(a * np.sin(2 * np.pi * f * tt) * (0.6 + 0.4 * np.sin(2 * np.pi * tt / p + ph))
            for f, a, p, ph in [(root, .5, 17, 0), (root * 1.5, .3, 23, 1), (root * 2, .25, 31, 2)])
    brown = np.cumsum(rng.normal(0, 1, n)); brown -= np.convolve(brown, np.ones(4800) / 4800, "same")
    return (x + 0.004 * brown) * env(n, SR, SR)
def whoosh(ms=300):  # band-limited noise swell, peak centred
    n = int(ms * SR / 1000); w = rng.normal(0, 1, n) * np.hanning(n) ** 1.5
    return lp(w, 0.25) - lp(w, 0.02)
def impact():  # layered: sub-drop 65→28 Hz + mid thud + airy tail
    n = int(0.9 * SR); tt = t(n); f = 65 * (28 / 65) ** (tt / 0.25).clip(0, 1)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 5)
    thud = lp(rng.normal(0, 1, n), 0.05) * np.exp(-tt * 18) * 3
    air = (rng.normal(0, 1, n) - lp(rng.normal(0, 1, n), 0.3)) * np.exp(-tt * 9) * 0.25
    return sub + thud + air
def riser(ms, root):  # rising filtered noise + root tone sweep (key-locked), ends hard
    n = int(ms * SR / 1000); tt = t(n); g = (tt / tt[-1]) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(root * 4 * (1 + g)) / SR) * g * 0.4
    return (lp(rng.normal(0, 1, n), 0.08 + 0.5 * g) * g + tone)
def pop(semi=0):  # micro text pop: 880 Hz × pitch variation, 60 ms exp decay
    n = int(0.06 * SR); tt = t(n); return np.sin(2 * np.pi * 880 * 2 ** (semi / 12) * tt) * np.exp(-tt * 70)

def scenes(work):
    srt = (pathlib.Path(work) / "captions.srt").read_text()
    ts = re.findall(r"(\d\d):(\d\d):(\d\d),(\d{3}) --> (\d\d):(\d\d):(\d\d),(\d{3})", srt)
    to = lambda h, m, s, ms: int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    return [(to(*a[:4]), to(*a[4:])) for a in ts]

def manifest(sc, dur, key, reveals, pops):
    root = KEYS[key]; ev = [dict(id="evt_bed", stem="atmosphere", synth=f"drone {key} root+5th+oct, brown noise", start_ms=0,
                                 end_ms=int(dur * 1000), gain_db=-30.0, fade_in_ms=1000, fade_out_ms=1200, ducking_enabled=True)]
    last_impact = -99
    for i, (a, b) in enumerate(sc):
        if i == 0: continue
        ms = int(a * 1000)
        if i in reveals and a - last_impact >= 3.5:
            ev.append(dict(id=f"evt_riser_{i}", stem="hard_sfx", synth=f"riser {key}", start_ms=ms - 1200, end_ms=ms - 50,
                           gain_db=-16.0, notes="cut dead ~50 ms before impact (silence gap rule)"))
            ev.append(dict(id=f"evt_impact_{i}", stem="hard_sfx", synth="sub-drop+thud+air", start_ms=ms, transient_sync_ms=ms, gain_db=-9.0))
            last_impact = a
        else:
            ev.append(dict(id=f"evt_whoosh_{i}", stem="hard_sfx", synth="whoosh 300ms", start_ms=ms - 150, transient_sync_ms=ms, gain_db=-17.0))
    for j, i in enumerate(pops):
        a = sc[i][0] if i < len(sc) else 0
        ev.append(dict(id=f"evt_pop_{i}", stem="micro_sfx", synth="pop 880Hz", start_ms=int(a * 1000) + 350, gain_db=-22.0 + rng.uniform(-2, 2),
                       pitch_shift_semitones=round(float(rng.uniform(-3, 3)), 1), pan=round(float(rng.uniform(-.3, .3)), 2)))
    return dict(video_profile=dict(pacing="Fast" if dur / max(len(sc), 1) < 2.5 else "Medium" if dur / max(len(sc), 1) <= 5 else "Slow",
                                   tone="Analytical/Documentary, awe", target_bpm=None, musical_key=f"{key} (drone-locked)"), audio_events=ev)

def render(man, vo, dur, key):
    n = int(dur * SR) + SR; fx = np.zeros(n); amb = np.zeros(n); root = KEYS[key]
    for e in man["audio_events"]:
        s = int(e["start_ms"] * SR / 1000); g = 10 ** (e["gain_db"] / 20)
        if e["stem"] == "atmosphere": x = bed(e["end_ms"] / 1000, root); amb[s:s + len(x)] += x / np.abs(x).max() * g; continue
        syn = e["synth"]
        x = whoosh() if syn.startswith("whoosh") else impact() if syn.startswith("sub") else \
            riser(e["end_ms"] - e["start_ms"], root) if syn.startswith("riser") else pop(e.get("pitch_shift_semitones", 0))
        x = x / (np.abs(x).max() + 1e-9) * g; s = max(s, 0); fx[s:s + len(x)] += x[:n - s]
    v = np.zeros(n); v[:len(vo)] = vo
    envl = np.convolve(np.abs(v), np.ones(int(.02 * SR)) / int(.02 * SR), "same")          # sidechain: duck bed ~8 dB under VO
    duck = np.where(envl > 0.02, 10 ** (-8 / 20), 1.0); duck = lp(duck, 1 / (0.3 * SR))     # ~300 ms release
    return v + amb * duck + fx

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("work"); ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--key", default="D"); ap.add_argument("--reveals", default=""); ap.add_argument("--pops", default="")
    a = ap.parse_args(); work = pathlib.Path(a.work)
    vo = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", a.inp, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                      capture_output=True).stdout, np.float32).astype(np.float64)
    dur = len(vo) / SR; sc = scenes(work)
    rev = [int(x) for x in a.reveals.split(",") if x]; pops = [int(x) for x in a.pops.split(",") if x]
    man = manifest(sc, dur, a.key, rev, pops); (work / "audio_manifest.json").write_text(json.dumps(man, indent=1))
    mix = render(man, vo, dur, a.key); sf.write(work / "mix.wav", (mix / max(1.0, np.abs(mix).max())).astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.inp, "-i", str(work / "mix.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "highpass=f=30,loudnorm=I=-14:TP=-1.0", "-c:a", "aac", "-b:a", "192k", "-shortest", a.out], check=True)
    print(json.dumps(dict(out=a.out, events=len(man["audio_events"]), profile=man["video_profile"])))
