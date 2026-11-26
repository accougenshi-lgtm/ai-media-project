"""Shorts pipeline v2 (owner's overhaul directive, 2026-11-24). One storyboard JSON → validated → VO (silence-capped, 1.10×) →
word-level alignment (single source of truth) → shots ≤2.4 s with continuous motion, vignette, grain, real NASA media →
token-bound captions/headers/counters (ASS) → 5-stem mix (VO, bed, sensory cue, hard SFX, micro SFX) → −14 LUFS / −1 dBTP → checks.
  python pipeline/short_v2.py <storyboard.json> <out.mp4>
Storyboard: {"key":"Bb","loop":true,"beats":[{"text","header","bg":{"nasa":id}|{"paint":kind},"anchor"?,"counter"?:{"to":57,"word":"seven"},
             "sfx"?:"impact"|"whoosh","cue"?:{"tone_hz":466.16,"ms":2500,"label":"..."}}]}"""
import os, sys, json, re, pathlib, subprocess, random, numpy as np, soundfile as sf
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")   # xet CAS downloads fail behind the proxy (2026-11-26)
ROOT = pathlib.Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ROOT / "pipeline"))
CACHE = ROOT / "assets" / "cache"; CACHE.mkdir(parents=True, exist_ok=True); SR = 48000; FPS = 30
NUM = re.compile(r"\d|\b(hundred|thousand|million|billion|trillion|octaves?|light years?)\b", re.I)
HEDGE = re.compile(r"\b(in a way|sort of|kind of|maybe|perhaps|might)\b", re.I)
def sh(*a): subprocess.run(a, check=True, capture_output=True)

def validate(sb):
    errs, b = [], sb["beats"]
    if "?" in b[0]["text"] or HEDGE.search(b[0]["text"]) or HEDGE.search(b[1]["text"] if len(b) > 1 else ""):
        errs.append("hook must be a paradox/proof statement: no question, no hedge")
    for i, x in enumerate(b):
        if NUM.search(x["text"]) and not x.get("anchor"): errs.append(f"beat {i}: number without human-scale anchor")
        if x.get("header", "").lower().strip(" .") and x["header"].lower().strip(" .") in x["text"].lower(): errs.append(f"beat {i}: header repeats spoken text")
    if any(re.search(r"\b(sound|hear|note|recording)\b", x["text"], re.I) for x in b) and not any("cue" in x for x in b[:4]):
        errs.append("references a sound but has no sensory cue in the first beats")
    if sb.get("loop") and b[-1]["text"].rstrip()[-1:] in ".!?": errs.append("loop bridge: last line must run into the first line (no final stop)")
    return errs

def nasa(nid):
    p = CACHE / f"{nid}.jpg"
    if not p.exists():
        meta = json.loads(subprocess.run(["curl", "-s", "-m", "60", f"https://images-api.nasa.gov/asset/{nid}"], capture_output=True, text=True).stdout)
        hrefs = [h["href"] for h in meta["collection"]["items"]]   # some assets have no ~large: fall back to ~orig
        href = next(h for suf in ("~large.jpg", "~orig.jpg") for h in hrefs if h.endswith(suf)).replace("http://", "https://")
        sh("curl", "-s", "-m", "120", "-o", str(p), href)
    return p

def vo(beats, work):
    from voice_fx import render
    parts = []
    for i, x in enumerate(beats):
        w = work / f"b{i}.wav"; render("dark", x["text"], str(w), seed=i); parts.append(w)
    (work / "l.txt").write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "l.txt"), str(work / "raw_vo.wav"))
    sh("ffmpeg", "-y", "-i", str(work / "raw_vo.wav"), "-af",
       "silenceremove=start_periods=1:start_threshold=-40dB:stop_periods=-1:stop_duration=0.18:stop_threshold=-40dB,atempo=1.10,highpass=f=80,treble=g=2:f=8000",
       "-ar", str(SR), "-ac", "1", str(work / "clean_vo.wav"))
    return work / "clean_vo.wav"

