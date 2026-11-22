"""Speech-style stats from timestamped transcripts ([m:ss] markers). Usage: python pipeline/speech_stats.py file.json ..."""
import json, re, sys, statistics as st
def ts(s):
    p=[int(x) for x in s.split(":")]; return sum(v*60**i for i,v in enumerate(reversed(p)))
for f in sys.argv[1:]:
    t=json.load(open(f))["transcription"]
    marks=[ts(m) for m in re.findall(r"\[(\d+:\d{2}(?::\d{2})?)\]", t)]
    text=re.sub(r"\[[^\]]*\]"," ",t); words=text.split()
    dur=max(marks) if marks else 1
    sents=[s for s in re.split(r"(?<=[.!?])\s+", text) if len(s.split())>1]
    sl=[len(s.split()) for s in sents]
    low=text.lower(); W=len(words)
    you=len(re.findall(r"\byou\b|\byour\b",low)); q=text.count("?")
    print(f"{f.split('/')[-1]:22} words={W:6} min={dur/60:6.1f} wpm={W/(dur/60):5.0f} sent_med={st.median(sl):4.1f} sent_p90={sorted(sl)[int(len(sl)*.9)]:3} you/1k={you/W*1000:5.1f} q/1k={q/W*1000:4.1f}")
