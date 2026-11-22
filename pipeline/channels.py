"""For top channels per niche, fetch REAL subs + recent video views. Stores in channel_stats."""
import sqlite3, json, subprocess, statistics as st, datetime
db = sqlite3.connect("research/research.db")
db.execute("CREATE TABLE IF NOT EXISTS channel_stats(fetched_at TEXT, niche TEXT, channel TEXT, channel_id TEXT, subs INT, recent_median INT, recent_max INT, n INT, top_title TEXT, top_views INT)")
now = datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")
NICHES = ["disaster_engineering","dark_history","gaming_patch_math","science_whatif","versus_culture","mystery_unexplained","psychology","business_docs","scifi_original"]
for n in NICHES:
    tops = db.execute("""select channel, channel_id, sum(views) s from (select distinct video_id, channel, channel_id, views from search_results where niche=? and mode='this_year' and views is not null)
                         group by channel_id order by s desc limit 5""", (n,)).fetchall()
    for ch, cid, _ in tops:
        if not cid: continue
        out = subprocess.run(["yt-dlp","--flat-playlist","-J","--playlist-end","20",f"https://www.youtube.com/channel/{cid}/videos"],capture_output=True,text=True,timeout=180).stdout
        try: d = json.loads(out)
        except Exception: continue
        es = [e for e in (d.get("entries") or []) if e and e.get("view_count")]
        if not es: continue
        v = [e["view_count"] for e in es]; best = max(es, key=lambda e: e["view_count"])
        db.execute("insert into channel_stats values (?,?,?,?,?,?,?,?,?,?)",(now,n,ch,cid,d.get("channel_follower_count"),int(st.median(v)),max(v),len(v),best.get("title"),best["view_count"]))
        db.commit(); print(n, ch, d.get("channel_follower_count"), int(st.median(v)), flush=True)