def align(wav, beats):
    from faster_whisper import WhisperModel
    a, sr = sf.read(wav, dtype="float32"); x = np.interp(np.arange(0, len(a), sr / 16000), np.arange(len(a)), a).astype(np.float32)
    words = [w for s in WhisperModel("small.en", device="cpu", compute_type="int8").transcribe(x, word_timestamps=True, beam_size=5)[0] for w in s.words]
    return assign([(w.word.strip(), w.start, w.end) for w in words], beats), len(a) / sr

def assign(toks, beats):
    """Map STT tokens to beats by aligning normalized words (2026-11-26: word counts drifted when Whisper wrote
    'one point three' as '1' '.3' or 'a hundred and seven thousand' as '107' ',000')."""
    import difflib
    from qa import norm
    m = []   # merge split numbers: '1' '.3' → '1.3', '23' ',000' → '23,000'
    for w, s0, s1 in toks:
        if m and re.match(r"^[.,]\d", w) and re.search(r"\d$", m[-1][0]): m[-1] = (m[-1][0] + w, m[-1][1], s1)
        else: m.append((w, s0, s1))
    hw, hi = [], []   # normalized STT words → token index
    for i, (w, _, _) in enumerate(m):
        for x in norm(w).split(): hw.append(x); hi.append(i)
    sw, si = [], []   # normalized script words → beat index
    for b, x_ in enumerate(beats):
        for x in norm(x_["text"]).split(): sw.append(x); si.append(b)
    first = {}   # beat → first matched token
    for blk in difflib.SequenceMatcher(None, sw, hw, autojunk=False).get_matching_blocks():
        for j in range(blk.size):
            b = si[blk.a + j]; t = hi[blk.b + j]; first[b] = min(first.get(b, t), t)
    starts, prev = [], 0
    for b in range(len(beats)):
        t = max(prev, first.get(b, prev + 1 if b else 0)) if b else 0; starts.append(min(t, len(m) - 1)); prev = starts[-1]
    out = []
    for b, t0 in enumerate(starts):
        t1 = starts[b + 1] if b + 1 < len(starts) else len(m); seg = m[t0:max(t1, t0 + 1)]
        out.append(dict(start=seg[0][1], end=seg[-1][2], words=seg))
    w, s0, s1 = out[-1]["words"][-1]; out[-1]["words"][-1] = (w.rstrip(".!"), s0, s1)   # loop bridge never ends with a stop
    return out

def ass_t(s): s = max(0, s); return f"{int(s//3600)}:{int(s%3600//60):02}:{s%60:05.2f}"
def captions(al, beats, dur):
    L = ["[Script Info]", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
         "Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Alignment,MarginL,MarginR,MarginV,BorderStyle,Outline,Shadow",
         "Style: Cap,DejaVu Sans,72,&H00F2EDE8,&H00000000,&H64000000,1,2,90,170,560,1,6,0",
         "Style: Head,DejaVu Sans,46,&H00F8BD38,&H00000000,&H00000000,1,8,90,170,210,1,3,0",
         "Style: Count,DejaVu Sans,230,&H000B9EF5,&H00000000,&H00000000,1,5,0,0,0,1,8,0", "", "[Events]", "Format: Layer,Start,End,Style,Text"]
    for i, (b, a) in enumerate(zip(beats, al)):
        end = al[i + 1]["start"] if i + 1 < len(al) else dur
        if b.get("header"): L.append(f"Dialogue: 0,{ass_t(a['start'])},{ass_t(end)},Head,{{\\fad(120,120)}}{b['header'].upper()}")
        ws = a["words"]
        for j in range(0, len(ws), 3):
            ch = ws[j:j + 3]; txt = re.sub(r"\s+([,.%])", r"\1", " ".join(w for w, _, _ in ch)).upper()   # "300 ,000" → "300,000"
            L.append(f"Dialogue: 0,{ass_t(ch[0][1])},{ass_t(ch[-1][2] + 0.04)},Cap,{{\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}}{txt}")
        c = b.get("counter")
        if c:   # token-bound: start 600 ms before the target word, land exactly on its end
            tgt = next((w for w in ws if c["word"].lower() in w[0].lower() or str(c["to"]) in w[0].replace(",", "")), ws[-1]); t0, t1 = tgt[1] - 0.6, tgt[2]   # STT may write digits
            steps = max(2, int((t1 - t0) * FPS))
            for s in range(steps):
                u = s / (steps - 1); v = round(c["to"] * (1 - (1 - u) ** 3))   # cubic ease-out
                L.append(f"Dialogue: 1,{ass_t(t0 + (t1 - t0) * s / steps)},{ass_t(t0 + (t1 - t0) * (s + 1) / steps)},Count,{v:,}")
            L.append(f"Dialogue: 1,{ass_t(t1)},{ass_t(end)},Count,{c['to']:,}")
    return "\n".join(L)

