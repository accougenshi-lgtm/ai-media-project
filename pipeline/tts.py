"""Free local narration with Kokoro (Apache-2.0). Splits script into paragraphs, renders each,
joins with natural pauses. Usage: python pipeline/tts.py script.txt out.wav [voice] [speed]"""
import sys, pathlib, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ROOT = pathlib.Path(__file__).resolve().parent.parent
M = ROOT / "models"

def narrate(text, out, voice="bm_george", speed=0.95, pause=0.55):
    k = Kokoro(str(M / "kokoro-v1.0.onnx"), str(M / "voices-v1.0.bin"))
    lang = "en-gb" if voice.startswith("b") else "en-us"
    chunks, sr = [], 24000
    for para in [p.strip() for p in text.split("\n\n") if p.strip()]:
        audio, sr = k.create(para, voice=voice, speed=speed, lang=lang)
        chunks += [audio, np.zeros(int(sr * pause), dtype=audio.dtype)]
    sf.write(out, np.concatenate(chunks), sr)
    return out

if __name__ == "__main__":
    txt = pathlib.Path(sys.argv[1]).read_text()
    narrate(txt, sys.argv[2], *(sys.argv[3:4] or []), *( [float(sys.argv[4])] if len(sys.argv) > 4 else []))
