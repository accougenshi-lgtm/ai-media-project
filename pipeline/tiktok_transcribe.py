"""Download + transcribe every video of given TikTok accounts (resumable). Stores in research.db table tiktok.
Order: each account's top videos by views first, then most recent, then the rest.
Usage: HF_HUB_DISABLE_XET=1 python pipeline/tiktok_transcribe.py blakeryan052 sina.growthtech"""
import sys, json, sqlite3, subprocess, pathlib, datetime, os
from faster_whisper import WhisperModel

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "research/tiktok/tiktok_work.db"  # gitignored while running; merged into research.db when done
AUD = ROOT / "research/tiktok/audio"; AUD.mkdir(parents=True, exist_ok=True)

def main(users):
    db = sqlite3.connect(DB)
    db.execute("""CREATE TABLE IF NOT EXISTS tiktok(id TEXT PRIMARY KEY, user TEXT, posted TEXT, views INT, likes INT,
                  comments INT, shares INT, saves INT, duration INT, description TEXT, transcript TEXT, fetched_at TEXT)""")
    model = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=4)
    lists = []
    for u in users:
        es = [e for e in json.load(open(ROOT / f"research/tiktok/{u}.json"))["entries"] if e]
        by_views = sorted(es, key=lambda e: -(e.get("view_count") or 0))
        by_recent = sorted(es, key=lambda e: -(e.get("timestamp") or 0))
        seen = set()
        lists.append([(u, e) for e in by_views[:100] + by_recent[:50] + by_views[100:]
                      if not (e["id"] in seen or seen.add(e["id"]))])
    # interleave accounts so both progress
    queue = [x for i in range(max(map(len, lists))) for l in lists if i < len(l) for x in [l[i]]]
    snap = ROOT / "research/tiktok/tiktok_snapshot.db"  # committed copy: resume from it after a container reset
    if snap.exists() and db.execute("select count(*) from tiktok").fetchone()[0] == 0:
        s = sqlite3.connect(snap); db.executemany("insert or replace into tiktok values (?,?,?,?,?,?,?,?,?,?,?,?)", s.execute("select * from tiktok")); db.commit()
    done = {r[0] for r in db.execute("select id from tiktok where transcript is not null")}
    for n, (u, e) in enumerate(queue, 1):
        if e["id"] in done: continue
        f = AUD / f"{e['id']}.mp3"
        r = subprocess.run(["yt-dlp", "-q", "-f", "b[url*=webapp-prime]/ba[url*=webapp-prime]/b[url*=v16m]/b[url*=v19]/b", "-x", "--audio-format", "mp3", "--audio-quality", "9",
                            "-o", str(AUD / "%(id)s.%(ext)s"), e["url"]], capture_output=True, text=True, timeout=600)
        text = None
        if f.exists():
            import numpy as np
            pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(f), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                 capture_output=True).stdout
            segs, _ = model.transcribe(np.frombuffer(pcm, np.float32), vad_filter=True, beam_size=1)
            text = " ".join(s.text.strip() for s in segs); f.unlink()
        ts = datetime.date.fromtimestamp(e["timestamp"]).isoformat() if e.get("timestamp") else None
        db.execute("insert or replace into tiktok values (?,?,?,?,?,?,?,?,?,?,?,?)",
                   (e["id"], u, ts, e.get("view_count"), e.get("like_count"), e.get("comment_count"), e.get("repost_count"),
                    e.get("save_count"), e.get("duration"), e.get("description") or e.get("title"), text,
                    datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")))
        db.commit(); print(f"[{n}/{len(queue)}] {u} {e.get('view_count')} {'ok' if text else 'FAIL ' + r.stderr[-120:]}", flush=True)

if __name__ == "__main__":
    main(sys.argv[1:])
