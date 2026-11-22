# 1% AI Media Project: operating rules

Mission: build an AI-assisted YouTube channel to monetization with original, well-made, fact-checked videos.
Current channel #1: science what-ifs with real math (see docs/STRATEGY.md). Free tools only until data justifies spending.

## Hard rules
- Never publish, spend money, delete, or change accounts without the owner's OK.
- Every factual claim needs a source or a shown derivation in `docs/factcheck_epNNN.md`.
- Never invent analytics or competitor numbers; research numbers come from `research/research.db` with fetch dates.
- Only public-domain / CC0 / self-made assets; log credits in `assets/pd/credits.json`.
- No templated mass production: each episode gets its own script, scenes and math.
- Test one variable at a time; log hypothesis → change → result → conclusion.

## How to run
- Research: `python3 pipeline/research_niches.py && python3 pipeline/channels.py && python3 pipeline/analyze.py`
- Render an episode: `python3 episodes/ep001_moon_twice_as_close.py [voice]` → `output/` (mp4 + captions.srt)
- Models: `models/kokoro-v1.0.onnx`, `models/voices-v1.0.bin` (from github.com/thewh1teagle/kokoro-onnx releases, not committed)
- Deps: `pip install yt-dlp kokoro-onnx soundfile pillow matplotlib`; ffmpeg.
