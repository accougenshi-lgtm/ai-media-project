"""EP005 (original Short, 'Real Questions' format): Is a black hole screaming at us?
FACT SHEET (docs/factcheck_ep005.md): Perseus cluster ~250 million ly (NASA); Chandra (2003) found pressure waves in hot gas
around its central black hole; as a note: B-flat ~57 octaves below middle C; one oscillation ~10 million years (NASA: 9.6 Myr).
Test variable (11 AM plan 2026-11-23): original what-if/question Short vs clip Shorts."""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "pipeline"))
from engine import *
from PIL import ImageDraw

def black_hole(img, cx, cy, r, sec):
    d = ImageDraw.Draw(img)
    glow_disc(img, cx, cy, r * 1.45, (255, 190, 110), (120, 50, 10), glow=(255, 150, 60))   # accretion glow
    glow_disc(img, cx, cy, r, (2, 2, 3), (0, 0, 0))                                          # event horizon shadow

def waves(img, cx, cy, sec, strength=1.0):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for k in range(6):
        rr = (sec * 90 + k * 140) % 840 + 160
        a = int(110 * strength * (1 - (rr - 160) / 840))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(120, 190, 255, max(a, 0)), width=5)
    img.alpha_composite(layer)

def s_hook(img, t, sec):
    starfield(img, sec); waves(img, 540, 900, sec, seg(t, 0.2, 0.8)); black_hole(img, 540, 900, 130, sec)
    text_c(img, "IS A BLACK HOLE", 250, 80, alpha=seg(t, 0, .15))
    text_c(img, "SCREAMING AT US?", 345, 92, ACCENT, alpha=seg(t, 0, .15))

def s_where(img, t, sec):
    starfield(img, sec, 2); waves(img, 540, 900, sec); black_hole(img, 540, 900, 120, sec)
    text_c(img, "PERSEUS CLUSTER", 250, 70, alpha=seg(t, 0, .2))
    text_c(img, "~250 MILLION LIGHT YEARS", 340, 48, DIM, alpha=seg(t, .2, .4))

def s_note(img, t, sec):
    starfield(img, sec, 2); d = ImageDraw.Draw(img)
    for i in range(5):  # musical staff
        y = 760 + i * 46; d.line([140, y, 940, y], fill=DIM, width=3)
    x = 540; y = 760 + 3.5 * 46
    d.ellipse([x - 34, y - 24, x + 34, y + 24], fill=ACCENT); d.line([x + 32, y, x + 32, y - 170], fill=ACCENT, width=6)
    text_c(img, "♭", int(y - 70), 90, ACCENT, alpha=seg(t, .2, .35), cx=x - 90)
    text_c(img, "B-FLAT", 400, 110, alpha=seg(t, .3, .45))

def s_octaves(img, t, sec):
    starfield(img, sec, 2)
    n = int(57 * seg(t, 0.05, 0.6))
    text_c(img, f"{n}", 620, 300, ACCENT)
    text_c(img, "OCTAVES BELOW MIDDLE C", 980, 54)
    text_c(img, "one wave ≈ 10,000,000 years", 1080, 40, DIM, alpha=seg(t, .6, .75))

def s_end(img, t, sec):
    starfield(img, sec); waves(img, 540, 900, sec); black_hole(img, 540, 900, 130, sec)
    text_c(img, "THE DEEPEST NOTE EVER FOUND", 250, 56, alpha=seg(t, 0, .2))
    text_c(img, "STILL PLAYING", 330, 80, ACCENT, alpha=seg(t, .3, .45))

SCENES = [
    dict(draw=s_hook, text="Is a black hole screaming at us?", pad=0.25),
    dict(draw=s_where, text="In a way, yes. In the Perseus galaxy cluster, about two hundred and fifty million light years away, a giant black hole is pushing pressure waves through hot gas.", pad=0.3),
    dict(draw=s_note, text="Astronomers measured them with NASA's Chandra telescope. Turned into a musical note, it's a B flat.", pad=0.3),
    dict(draw=s_octaves, text="Fifty seven octaves below middle C. A single wave takes about ten million years.", pad=0.3),
    dict(draw=s_end, text="The deepest note ever found. And it's still playing.", pad=0.4),
]

if __name__ == "__main__":
    out = ROOT / "output/ep005_black_hole_scream.mp4"
    path, dur = build(SCENES, out, voice="dark"); print(f"rendered {path} ({dur:.1f}s)")
