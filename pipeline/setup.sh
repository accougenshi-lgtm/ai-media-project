#!/usr/bin/env bash
# Idempotent setup for a fresh container: python deps + Kokoro voice model.
set -e
cd "$(dirname "$0")/.."
pip install -q yt-dlp kokoro-onnx soundfile pillow matplotlib faster-whisper 2>/dev/null || true
mkdir -p models
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "models/$f" ] || curl -sSL -o "models/$f" "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done
echo "setup ok"
