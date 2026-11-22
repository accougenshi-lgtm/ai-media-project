"""Tiny free video engine: PIL draws each frame, Kokoro narrates each scene, ffmpeg encodes.
Scene = dict(text=narration, draw=fn(img, draw, t, sec)) where t is 0..1 progress through the scene.
Captions are word-chunked and timed by character share of the scene's audio."""
import math, random, subprocess, pathlib, json, wave
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H, FPS = 1080, 1920, 30
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
ACCENT, WHITE, DIM, BG = (255, 186, 73), (245, 245, 240), (150, 160, 175), (8, 10, 20)
_fonts = {}
def font(size, bold=True):
    k = (size, bold)
    if k not in _fonts: _fonts[k] = ImageFont.truetype(FONT_B if bold else FONT_R, size)
    return _fonts[k]

# ---------- reusable drawing helpers ----------
_rng = random.Random(7)
STARS = [(_rng.randrange(W), _rng.randrange(H), _rng.random()) for _ in range(380)]
def starfield(img, sec, drift=6):
    d = ImageDraw.Draw(img)
    for x, y, b in STARS:
        tw = 0.6 + 0.4 * math.sin(sec * 2 + x)
        c = int(90 + 140 * b * tw); r = 1 if b < .8 else 2
        yy = (y + sec * drift * b) % H
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=(c, c, min(255, c + 20)))

def glow_disc(img, cx, cy, r, inner, outer, glow=None):
    if glow:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.ellipse([cx - r * 1.25, cy - r * 1.25, cx + r * 1.25, cy + r * 1.25], fill=glow + (90,))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(r * 0.25 + 4)))
    disc = Image.new("RGBA", img.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(disc)
    steps = 24
    for i in range(steps):  # radial gradient, light from upper-left
        f = i / steps; rr = r * (1 - f)
        c = tuple(int(outer[j] + (inner[j] - outer[j]) * f) for j in range(3))
        ox, oy = -r * 0.25 * f, -r * 0.25 * f
        dd.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr], fill=c + (255,))
    mask = Image.new("L", img.size, 0); ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.paste(disc, (0, 0), mask)

def earth(img, cx, cy, r):
    glow_disc(img, cx, cy, r, (90, 170, 255), (10, 40, 110), glow=(60, 130, 255))
    d = ImageDraw.Draw(img)
    for ax, ay, ar in [(-.3, -.2, .28), (.25, .15, .22), (-.05, .4, .18), (.35, -.35, .12)]:
        d.ellipse([cx + ax * r - ar * r, cy + ay * r - ar * r * .7, cx + ax * r + ar * r, cy + ay * r + ar * r * .7], fill=(60, 140, 90))

def moon(img, cx, cy, r):
    glow_disc(img, cx, cy, r, (225, 225, 220), (95, 95, 100), glow=(200, 200, 190))
    d = ImageDraw.Draw(img)
    for ax, ay, ar in [(-.3, -.25, .16), (.2, .1, .22), (-.1, .35, .1), (.35, -.3, .08), (-.4, .15, .07)]:
        d.ellipse([cx + ax * r - ar * r, cy + ay * r - ar * r, cx + ax * r + ar * r, cy + ay * r + ar * r], fill=(130, 130, 135))

def text_c(img, s, y, size, fill=WHITE, bold=True, alpha=1.0, cx=None):
    if alpha <= 0: return
    f = font(size, bold); layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    w = d.textlength(s, font=f)
    d.text((((cx if cx is not None else W / 2)) - w / 2, y), s, font=f, fill=fill + (int(255 * alpha),), stroke_width=max(2, size // 18), stroke_fill=(0, 0, 0, int(220 * alpha)))
    img.alpha_composite(layer)

def ease(t): return t * t * (3 - 2 * t)
def seg(t, a, b): return 0.0 if t <= a else 1.0 if t >= b else ease((t - a) / (b - a))

# ---------- captions ----------
def chunks(text, n=3):
    w = text.split(); return [" ".join(w[i:i + n]) for i in range(0, len(w), n)]

def caption(img, text, t):
    cs = chunks(text); total = sum(len(c) + 1 for c in cs); acc = 0
    for c in cs:
        share = (len(c) + 1) / total
        if acc <= t < acc + share or c is cs[-1] and t >= acc:
            text_c(img, c.upper(), int(H * 0.74), 64); return
        acc += share

# ---------- build ----------
def build(scenes, out_path, voice="dark", speed=1.0, music=None):
    from voice_fx import PRESETS, render as render_fx
    from kokoro_onnx import Kokoro
    k = Kokoro(str(ROOT / "models/kokoro-v1.0.onnx"), str(ROOT / "models/voices-v1.0.bin"))
    work = pathlib.Path(out_path).with_suffix(""); work.mkdir(parents=True, exist_ok=True)
    audio, durs, sr, srt, clock = [], [], 24000, [], 0.0
    for i, s in enumerate(scenes):
        if voice in PRESETS:  # processed original narrator voices (voice_fx.py)
            vf = work / f"scene{i}.wav"; render_fx(voice, s["text"], str(vf), seed=i)
            a, sr = sf.read(vf, dtype="float32")
            if a.ndim > 1: a = a.mean(axis=1)
        else:
            a, sr = k.create(s["text"], voice=voice, speed=speed, lang="en-gb" if voice[0] == "b" else "en-us")
        pad = np.zeros(int(sr * s.get("pad", 0.45)), dtype=a.dtype)
        a = np.concatenate([np.zeros(int(sr * 0.15), dtype=a.dtype), a, pad]); audio.append(a)
        d = len(a) / sr; durs.append(d)
        srt.append((clock, clock + d, s["text"])); clock += d
    sf.write(work / "narration.wav", np.concatenate(audio), sr)
    # encode frames
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", str(work / "narration.wav"), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", str(out_path)], stdin=subprocess.PIPE)
    sec = 0.0
    for s, d in zip(scenes, durs):
        n = max(1, int(d * FPS))
        for f in range(n):
            t = f / n; img = Image.new("RGBA", (W, H), BG + (255,))
            s["draw"](img, t, sec); caption(img, s["text"], t)
            ff.stdin.write(img.convert("RGB").tobytes()); sec += 1 / FPS
    ff.stdin.close(); ff.wait()
    with open(work / "captions.srt", "w") as fh:  # upload this to YouTube as the caption track
        for i, (a, b, txt) in enumerate(srt, 1):
            ts = lambda x: f"{int(x//3600):02}:{int(x%3600//60):02}:{int(x%60):02},{int(x%1*1000):03}"
            fh.write(f"{i}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
    return out_path, sum(durs)
