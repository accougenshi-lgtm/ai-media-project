#!/bin/sh
# One-shot clip: make + all blind QA + contact sheet, compact output.
# Usage: sh pipeline/make_clip.sh <epdir> <ch> <idx> <out.mp4> <kind> ["custom hook"]
set -e; E="$1"; CH="$2"; IX="$3"; OUT="$4"; K="$5"; H="${6:-}"
export HF_HUB_DISABLE_XET=1
python3 pipeline/clip_short.py make "$E" "$CH" "$IX" "$OUT" - "$K" ${H:+"$H"} 2>/dev/null | tail -1
python3 - "$E" "$CH" "$IX" "${OUT%.mp4}.txt" <<'PY'
import sys,re; sys.path.insert(0,'pipeline'); from clip_short import facts
f=[x for x in facts(sys.argv[1]) if x['ch']==int(sys.argv[2]) and x['idx']==int(sys.argv[3])][0]
open(sys.argv[4],'w').write(re.sub(r"^Fact [a-z ]+[.:]\s*","",f['text']))
PY
A=$(python3 pipeline/qa.py audio "$OUT" "${OUT%.mp4}.txt" 2>/dev/null | grep -E '"wer"|"pass"' | tr -d ' \n')
L=$(python3 pipeline/qa.py loud "$OUT" short | grep '"pass"' | tr -d ' ')
M=$(python3 pipeline/qa.py motion "$OUT" short | grep '"pass"' | tr -d ' ')
echo "QA audio:$A loud:$L motion:$M size:$(wc -c < "$OUT")"
for s in 1 12; do ffmpeg -loglevel error -y -ss $s -i "$OUT" -frames:v 1 -vf scale=270:-1 "output/qa/mc_$s.png"; done
python3 -c "
from PIL import Image
a=Image.open('output/qa/mc_1.png');b=Image.open('output/qa/mc_12.png');S=Image.new('RGB',(a.width*2,a.height));S.paste(a,(0,0));S.paste(b,(a.width,0));S.save('output/qa/mc_sheet.png')"
