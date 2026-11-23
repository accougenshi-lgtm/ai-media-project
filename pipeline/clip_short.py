"""Turn the most interesting self-contained fact from a rendered sleep episode into a vertical Short.
  python pipeline/clip_short.py rank  <episode_out_dir>            -> facts ranked by interest score (unused first)
  python pipeline/clip_short.py make  <episode_out_dir> <ch> <idx> <out.mp4> [speed=1.08]
Original material only (our own narration + our own paintings). Speeds the calm narration slightly for Shorts,
trims the spoken 'Fact N.' label, shows the hook sentence as a headline, word-chunk captions, slow vertical pan, soft pad."""
import sys, re, json, subprocess, pathlib, numpy as np, soundfile as sf
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
USED = ROOT / "research" / "clips_used.json"
SUPER = r"\b(largest|hottest|coldest|fastest|tallest|oldest|only|never|more than|billion|trillion|million|backwards|impossible|strange|rains?|diamonds?|alcohol|float)\b"

def facts(epdir):
    out = []
    for f in sorted(pathlib.Path(epdir).glob("ch*.times")):
        ch = int(f.stem[2:])
        for i, line in enumerate(f.read_text().splitlines()):
            a, b, p = line.split("\t", 2)
            if not re.match(r"Fact [a-z ]+[.:]", p): continue
            dur = float(b) - float(a)
            score = len(re.findall(r"\d|\b(one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand)\b", p.lower())) * 0.4 \
                    + len(re.findall(SUPER, p.lower())) * 1.5 + (2 if 17 <= dur <= 40 else -3)
            out.append(dict(ch=ch, idx=i, start=float(a), end=float(b), dur=dur, text=p, score=round(score, 1)))
    return out

def used(): return json.loads(USED.read_text()) if USED.exists() else []

def ass_time(t): return f"{int(t//3600)}:{int(t%3600//60):02}:{t%60:05.2f}"

