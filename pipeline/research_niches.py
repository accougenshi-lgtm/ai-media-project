"""Niche research: pulls REAL observable YouTube search results (via yt-dlp, no API key)
into SQLite so findings are dated and re-checkable. Usage: python pipeline/research_niches.py"""
import json, sqlite3, subprocess, datetime, statistics, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "research" / "research.db"

NICHES = {
    "disaster_engineering": ["engineering disaster explained", "industrial accident documentary", "plane crash investigation explained"],
    "dark_history": ["forgotten history documentary", "strange history events", "history mystery explained"],
    "mystery_unexplained": ["unsolved mystery documentary", "unexplained disappearance explained"],
    "gaming_patch_math": ["patch notes explained math", "weapon changes math breakdown", "hero balance changes analysis"],
    "versus_culture": ["american vs british", "american vs european differences", "country vs country comparison"],
    "science_whatif": ["what if scenario science", "what would happen if earth", "hypothetical science explained"],
    "horror_fiction": ["horror story narration animated", "scary story original fiction narrated"],
    "psychology": ["psychology explained documentary", "human behavior explained"],
    "business_docs": ["how this company collapsed", "business documentary rise and fall"],
    "scifi_original": ["sci fi story narrated original", "animated sci fi short story"],
}

def run(query, n, mode="rel"):
    import urllib.parse
    target = f"ytsearch{n}:{query}" if mode == "rel" else (
        "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query) + "&sp=EgIIBQ%253D%253D")
    cmd = ["yt-dlp", "--flat-playlist", "-J", "--playlist-end", str(n), target]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=180).stdout
    try:
        data = json.loads(out) if out.strip() else None
        return (data or {}).get("entries", []) or []
    except json.JSONDecodeError:
        return []

def main():
    db = sqlite3.connect(DB)
    db.execute("""CREATE TABLE IF NOT EXISTS search_results(
        fetched_at TEXT, niche TEXT, query TEXT, mode TEXT, rank INT, video_id TEXT, title TEXT,
        channel TEXT, channel_id TEXT, views INT, duration INT)""")
    now = datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")
    for niche, queries in NICHES.items():
        for q in queries:
            for mode, n in (("rel", 40), ("this_year", 40)):
                rows = run(q, n, mode)
                for i, e in enumerate(r for r in rows if r):
                    db.execute("INSERT INTO search_results VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        (now, niche, q, mode, i, e.get("id"), e.get("title"), e.get("channel"),
                         e.get("channel_id"), e.get("view_count"), e.get("duration")))
                db.commit()
                print(f"{niche:22} {mode:13} {q[:40]:40} {len(rows)} results", flush=True)
    db.close()

if __name__ == "__main__":
    main()
