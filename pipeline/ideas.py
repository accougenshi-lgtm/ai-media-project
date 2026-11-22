"""Idea database + per-video performance tracker (SQLite, research/research.db).

Ideas:   python pipeline/ideas.py add "<title>" <format short|sleep> "<evidence + link>" demand originality feasibility appeal
         python pipeline/ideas.py rank            # ranked list of open ideas (score = weighted 1-5 ratings)
         python pipeline/ideas.py used <id> <videoId>
Videos:  python pipeline/ideas.py video <videoId> <format> "<title>" <published_iso> <length_s>
         python pipeline/ideas.py check <videoId> <24h|72h|7d> views=.. engaged=.. minutes=.. avd=.. avp=.. subs=.. likes=.. comments=..
         python pipeline/ideas.py due             # which 24h/72h/7d checks are due now
         python pipeline/ideas.py report          # every video with its checkpoints vs channel baseline
"""
import sqlite3, sys, datetime, pathlib, statistics as st
DB = pathlib.Path(__file__).resolve().parent.parent / "research" / "research.db"
W = dict(demand=0.35, originality=0.25, feasibility=0.2, appeal=0.2)

def db():
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS ideas(id INTEGER PRIMARY KEY, added TEXT, title TEXT, format TEXT, evidence TEXT,
                 demand INT, originality INT, feasibility INT, appeal INT, status TEXT DEFAULT 'open', video_id TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS videos(video_id TEXT PRIMARY KEY, format TEXT, title TEXT, published TEXT, length_s INT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS checks(video_id TEXT, checkpoint TEXT, fetched_at TEXT, views INT, engaged INT, minutes REAL,
                 avd REAL, avp REAL, subs INT, likes INT, comments INT, PRIMARY KEY(video_id, checkpoint))""")
    return c

def now(): return datetime.datetime.now(datetime.UTC)
def score(r): return round(sum(W[k] * r[k] for k in W), 2)

def main(a):
    c = db(); cmd = a[0] if a else "rank"
    if cmd == "add":
        t, f, ev, d, o, fe, ap = a[1:8]
        c.execute("insert into ideas(added,title,format,evidence,demand,originality,feasibility,appeal) values (?,?,?,?,?,?,?,?)",
                  (now().date().isoformat(), t, f, ev, int(d), int(o), int(fe), int(ap))); c.commit(); print("added")
    elif cmd == "rank":
        rows = c.execute("select id,title,format,evidence,demand,originality,feasibility,appeal from ideas where status='open'").fetchall()
        rows = sorted(rows, key=lambda r: -score(dict(zip(["id","t","f","e"] + list(W), r))))
        for r in rows:
            d = dict(zip(["id", "t", "f", "e"] + list(W), r))
            print(f"{score(d):4}  #{d['id']:<3} [{d['f']}] {d['t']}  | {d['e'][:90]}")
    elif cmd == "used":
        c.execute("update ideas set status='used', video_id=? where id=?", (a[2], int(a[1]))); c.commit()
    elif cmd == "video":
        c.execute("insert or replace into videos values (?,?,?,?,?)", (a[1], a[2], a[3], a[4], int(a[5]))); c.commit()
    elif cmd == "check":
        kv = dict(x.split("=") for x in a[3:])
        c.execute("insert or replace into checks values (?,?,?,?,?,?,?,?,?,?,?)", (a[1], a[2], now().isoformat(timespec="minutes"),
                  *(kv.get(k) for k in ["views", "engaged", "minutes", "avd", "avp", "subs", "likes", "comments"]))); c.commit()
    elif cmd == "due":
        for vid, title, pub in c.execute("select video_id,title,published from videos"):
            age = (now() - datetime.datetime.fromisoformat(pub)).total_seconds() / 3600
            have = {r[0] for r in c.execute("select checkpoint from checks where video_id=?", (vid,))}
            for cp, h in [("24h", 24), ("72h", 72), ("7d", 168)]:
                if age >= h and cp not in have: print(f"DUE {cp:4} {vid} ({age:.0f} h old) {title}")
    elif cmd == "report":
        for fmt in ["short", "sleep"]:
            print(f"== {fmt}")
            for cp in ["24h", "72h", "7d"]:
                rows = c.execute("select c.video_id,v.title,c.views,c.avd,c.avp,c.subs from checks c join videos v using(video_id) where v.format=? and c.checkpoint=?", (fmt, cp)).fetchall()
                if not rows: continue
                base = st.median([r[2] or 0 for r in rows])
                for r in rows:
                    print(f"  {cp:4} {r[0]} views={r[2]} ({(r[2] or 0) / base if base else 0:.1f}x median) avd={r[3]}s avp={r[4]}% subs={r[5]} | {r[1][:50]}")
if __name__ == "__main__":
    main(sys.argv[1:])
