"""EP003 (long-form, sleep): 100 Quiet Facts About the Universe. Run: python episodes/ep003_universe_sleep/build.py"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
import sleep_engine
sleep_engine.PARA_PAUSE = 2.4   # slower, calmer gaps between facts
VISUALS = ["galaxy", "sun", "mars", "jupiter", "saturn", "nebula",
           "nebula", "galaxy", "deepfield", "earth_moon", "horizon"]
if __name__ == "__main__":
    total = sleep_engine.build(HERE / "script.md", VISUALS, ROOT / "output/ep003_universe_sleep.mp4")
    print(f"DONE total {total/60:.1f} min")
