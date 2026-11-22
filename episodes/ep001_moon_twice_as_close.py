"""EP001 (Short): What if the Moon were twice as close?
FACT SHEET (all derived from standard physics, see docs/factcheck_ep001.md):
- Mean Earth-Moon distance 384,400 km -> 192,200 km.
- Tidal (differential) force ~ M/d^3  -> 2^3 = 8x.
- Angular diameter ~ 1/d -> 2x wider; apparent area 4x -> full-moon light ~4x.
- Kepler III: T ~ a^1.5 -> 27.32 d / 2.828 = 9.66 d sidereal.
- Moon's angular size (~0.52 deg) doubles to ~1.04 deg > Sun (~0.53 deg) always -> no annular eclipses.
- Tidal braking torque ~ 1/d^6 -> 2^6 = 64x faster spin-down.
- Roche limit (~9,500-18,000 km) is far below 192,200 km -> Moon stays intact.
"""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "pipeline"))
from engine import *
from PIL import ImageDraw

def s1(img, t, sec):  # hook: moon slides in to half distance, "8" lands
    starfield(img, sec)
    earth(img, 300, 760, 150)
    x = 980 - 360 * seg(t, 0.05, 0.6)
    moon(img, x, 760, 40 + 40 * seg(t, 0.05, 0.6))
    text_c(img, "WHAT IF THE MOON WERE", 230, 58, alpha=seg(t, 0, .1))
    text_c(img, "TWICE AS CLOSE?", 310, 92, ACCENT, alpha=seg(t, 0, .1))
    text_c(img, "8", 930, 300, ACCENT, alpha=seg(t, 0.7, 0.85))
    text_c(img, "not to scale", 1840, 26, DIM, bold=False)

def s2(img, t, sec):  # tidal force curve 1/d^3
    starfield(img, sec, 2); d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 140, 1180, 960, 380
    d.line([x0, y0, x1, y0], fill=DIM, width=4); d.line([x0, y0, x0, y1], fill=DIM, width=4)
    pts = []
    for i in range(101):
        dist = 0.45 + 0.6 * i / 100; f = 1 / dist**3
        pts.append((x0 + (dist - 0.45) / 0.6 * (x1 - x0), y0 - min(f, 11) / 11 * (y0 - y1)))
    d.line(pts, fill=(120, 190, 255), width=8)
    cur = 1 - 0.5 * seg(t, 0.25, 0.75); f = 1 / cur**3
    px = x0 + (cur - 0.45) / 0.6 * (x1 - x0); py = y0 - min(f, 11) / 11 * (y0 - y1)
    d.ellipse([px - 22, py - 22, px + 22, py + 22], fill=ACCENT)
    text_c(img, "TIDAL FORCE  ∝  1 / distance³", 230, 54)
    text_c(img, f"{f:.1f}×", 1230, 120, ACCENT)
    text_c(img, "distance →", 1190, 34, DIM, bold=False, alpha=1 - seg(t, .2, .3))

def s3(img, t, sec):  # apparent size and brightness
    starfield(img, sec, 2)
    g = seg(t, 0.15, 0.6)
    moon(img, 300, 700, 110); moon(img, 760, 700, 110 + 110 * g)
    text_c(img, "TODAY", 860, 44, DIM, cx=300)
    text_c(img, "HALF THE DISTANCE", 960, 40, ACCENT, cx=760, alpha=seg(t, .3, .45))
    text_c(img, "2× WIDER", 330, 78, ACCENT, alpha=seg(t, .3, .45))
    text_c(img, "4× THE SKY  ·  ~4× BRIGHTER NIGHTS", 1060, 46, alpha=seg(t, .55, .7))

