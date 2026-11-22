"""EP002 (long-form, sleep): Moon facts to fall asleep to. Run: python episodes/ep002_moon_sleep/build.py"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
from sleep_engine import build
VISUALS = ["full", "earth_moon", "gibbous", "crescent", "closeup", "horizon",
           "earth_moon", "closeup", "gibbous", "eclipse", "horizon", "full"]
if __name__ == "__main__":
    total = build(HERE / "script.md", VISUALS, ROOT / "output/ep002_moon_sleep.mp4")
    print(f"DONE total {total/60:.1f} min")