def make(epdir, ch, idx, out, speed=1.08, kind=None, hook=None):
    from faster_whisper import WhisperModel
    epdir = pathlib.Path(epdir); fx = [f for f in facts(epdir) if f["ch"] == ch and f["idx"] == idx][0]
    wav, sr = sf.read(epdir / f"ch{ch:02}.wav", dtype="float32")
    seg = wav[int(fx["start"] * sr): int(fx["end"] * sr) + int(0.3 * sr)]
    tmp = pathlib.Path(out).with_suffix(""); tmp.mkdir(parents=True, exist_ok=True)
    sf.write(tmp / "raw.wav", seg, sr)
    # word timestamps → trim the "Fact N." label, time the captions
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(tmp / "raw.wav"), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
    words = [w for s in m.transcribe(np.frombuffer(pcm, np.float32), word_timestamps=True, beam_size=5)[0] for w in s.words]
    # cut at the first content word of the script (STT mishears the "Fact N." label, e.g. "Vagged 65")
    first = re.sub(r"[^a-z]", "", re.sub(r"^Fact [a-z ]+[.:]\s*", "", fx["text"]).split()[0].lower())
    k = next((i for i, w in enumerate(words[:10]) if re.sub(r"[^a-z]", "", w.word.lower()) == first), None)
    if k is None:  # fallback: skip label-like tokens
        LABEL = set("fact one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred".split())
        k = 0
        while k < len(words) and (re.sub(r"[^a-z]", "", words[k].word.lower()) in LABEL or re.sub(r"[^0-9]", "", words[k].word)): k += 1
    t0 = max(0.0, words[k].start - 0.08) if k < len(words) else 0.0
    words = words[k:]
    body = re.sub(r"^Fact [a-z ]+[.:]\s*", "", fx["text"])
    if not hook:  # headline must be short: first sentence, cut at the first comma if longer than 10 words
        hook = re.split(r"(?<=[.!?])\s", body)[0]
        if len(hook.split()) > 10: hook = hook.split(",")[0].rstrip(".") + "."
    from qa import US_UK
    for w in words:  # captions follow the script's (UK) spelling, like the headline
        core = re.sub(r"[^a-z]", "", w.word.lower())
        if core in US_UK: w.word = w.word.lower().replace(core, US_UK[core])
    # audio: trim, speed up (pitch kept), add soft pad, loudness for Shorts
    dur = (len(seg) / sr - t0) / speed
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t0:.3f}", "-i", str(tmp / "raw.wav"),
                    "-f", "lavfi", "-i", f"aevalsrc='0.03*sin(2*PI*110*t)*(0.6+0.4*sin(2*PI*t/7))+0.025*sin(2*PI*164.81*t)+0.02*sin(2*PI*220*t)*(0.5+0.5*sin(2*PI*t/5))':s={sr}:d={dur + 1:.2f}",
                    "-filter_complex", f"[0:a]atempo={speed}[v];[1:a]lowpass=f=1500,volume=0.55[m];[v][m]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5[a]",
                    "-map", "[a]", "-ar", "48000", str(tmp / "audio.wav")], check=True)
    # captions (ASS): 3-word chunks timed by Whisper; hook headline at top for the whole clip
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w.word.strip()[-1:] in ".,": chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    def esc(s): return s.replace("{", "(").replace("}", ")")
    ass = ["[Script Info]", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
           "Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Alignment,MarginL,MarginR,MarginV,BorderStyle,Outline,Shadow",
           "Style: Cap,DejaVu Sans,70,&H00F2EDE8,&H00000000,&H64000000,1,2,90,170,560,1,5,0",
           "Style: Hook,DejaVu Sans,58,&H00F8BD38,&H00000000,&H64000000,1,8,90,170,260,1,5,0",
           "Style: Tag,DejaVu Sans,34,&H00A0A8B4,&H00000000,&H00000000,1,8,90,170,170,1,2,0", "", "[Events]",
           "Format: Layer,Start,End,Style,Text",
           f"Dialogue: 0,{ass_time(0)},{ass_time(dur)},Tag,QUIET FACTS",
           f"Dialogue: 0,{ass_time(0)},{ass_time(dur)},Hook,{esc(hook.upper())}"]
    for c in chunks:
        a, b = (c[0].start - t0) / speed, (c[-1].end - t0) / speed + 0.05
        ass.append(f"Dialogue: 0,{ass_time(max(a,0))},{ass_time(b)},Cap,{esc(' '.join(w.word.strip() for w in c).upper())}")
    (tmp / "caps.ass").write_text("\n".join(ass))
    # video: vertical crop of the chapter painting with a slow pan (2400x1350 → 760x1350 window → 1080x1920)
    png = epdir / f"ch{ch:02}.png"
    if kind:  # topic-matched painting, painted natively in portrait so the subject fills the frame
        import sleep_engine as se
        se.OW, se.OH = 1188, 2112; se.paint(kind, seed=ch * 100 + idx).save(tmp / "bg.png"); png = tmp / "bg.png"
    vf = (f"scale=w='trunc(1188*(1+0.09*t/{dur:.2f})/2)*2':h=-2:eval=frame:flags=bicubic,crop=1080:1920:(iw-1080)/2:(ih-1920)/2," if kind else
          f"crop=760:1350:x='(iw-760)*(0.25+0.5*t/{dur:.2f})':y=0,scale=1080:1920:flags=lanczos,")
    vf += (f"ass={tmp/'caps.ass'},fade=t=in:st=0:d=0.25,fade=t=out:st={dur-0.4:.2f}:d=0.4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-i", str(png), "-i", str(tmp / "audio.wav"),
                    "-vf", vf, "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)
    u = used(); u.append(f"{epdir.name}:{ch}:{idx}"); USED.write_text(json.dumps(u))
    print(json.dumps(dict(out=str(out), dur=round(dur, 1), hook=hook)))

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "rank":
        u = used(); fs = [f for f in facts(a[1]) if f"{pathlib.Path(a[1]).name}:{f['ch']}:{f['idx']}" not in u]
        for f in sorted(fs, key=lambda f: -f["score"])[:15]: print(f"{f['score']:5} ch{f['ch']:02} #{f['idx']:<2} {f['dur']:4.1f}s  {f['text'][:95]}")
    else:
        make(a[1], int(a[2]), int(a[3]), a[4], float(a[5]) if len(a) > 5 and a[5] != "-" else 1.08, a[6] if len(a) > 6 else None, a[7] if len(a) > 7 else None)
