import sqlite3, statistics as st, sys
db = sqlite3.connect("research/research.db")
niches = [r[0] for r in db.execute("select distinct niche from search_results")]
print(f"{'niche':22} {'n':>3} {'median':>9} {'p75':>9} {'>=100k%':>7} {'>=1M':>4} {'chans':>5} {'top1chan%':>9} {'medDur':>6}")
for n in niches:
    rows = db.execute("select views, channel, duration from search_results where niche=? and mode='this_year' and views is not null", (n,)).fetchall()
    rows = list({(r[0], r[1]): r for r in rows}.values())
    v = sorted(r[0] for r in rows)
    if not v: print(f"{n:22} no this-year data"); continue
    chans = {}
    for r in rows: chans[r[1]] = chans.get(r[1], 0) + r[0]
    top = max(chans.values())/sum(v)*100
    durs = [r[2] for r in rows if r[2]]
    print(f"{n:22} {len(v):>3} {int(st.median(v)):>9,} {int(v[int(len(v)*.75)]):>9,} {sum(x>=1e5 for x in v)/len(v)*100:>6.0f}% {sum(x>=1e6 for x in v):>4} {len(chans):>5} {top:>8.0f}% {int(st.median(durs)/60) if durs else 0:>5}m")
