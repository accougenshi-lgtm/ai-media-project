# Shorts pipeline v2: changelog (owner overhaul directive, 2026-11-24)
Repo map before change: pipeline/{engine.py (2D Shorts), clip_short.py (clips), sleep_engine.py, sound.py, qa.py, voice_fx.py,...}; no CI workflows.

## Added
- `pipeline/short_v2.py`: new end-to-end Shorts entrypoint (old `engine.py`/`clip_short.py` CLIs unchanged).
  - **Storyboard validator** (JSON): rejects question/hedge hooks, numbers without a human-scale `anchor`, headers that repeat spoken
    text, sound references without an early sensory `cue`, and loop endings that stop with punctuation.
  - **Real media**: NASA Image & Video Library (no key) → `assets/cache/` (public domain); procedural paintings only as fallback.
  - **VO**: per-beat TTS → `silenceremove` (inter-sentence pauses ≤180 ms) → `atempo=1.10` → HPF 80 Hz + 8 kHz presence.
  - **Single source of truth**: Whisper word timestamps on `clean_vo.wav` drive captions, headers and counters
    (counter starts 600 ms before its target word and lands on the word's end, cubic ease-out).
  - **Shots ≤2.4 s** (never >2.5 s per visual state): continuous zoompan push/pull + lateral drift, vignette, film grain, grade.
  - **Sensory payoff**: a dedicated silent window in the VO for the cue (e.g. Perseus B-flat raised into hearing range).
  - **5-stem mix**: VO, bed (HPF60/LPF5k, sidechaincompress 4:1 20/300 ms against VO), cue, hard SFX (pool, ±4–5% pitch, ±2 dB,
    riser cut ~50 ms before impacts ≥3.5 s apart), micro SFX (HPF150, panned); **two-pass loudnorm** I=−14, TP −1.5, LRA 7.
  - **Checks**: pauses >200 ms (cue windows exempt), loudness/true peak, static segments (qa.motion).
- `episodes/ep005v2_black_hole.json`: first v2 storyboard.
## Changed
- `pipeline/engine.py`: captions auto-shrink to fit width.
## Test result (EP005 v2)
- 0 pauses >200 ms · −14.4 LUFS / −1.44 dBTP · speech WER 0.0% · motion pass · NASA Perseus image as hook.
## Env / keys
- No API keys. Network allowlist added: images-api.nasa.gov, images-assets.nasa.gov. Pexels/Pixabay not used (would need keys).
## Not done (honest)
- WhisperX not installed: faster-whisper word timestamps used instead (same role).
- No NASA sonification audio exists in the NASA library API; the cue is synthesized from the published physics (B-flat raised into hearing range).
