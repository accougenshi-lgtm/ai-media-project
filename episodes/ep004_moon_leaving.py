"""EP004 (Short, ~35 s): The Moon is leaving us.
FACT SHEET (docs/factcheck_ep004.md):
- Moon recedes ~3.8 cm/yr (Lunar Laser Ranging; NASA). Fingernails grow ~3–4 cm/yr: "about as fast".
- Retroreflectors left by Apollo 11, 14, 15 (plus Soviet Lunokhod rovers). Laser round trip ~2.5 s.
- 3.8 cm/yr × 600 Myr = 22,800 km ("at today's rate").
- Total solar eclipses end in roughly 600 million years, when the Moon can no longer cover the Sun (common estimate, hedged).
Structure (from research 2026-11-22): hook = premise in 5 words; one comparison per number; loop: last line = first line.
"""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "pipeline"))
from engine import *
from PIL import ImageDraw

def s_hook(img, t, sec):
    starfield(img, sec)
    earth(img, 330, 820, 170)
    moon(img, 760 + 120 * t, 820, 60)
    text_c(img, "THE MOON IS", 260, 84, alpha=seg(t, 0, .15))
    text_c(img, "LEAVING US", 360, 110, ACCENT, alpha=seg(t, 0, .15))

def s_rate(img, t, sec):
    starfield(img, sec, 2); d = ImageDraw.Draw(img)
    x0, x1, y = 160, 920, 820; g = seg(t, .1, .6)
    d.rounded_rectangle([x0, y - 40, x0 + (x1 - x0) * g, y + 40], radius=20, fill=ACCENT)
    for i in range(11):
        xx = x0 + (x1 - x0) * i / 10; d.line([xx, y + 50, xx, y + (80 if i % 5 == 0 else 65)], fill=DIM, width=4)
    text_c(img, f"{3.8 * g:.1f} cm", 560, 150, WHITE)
    text_c(img, "EVERY YEAR", 960, 60, DIM)
    text_c(img, "≈ how fast your fingernails grow", 1060, 40, alpha=seg(t, .55, .7))

def s_laser(img, t, sec):
    starfield(img, sec, 2); d = ImageDraw.Draw(img)
    earth(img, 540, 1320, 160); moon(img, 540, 420, 80)
    pulse = (sec * 0.8) % 1.0                       # a laser pulse going up and coming back
    yy = 1160 - (1160 - 500) * (pulse * 2 if pulse < .5 else 2 - pulse * 2)
    d.line([540, 1160, 540, 500], fill=(255, 80, 80), width=2)
    d.ellipse([528, yy - 12, 552, yy + 12], fill=(255, 120, 120))
    text_c(img, "APOLLO LEFT MIRRORS", 220, 56, alpha=seg(t, 0, .15))
    text_c(img, "2.5 s THERE AND BACK", 1560, 60, ACCENT, alpha=seg(t, .35, .5))

def s_math(img, t, sec):
    starfield(img, sec, 2)
    text_c(img, "3.8 cm × 600,000,000 yr", 560, 62, alpha=seg(t, 0, .2))
    text_c(img, "=", 680, 80, DIM, alpha=seg(t, .25, .35))
    km = int(22800 * seg(t, .3, .7))
    text_c(img, f"{km:,} km", 800, 130, ACCENT, alpha=seg(t, .3, .4))
    text_c(img, "farther away (at today's rate)", 980, 40, DIM, alpha=seg(t, .6, .75))

def s_eclipse(img, t, sec):
    starfield(img, sec, 1)
    cx, cy, sr = 540, 820, 210
    glow_disc(img, cx, cy, sr, (255, 240, 200), (255, 160, 40), glow=(255, 170, 60))
    mr = sr * (1.03 - 0.16 * seg(t, .1, .6))        # moon shrinks below the Sun's size: a ring remains
    glow_disc(img, cx, cy, mr, (18, 18, 22), (6, 6, 8))
    text_c(img, "TOO SMALL TO", 240, 70, alpha=seg(t, .4, .55))
    text_c(img, "COVER THE SUN", 330, 84, ACCENT, alpha=seg(t, .4, .55))

def s_loop(img, t, sec):
    starfield(img, sec)
    earth(img, 330, 820, 170)
    moon(img, 760 + 120 * t, 820, 60)
    text_c(img, "THE LAST TOTAL ECLIPSE", 260, 60, alpha=1 - seg(t, .5, .7))
    text_c(img, "IS ALREADY COMING", 340, 70, ACCENT, alpha=1 - seg(t, .5, .7))

SCENES = [
    dict(draw=s_hook, text="The Moon is leaving us.", pad=0.25),
    dict(draw=s_rate, text="Three point eight centimetres every year. About as fast as your fingernails grow.", pad=0.3),
    dict(draw=s_laser, text="We know because Apollo astronauts left mirrors up there. We fire lasers at them, and time the bounce.", pad=0.3),
    dict(draw=s_math, text="At today's rate, six hundred million years adds up to twenty two thousand kilometres.", pad=0.3),
    dict(draw=s_eclipse, text="Far enough that the Moon looks too small to cover the Sun.", pad=0.3),
    dict(draw=s_loop, text="The last total eclipse is already on its way.", pad=0.1),
]

if __name__ == "__main__":
    out = ROOT / "output/ep004_moon_leaving.mp4"
    path, dur = build(SCENES, out, voice="dark")
    print(f"rendered {path} ({dur:.1f}s)")
