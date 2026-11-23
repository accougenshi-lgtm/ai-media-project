"""Long-form 'fall asleep to' engine (16:9, 1080p). Per chapter: soft narration (voice_fx), one procedurally
painted still (numpy), slow pan via ffmpeg crop, gentle title fade. Then concat + original ambient pad.
Outputs: video mp4, captions .srt, chapters.txt (YouTube description timestamps)."""
import math, re, pathlib, subprocess, random
import numpy as np, soundfile as sf
from PIL import Image, ImageFilter, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OW, OH, CW, CH, FPS = 2400, 1350, 1920, 1080, 24
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

# ---------------- procedural painting ----------------
def smooth_noise(h, w, scale, rng):
    small = rng.random((max(2, h // scale), max(2, w // scale))).astype(np.float32)
    im = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(im.filter(ImageFilter.GaussianBlur(scale / 3)), np.float32) / 255

def starfield(h, w, rng, n=2600):
    img = np.zeros((h, w, 3), np.float32)
    ys, xs = rng.integers(0, h, n), rng.integers(0, w, n)
    b = 0.25 + 0.75 * rng.random(n) ** 2.5
    tint = np.stack([0.9 + 0.1 * rng.random(n), 0.92 + 0.08 * rng.random(n), np.ones(n)], 1)
    img[ys, xs] = (b[:, None] * tint)
    glow = np.asarray(Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    neb = smooth_noise(h, w, 260, rng)[..., None] * np.array([0.05, 0.06, 0.11])  # faint blue haze
    return np.clip(img * 1.2 + glow * 2.2 + neb * 0.45, 0, 1)

def moon_disc(size, rng, phase=0.0, earthshine=0.035, red=False):
    """phase: angle (rad) of sunlight from the viewer direction; 0 = full, pi*0.8 = thin crescent."""
    y, x = np.mgrid[-1:1:size * 1j, -1:1:size * 1j].astype(np.float32)
    r2 = x * x + y * y; inside = r2 < 1; z = np.sqrt(np.clip(1 - r2, 0, 1))
    alb = 0.62 + 0.18 * smooth_noise(size, size, max(4, size // 60), rng) + 0.08 * smooth_noise(size, size, max(2, size // 200), rng)
    maria = smooth_noise(size, size, max(8, size // 6), rng)
    alb -= np.clip((maria - 0.47) * 3.0, 0, 1) * 0.36 * (0.55 + 0.45 * np.clip((0.5 - y) / 0.8, 0, 1))
    for _ in range(int(size * 0.35)):  # craters
        cx, cy = rng.uniform(-1, 1, 2); cr = rng.uniform(0.006, 0.06) ** 1.0 * (1.6 if rng.random() < 0.04 else 1)
        if cx * cx + cy * cy > 0.97: continue
        x0, x1 = int((cx - cr * 1.4 + 1) / 2 * size), int((cx + cr * 1.4 + 1) / 2 * size) + 1
        y0, y1 = int((cy - cr * 1.4 + 1) / 2 * size), int((cy + cr * 1.4 + 1) / 2 * size) + 1
        x0, y0 = max(x0, 0), max(y0, 0)
        d = np.sqrt((x[y0:y1, x0:x1] - cx) ** 2 + (y[y0:y1, x0:x1] - cy) ** 2) / cr
        alb[y0:y1, x0:x1] += np.where(d < 1, -0.07 * (1 - d), np.where(d < 1.35, 0.06 * (1.35 - d) / 0.35, 0))
    L = np.array([math.sin(phase), -0.15 * math.sin(phase), math.cos(phase)], np.float32); L /= np.linalg.norm(L)
    lit = np.clip(x * L[0] + y * L[1] + z * L[2], 0, 1) ** 0.8
    shade = lit + earthshine + 0.12 * (1 - r2) * (lit > 0)
    col = np.array([1.0, 0.97, 0.92]) if not red else np.array([0.75, 0.28, 0.12])
    rgb = np.clip(alb[..., None] * shade[..., None] * col, 0, 1)
    edge = np.clip((1 - np.sqrt(r2)) * size / 2.5, 0, 1)  # antialias
    return rgb, (inside * edge).astype(np.float32)

def earth_disc(size, rng):
    y, x = np.mgrid[-1:1:size * 1j, -1:1:size * 1j].astype(np.float32)
    r2 = x * x + y * y; inside = r2 < 1; z = np.sqrt(np.clip(1 - r2, 0, 1))
    land = smooth_noise(size, size, max(8, size // 7), rng) > 0.56
    cloud = np.clip((smooth_noise(size, size, max(4, size // 25), rng) - 0.5) * 3, 0, 1)
    base = np.where(land[..., None], np.array([0.22, 0.38, 0.2]), np.array([0.05, 0.18, 0.45]))
    base = base * (1 - cloud[..., None]) + cloud[..., None] * 0.95
    L = np.array([-0.6, -0.3, 0.75]); L /= np.linalg.norm(L)
    lit = np.clip(x * L[0] + y * L[1] + z * L[2], 0, 1)
    rgb = np.clip(base * (lit[..., None] * 1.1 + 0.02), 0, 1)
    edge = np.clip((1 - np.sqrt(r2)) * size / 2.5, 0, 1)
    return rgb, (inside * edge).astype(np.float32)

def paste(bg, rgb, a, cx, cy, glow=None):
    s = rgb.shape[0]; H, W, _ = bg.shape; x0, y0 = int(cx - s / 2), int(cy - s / 2)
    bx0, by0, bx1, by1 = max(x0, 0), max(y0, 0), min(x0 + s, W), min(y0 + s, H)  # clip to canvas
    sx0, sy0 = bx0 - x0, by0 - y0; sx1, sy1 = sx0 + (bx1 - bx0), sy0 + (by1 - by0)
    if glow is not None:  # soft halo on a padded canvas so it never shows a square edge
        m = int(s * 0.5); big = np.zeros((s + 2 * m, s + 2 * m), np.float32); big[m:m + s, m:m + s] = a
        g = np.asarray(Image.fromarray((big * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(s * 0.09)), np.float32) / 255
        gx0, gy0 = x0 - m, y0 - m; cx0, cy0 = max(gx0, 0), max(gy0, 0)
        cx1, cy1 = min(gx0 + g.shape[1], W), min(gy0 + g.shape[0], H)
        gg = g[cy0 - gy0:cy1 - gy0, cx0 - gx0:cx1 - gx0][..., None] * 0.45
        bg[cy0:cy1, cx0:cx1] = np.clip(bg[cy0:cy1, cx0:cx1] + gg * np.array(glow), 0, 1)
    rgb, a = rgb[sy0:sy1, sx0:sx1], a[sy0:sy1, sx0:sx1]
    sl = bg[by0:by1, bx0:bx1]
    bg[by0:by1, bx0:bx1] = sl * (1 - a[..., None]) + rgb * a[..., None]

def corona(bg, cx, cy, r):
    h, w, _ = bg.shape; y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / r
    ang = np.arctan2(y - cy, x - cx)
    streak = 0.6 + 0.4 * np.sin(ang * 9) * np.sin(ang * 4 + 1)
    c = np.clip(np.exp(-(d - 1) * 2.2) * streak, 0, 1) * (d > 1)
    bg += c[..., None] * np.array([0.95, 0.93, 0.85]); np.clip(bg, 0, 1, out=bg)


def sun_disc(size, rng):
    y, x = np.mgrid[-1:1:size * 1j, -1:1:size * 1j].astype(np.float32)
    r2 = x * x + y * y; inside = r2 < 1; mu = np.sqrt(np.clip(1 - r2, 0, 1))
    gran = 0.85 + 0.15 * smooth_noise(size, size, max(3, size // 120), rng)
    limb = 0.35 + 0.65 * mu ** 0.6  # limb darkening
    rgb = np.stack([np.ones_like(mu), 0.78 + 0.15 * mu, 0.35 + 0.35 * mu], -1) * (limb * gran)[..., None]
    edge = np.clip((1 - np.sqrt(r2)) * size / 2.5, 0, 1)
    return np.clip(rgb, 0, 1), (inside * edge).astype(np.float32)

def banded_disc(size, rng, palette, freq=9, phase=0.5, storm=None):
    y, x = np.mgrid[-1:1:size * 1j, -1:1:size * 1j].astype(np.float32)
    r2 = x * x + y * y; inside = r2 < 1; z = np.sqrt(np.clip(1 - r2, 0, 1))
    turb = smooth_noise(size, size, max(4, size // 30), rng)
    band = 0.5 + 0.5 * np.sin(y * freq * np.pi + turb * 3.0)
    a, b = np.array(palette[0]), np.array(palette[1])
    col = a * band[..., None] + b * (1 - band[..., None])
    if storm:
        sx, sy, sr = storm; d = ((x - sx) / (sr * 1.6)) ** 2 + ((y - sy) / sr) ** 2
        col = np.where((d < 1)[..., None], col * 0.5 + np.array([0.75, 0.35, 0.22]) * 0.5, col)
    L = np.array([-math.sin(phase), -0.2, math.cos(phase)]); L /= np.linalg.norm(L)
    lit = np.clip(x * L[0] + y * L[1] + z * L[2], 0, 1) ** 0.7 + 0.02
    edge = np.clip((1 - np.sqrt(r2)) * size / 2.5, 0, 1)
    return np.clip(col * lit[..., None], 0, 1), (inside * edge).astype(np.float32)

def rings(bg, cx, cy, R, front, tilt=0.28):
    h, w, _ = bg.shape; y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = (x - cx) / R, (y - cy) / (R * tilt); d = np.sqrt(dx * dx + dy * dy)
    ring = ((d > 1.25) & (d < 2.25)).astype(np.float32) * (0.55 + 0.45 * np.sin(d * 40) ** 2) * (1 - ((d > 1.85) & (d < 1.93)))
    half = (y > cy) if front else (y <= cy)
    a = ring * half * 0.85
    bg[:] = bg * (1 - a[..., None]) + a[..., None] * np.array([0.86, 0.8, 0.66])

def nebula_bg(h, w, rng):
    bg = starfield(h, w, rng, n=3200)
    wisp = np.zeros((h, w), np.float32)
    for sc, wt in [(420, 0.55), (160, 0.3), (60, 0.15)]:  # multi-scale fbm, soft wisps
        wisp += smooth_noise(h, w, sc, rng) * wt
    wisp = np.clip((wisp - 0.38) * 2.4, 0, 1) ** 1.6
    tint = smooth_noise(h, w, 500, rng)[..., None]
    col = np.array([0.55, 0.18, 0.42]) * tint + np.array([0.12, 0.32, 0.58]) * (1 - tint)
    glow = np.asarray(Image.fromarray((wisp * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14)), np.float32)[..., None] / 255
    return np.clip(bg + glow * col * 1.25, 0, 1)

def galaxy(bg, cx, cy, R, rng, tilt=0.45, arms=2, wind=3.2):
    h, w, _ = bg.shape; y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = (x - cx) / R, (y - cy) / (R * tilt); r = np.sqrt(dx * dx + dy * dy) + 1e-3; th = np.arctan2(dy, dx)
    spiral = (0.5 + 0.5 * np.cos(arms * (th - wind * np.log(r)))) ** 3
    noise = smooth_noise(h, w, 18, rng)
    disk = np.exp(-r / 0.38) * (0.35 + 0.9 * spiral * (0.6 + 0.8 * noise)) * (r < 1.6)
    core = np.exp(-(r / 0.09) ** 2) * 1.4
    bg += disk[..., None] * np.array([0.55, 0.65, 1.0]) * 0.9 + core[..., None] * np.array([1.0, 0.9, 0.7])
    np.clip(bg, 0, 1, out=bg)

def deepfield(h, w, rng, n=1100):
    bg = starfield(h, w, rng, n=700) * 0.5
    im = Image.fromarray((bg * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    for _ in range(n):
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        s = 1.2 + rng.pareto(2.2) * 2.5; s = min(s, 26); e = rng.uniform(0.25, 1); ang = rng.uniform(0, 3.14)
        c = [(255, 215, 165), (190, 205, 255), (255, 175, 130), (235, 235, 225)][rng.integers(0, 4)]
        k = rng.uniform(0.15, 0.6) * (1.3 if s > 8 else 1)
        dx, dy = s * math.cos(ang), s * math.sin(ang)
        d.ellipse([cx - abs(dx) - s * e * .5, cy - abs(dy) - s * e * .5, cx + abs(dx) + s * e * .5, cy + abs(dy) + s * e * .5],
                  fill=tuple(int(min(255, v * k)) for v in c))
    im = im.filter(ImageFilter.GaussianBlur(2.2))
    return np.asarray(im, np.float32) / 255

def paint(kind, seed):
    rng = np.random.default_rng(seed); bg = starfield(OH, OW, rng)
    if kind == "full":      m, a = moon_disc(820, rng, 0.05); paste(bg, m, a, OW * .5, OH * .5, glow=(.9, .9, .85))
    elif kind == "gibbous": m, a = moon_disc(860, rng, 0.9); paste(bg, m, a, OW * .55, OH * .5, glow=(.6, .6, .55))
    elif kind == "crescent":m, a = moon_disc(760, rng, 2.45, earthshine=0.06); paste(bg, m, a, OW * .5, OH * .5, glow=(.3, .3, .3))
    elif kind == "earth_moon":
        e, ea = earth_disc(700, rng); paste(bg, e, ea, OW * .33, OH * .55, glow=(.3, .5, 1))
        m, a = moon_disc(200, rng, 0.7); paste(bg, m, a, OW * .78, OH * .38, glow=(.5, .5, .5))
    elif kind == "closeup": m, a = moon_disc(2300, rng, 1.25); paste(bg, m, a, OW * .5, OH * 1.25)
    elif kind == "eclipse":
        corona(bg, OW * .5, OH * .5, 300); m, a = moon_disc(600, rng, 3.1, earthshine=0.0); paste(bg, m * 0.02, a, OW * .5, OH * .5)
    elif kind == "blood":   m, a = moon_disc(800, rng, 0.0, red=True); paste(bg, m * 0.75, a, OW * .5, OH * .5, glow=(.5, .15, .05))
    elif kind == "horizon":
        m, a = moon_disc(380, rng, 0.2); paste(bg, m, a, OW * .66, OH * .3, glow=(.8, .8, .75))
        y, x = np.mgrid[0:OH, 0:OW]; hills = OH * .78 + 60 * np.sin(x / 260) + 30 * np.sin(x / 97 + 2)
        bg[y > hills] = bg[y > hills] * 0.05 + np.array([0.01, 0.012, 0.02])
    elif kind == "sun":     m, a = sun_disc(760, rng); paste(bg, m, a, OW * .5, OH * .5, glow=(1, .75, .35))
    elif kind == "mars":    m, a = banded_disc(640, rng, [(0.78, 0.38, 0.2), (0.62, 0.28, 0.16)], freq=3); paste(bg, m, a, OW * .55, OH * .5, glow=(.6, .3, .15))
    elif kind == "jupiter": m, a = banded_disc(820, rng, [(0.86, 0.76, 0.62), (0.66, 0.48, 0.34)], freq=11, storm=(0.25, 0.35, 0.12)); paste(bg, m, a, OW * .5, OH * .5, glow=(.5, .4, .3))
    elif kind == "saturn":
        cx, cy, R = OW * .5, OH * .5, 280
        rings(bg, cx, cy, R, front=False); m, a = banded_disc(2 * R, rng, [(0.9, 0.82, 0.6), (0.78, 0.68, 0.48)], freq=8)
        paste(bg, m, a, cx, cy, glow=(.4, .35, .25)); rings(bg, cx, cy, R, front=True)
    elif kind == "venus":   m, a = banded_disc(760, rng, [(0.93, 0.86, 0.64), (0.84, 0.73, 0.5)], freq=3, phase=0.6); paste(bg, m, a, OW * .5, OH * .5, glow=(.6, .5, .3))
    elif kind == "icegiant": m, a = banded_disc(760, rng, [(0.55, 0.78, 0.86), (0.36, 0.6, 0.78)], freq=5, phase=0.7); paste(bg, m, a, OW * .5, OH * .5, glow=(.3, .55, .75))
    elif kind == "nebula":  bg = nebula_bg(OH, OW, rng)
    elif kind == "galaxy":  galaxy(bg, OW * .5, OH * .5, 900, rng)
    elif kind == "deepfield": bg = deepfield(OH, OW, rng)
    return Image.fromarray((np.clip(bg, 0, 1) * 255).astype(np.uint8))

# ---------------- audio ----------------
PARA_PAUSE = 1.6  # seconds between paragraphs; episodes may raise it
def narrate_chapter(text, out, preset="dark_soft", para_pause=None):
    para_pause = PARA_PAUSE if para_pause is None else para_pause
    from voice_fx import render
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, sr, times = [], 24000, []
    t = 0.0
    for i, p in enumerate(paras):
        tmp = pathlib.Path(out).with_name(f"_p{i}.wav"); render(preset, p, str(tmp), seed=i)
        a, sr = sf.read(tmp, dtype="float32"); a = a if a.ndim == 1 else a.mean(1); tmp.unlink()
        times.append((t, t + len(a) / sr, p)); t += len(a) / sr + para_pause
        chunks += [a, np.zeros(int(sr * para_pause), np.float32)]
    sf.write(out, np.concatenate(chunks), sr)
    return t, times

def ambient_pad(out, dur):
    # original drone: soft A-minor-ish chord with slow independent swells, plus very quiet brown noise
    expr = ("0.05*sin(2*PI*110*t)*(0.6+0.4*sin(2*PI*t/23))+0.04*sin(2*PI*164.81*t)*(0.6+0.4*sin(2*PI*t/31+1))"
            "+0.035*sin(2*PI*220*t)*(0.5+0.5*sin(2*PI*t/41+2))+0.025*sin(2*PI*261.63*t)*(0.5+0.5*sin(2*PI*t/53+3))")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"aevalsrc='{expr}':s=24000:d={dur:.1f}",
                    "-f", "lavfi", "-i", f"anoisesrc=c=brown:a=0.02:d={dur:.1f}:r=24000",
                    "-filter_complex", "[0][1]amix=inputs=2:normalize=0,lowpass=f=1800,aecho=0.6:0.5:900:0.25", out], check=True)

# ---------------- build ----------------
def ts(x): return f"{int(x//3600):02}:{int(x%3600//60):02}:{int(x%60):02},{int(x%1*1000):03}"
def yt_ts(x): return f"{int(x//3600)}:{int(x%3600//60):02}:{int(x%60):02}" if x >= 3600 else f"{int(x//60)}:{int(x%60):02}"

def build(script_md, visuals, out_mp4, title_font=64):
    work = pathlib.Path(out_mp4).with_suffix(""); work.mkdir(parents=True, exist_ok=True)
    chapters = re.findall(r"^## (.+?)\n(.*?)(?=^## |\Z)", pathlib.Path(script_md).read_text(), re.S | re.M)
    parts, srt, chap_lines, clock = [], [], [], 0.0
    for i, (title, body) in enumerate(chapters):
        wav = work / f"ch{i:02}.wav"; mp4 = work / f"ch{i:02}.mp4"; png = work / f"ch{i:02}.png"
        if not mp4.exists():
            dur, times = narrate_chapter(body, str(wav))
            dur += 3.0
            paint(visuals[i % len(visuals)], seed=100 + i).save(png)
            safe = title.replace("'", "’").replace(":", "\\:")
            dx = 1 if i % 2 == 0 else -1
            vf = (f"crop={CW}:{CH}:x='(iw-{CW})/2+{dx}*(iw-{CW})/2*(2*t/{dur:.2f}-1)':y='(ih-{CH})/2+40*sin(t/40)',"
                  f"drawtext=fontfile={SERIF}:text='{safe}':fontsize={title_font}:fontcolor=white@0.85:"
                  f"x=(w-text_w)/2:y=h*0.80:alpha='if(lt(t,1),0,if(lt(t,3),(t-1)/2,if(lt(t,9),1,if(lt(t,11),(11-t)/2,0))))',"
                  f"fade=t=in:st=0:d=2,fade=t=out:st={dur-2:.2f}:d=2")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS), "-i", str(png),
                            "-i", str(wav), "-vf", vf, "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "veryfast",
                            "-tune", "stillimage", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
                            "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-af", "apad", str(mp4.with_suffix(".part.mp4"))], check=True)
            mp4.with_suffix(".part.mp4").rename(mp4)  # atomic: a killed render never leaves a half-written chapter
            (work / f"ch{i:02}.times").write_text("\n".join(f"{a}\t{b}\t{p}" for a, b, p in times))
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                                   capture_output=True, text=True).stdout)
        for line in (work / f"ch{i:02}.times").read_text().splitlines():
            a, b, p = line.split("\t", 2); srt.append((clock + float(a), clock + float(b), p))
        chap_lines.append(f"{yt_ts(clock)} {title}"); parts.append(mp4); clock += dur
        print(f"chapter {i+1}/{len(chapters)} {title}: {dur/60:.1f} min", flush=True)
    lst = work / "parts.txt"; lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    joined = work / "joined.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(joined)], check=True)
    pad = work / "pad.wav"; ambient_pad(str(pad), clock + 5)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(joined), "-i", str(pad), "-filter_complex",
                    "[0:a]loudnorm=I=-19:TP=-2[v];[1:a]volume=0.55,aresample=48000[m];[v][m]amix=inputs=2:normalize=0:duration=first[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", str(out_mp4)], check=True)
    with open(work / "captions.srt", "w") as fh:
        for n, (a, b, p) in enumerate(srt, 1): fh.write(f"{n}\n{ts(a)} --> {ts(b)}\n{p}\n\n")
    (work / "chapters.txt").write_text("\n".join(chap_lines) + "\n")
    return clock