def s4(img, t, sec):  # Kepler: faster orbit
    starfield(img, sec, 2); d = ImageDraw.Draw(img)
    earth(img, 540, 760, 90)
    for r, period, col in [(380, 27.3, DIM), (230, 9.66, ACCENT)]:
        d.ellipse([540 - r, 760 - r, 540 + r, 760 + r], outline=col, width=3)
        ang = sec / period * 2 * math.pi * 2.5
        moon(img, 540 + r * math.cos(ang), 760 + r * math.sin(ang), 34 if col == DIM else 46)
    text_c(img, "T ∝ distance^1.5", 230, 60)
    text_c(img, "27.3 DAYS  →  9.7 DAYS", 1230, 70, ACCENT, alpha=seg(t, .3, .45))

def s5(img, t, sec):  # eclipses
    starfield(img, sec, 1)
    sun_r = 200; cx, cy = 540, 760
    glow_disc(img, cx, cy, sun_r, (255, 240, 200), (255, 160, 40), glow=(255, 170, 60))
    mr = sun_r * (0.97 + 1.0 * seg(t, 0.35, 0.65))  # today's moon ~ sun size; doubled = ~2x
    mx = cx + 420 * (1 - seg(t, 0.0, 0.3))
    glow_disc(img, mx, cy, mr, (18, 18, 22), (6, 6, 8))
    text_c(img, "TOTAL ECLIPSES: COMMON & LONG", 300, 52, alpha=seg(t, .5, .62))
    text_c(img, "RING OF FIRE: GONE", 380, 72, ACCENT, alpha=seg(t, .7, .82))

def s6(img, t, sec):  # 2^3 vs 2^6
    starfield(img, sec, 2); d = ImageDraw.Draw(img)
    base = 1200; g = seg(t, 0.15, 0.7)
    for x, val, lab, col in [(330, 8, "TIDES  2³", (120, 190, 255)), (750, 64, "SPIN-DOWN  2⁶", ACCENT)]:
        h = 760 * val / 64 * g
        d.rounded_rectangle([x - 110, base - h, x + 110, base], radius=18, fill=col)
        text_c_x = x
        f = font(44); w = d.textlength(lab, font=f); d.text((x - w / 2, base + 24), lab, font=f, fill=WHITE)
        f2 = font(80); s = f"{int(val * g)}×"; w2 = d.textlength(s, font=f2)
        d.text((x - w2 / 2, base - h - 100), s, font=f2, fill=WHITE, stroke_width=4, stroke_fill=(0, 0, 0))
    text_c(img, "TIDAL BRAKING  ∝  1 / distance⁶", 230, 50)

def s7(img, t, sec):  # outro
    starfield(img, sec)
    earth(img, 540, 1000, 230); moon(img, 820, 560, 120)
    text_c(img, "ONE CHANGE.", 230, 80)
    text_c(img, "REAL MATH.", 330, 80, ACCENT)

SCENES = [
    dict(draw=s1, text="Bring the Moon twice as close to Earth, and one number explains almost everything that happens next. Eight."),
    dict(draw=s2, text="Tides come from the difference in the Moon's pull across our planet. That difference falls with the cube of distance. Halve the distance, and the force raising our oceans grows two cubed. Eight times stronger."),
    dict(draw=s3, text="The Moon would look twice as wide, covering four times as much sky. Full moon nights would be roughly four times brighter."),
    dict(draw=s4, text="Kepler's third law says it would speed up too. Instead of twenty seven days, one orbit would take under ten."),
    dict(draw=s5, text="Total solar eclipses would become common, and long. And the ring of fire would vanish forever, because the Moon could never look smaller than the Sun again."),
    dict(draw=s6, text="But the quietest change matters most. Tidal braking scales with the sixth power of distance. Two to the sixth is sixty four. Earth's spin would slow sixty four times faster, stretching our days far sooner."),
    dict(draw=s7, text="One change. Real math. Follow for the next what if.", pad=0.9),
]

if __name__ == "__main__":
    out = ROOT / "output/ep001_moon_twice_as_close.mp4"
    path, dur = build(SCENES, out, voice=(sys.argv[1] if len(sys.argv) > 1 else "dark"))
    print(f"rendered {path} ({dur:.1f}s)")