def shots(beats, al, dur, work):
    import sleep_engine as se; clips = []
    for i, (b, a) in enumerate(zip(beats, al)):
        t0 = 0 if i == 0 else a["start"]; t1 = al[i + 1]["start"] if i + 1 < len(al) else dur
        if "nasa" in b["bg"]: src = nasa(b["bg"]["nasa"])
        else:
            src = work / f"p{i}.png"; se.OW, se.OH = 1188, 2112; se.paint(b["bg"]["paint"], seed=40 + i).save(src)
        n = max(1, int(np.ceil((t1 - t0) / 2.4)))  # ≤2.4 s per visual state
        for k in range(n):
            d = (t1 - t0) / n; z0 = 1.0 + 0.06 * (k % 2); dz = 0.0016 if k % 2 == 0 else -0.0012   # alternate push-in / pull-out punch
            out = work / f"s{i}_{k}.mp4"; fr = max(1, int(round(d * FPS)))
            vf = (f"scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,"
                  f"zoompan=z='{z0}+{dz}*on':x='iw/2-(iw/zoom/2)+{(-1) ** k * 18}*on/{fr}':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps={FPS},"
                  f"vignette=PI/4.5,noise=alls=7:allf=t,eq=contrast=1.05:saturation=1.08")
            sh("ffmpeg", "-y", "-loop", "1", "-i", str(src), "-vf", vf, "-frames:v", str(fr), "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", str(out))
            clips.append(out)
    (work / "v.txt").write_text("".join(f"file '{c.resolve()}'\n" for c in clips))
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "v.txt"), "-c", "copy", str(work / "video.mp4"))

def mix(beats, al, dur, voice, key, work):
    from sound import bed, whoosh, impact, pop, riser, KEYS
    n = int(dur * SR) + SR // 4; root = KEYS[key]
    def place(buf, x, at, gain_db, pitch=1.0):
        if pitch != 1.0: x = np.interp(np.arange(0, len(x), pitch), np.arange(len(x)), x)
        x = x / (np.abs(x).max() + 1e-9) * 10 ** (gain_db / 20); s = max(0, int(at * SR)); buf[s:s + len(x)] += x[:len(buf) - s]
    B = np.zeros(n); place(B, bed(dur + .25, root), 0, -30)
    H = np.zeros(n); M = np.zeros(n); C = np.zeros(n); last = -9
    for i, (b, a) in enumerate(zip(beats, al)):
        if i and b.get("sfx") == "impact" and a["start"] - last >= 3.5:
            place(H, riser(1100, root), a["start"] - 1.1 - 0.05, -16); place(H, impact(), a["start"], -9, random.uniform(.96, 1.04)); last = a["start"]
        elif i: place(H, whoosh(random.choice([220, 280, 340])), a["start"] - .15, -17 + random.uniform(-2, 2), random.uniform(.95, 1.05))
        if b.get("counter"): place(M, pop(random.uniform(-3, 3)), a["start"] + .3, -21 + random.uniform(-2, 2))
        if b.get("cue"):   # sensory payoff: the real phenomenon made audible (synthesized from the physics)
            tt = np.arange(int(b["cue"]["ms"] * SR / 1000)) / SR; f = b["cue"]["tone_hz"]
            tone = (np.sin(2 * np.pi * f * tt) + .35 * np.sin(4 * np.pi * f * tt)) * np.minimum(1, tt / .25) * np.minimum(1, (tt[-1] - tt) / .4 + 1e-9)
            place(C, tone, b.get("cue_at", a["start"] + .2), -12)
    for nm, buf in [("bed", B), ("hard", H), ("micro", M), ("cue", C)]: sf.write(work / f"{nm}.wav", buf.astype(np.float32), SR)
    fg = ("[1:a]highpass=f=60,lowpass=f=5000[bd];[bd][0:a]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[bdk];"
          "[2:a]highpass=f=30[h];[3:a]highpass=f=150,pan=stereo|c0=0.65*c0|c1=0.35*c0[m];[4:a]lowpass=f=6000[c];"
          "[0:a]volume=1.0[v];[v][bdk][h][m][c]amix=inputs=5:normalize=0[out]")
    sh("ffmpeg", "-y", "-i", str(voice), "-i", str(work / "bed.wav"), "-i", str(work / "hard.wav"), "-i", str(work / "micro.wav"),
       "-i", str(work / "cue.wav"), "-filter_complex", fg, "-map", "[out]", "-ar", str(SR), str(work / "premaster.wav"))
    # two-pass loudnorm (linear) → −14 LUFS exactly, true peak ≤ −1 dBTP after AAC (target −1.5 for codec headroom)
    r = subprocess.run(["ffmpeg", "-i", str(work / "premaster.wav"), "-af", "loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr; m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    sh("ffmpeg", "-y", "-i", str(work / "premaster.wav"), "-af",
       f"loudnorm=I=-14:TP=-1.5:LRA=7:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
       "-ar", str(SR), str(work / "master.wav"))

def checks(work, out, cues=0):
    r = subprocess.run(["ffmpeg", "-i", str(work / "clean_vo.wav"), "-af", "silencedetect=n=-40dB:d=0.2", "-f", "null", "-"], capture_output=True, text=True).stderr
    pauses = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", r)]
    from qa import loud, motion
    return dict(pauses_over_200ms_excluding_cue_windows=max(0, len(pauses) - cues), loud=loud(out, "short"), motion=motion(out, "short"))

if __name__ == "__main__":
    sb = json.loads(pathlib.Path(sys.argv[1]).read_text()); out = pathlib.Path(sys.argv[2])
    errs = validate(sb)
    if errs: print("STORYBOARD REJECTED:\n- " + "\n- ".join(errs)); sys.exit(2)
    work = out.with_suffix(""); work.mkdir(parents=True, exist_ok=True)
    v = vo(sb["beats"], work); al, dur = align(v, sb["beats"])
    for i, b in enumerate(sb["beats"]):   # sensory cue gets its own clean window: open a gap in the VO after that beat's last word
        if b.get("cue"):
            gap = b["cue"]["ms"] / 1000 + 0.15; cut = al[i]["end"] + 0.05
            a, sr = sf.read(v, dtype="float32"); k = int(cut * sr)
            sf.write(v, np.concatenate([a[:k], np.zeros(int(gap * sr), np.float32), a[k:]]), sr)
            b["cue_at"] = cut
            for j in range(i + 1, len(al)):
                al[j]["start"] += gap; al[j]["end"] += gap; al[j]["words"] = [(w, s0 + gap, s1 + gap) for w, s0, s1 in al[j]["words"]]
            dur += gap
    (work / "caps.ass").write_text(captions(al, sb["beats"], dur)); shots(sb["beats"], al, dur, work)
    mix(sb["beats"], al, dur, v, sb.get("key", "D"), work)
    sh("ffmpeg", "-y", "-i", str(work / "video.mp4"), "-i", str(work / "master.wav"), "-vf", f"ass={work / 'caps.ass'}",
       "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-maxrate", "12M", "-bufsize", "24M", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out))
    json.dump(dict(alignment=al, duration=dur), open(work / "alignment.json", "w"), indent=1)
    print(json.dumps(checks(work, out, sum(1 for b in sb["beats"] if b.get("cue")))))
