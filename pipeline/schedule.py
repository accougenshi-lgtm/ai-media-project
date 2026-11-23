"""Posting-slot planner (America/Chicago). Never two posts at the same time.
  python pipeline/schedule.py need [days=2]       -> open slots in the next N days (what to produce next)
  python pipeline/schedule.py book <date> <slot> <videoId|uploadId> "<title>"
  python pipeline/schedule.py show [days=7]
Slots: shortA 09:30, shortB 15:30 (6 h apart), sleep 21:00 (sleep videos: target every 2–3 days, daily when ready)."""
import sqlite3, sys, datetime, pathlib
from zoneinfo import ZoneInfo
DB = pathlib.Path(__file__).resolve().parent.parent / "research" / "research.db"; TZ = ZoneInfo("America/Chicago")
SLOTS = {"shortA": "09:30", "shortB": "15:30", "sleep": "21:00"}
SLEEP_EVERY = 1  # minimum days between sleep posts (owner: ultra-long videos alongside 2 Shorts/day)

def db():
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS slots(day TEXT, slot TEXT, ref TEXT, title TEXT, booked_at TEXT, PRIMARY KEY(day, slot))")
    return c

def publish_at(day, slot):
    h, m = map(int, SLOTS[slot].split(":"))
    return datetime.datetime.combine(datetime.date.fromisoformat(day), datetime.time(h, m), TZ).isoformat()

def need(days=2):
    c = db(); now = datetime.datetime.now(TZ); out = []
    booked = {(d, s) for d, s in c.execute("select day, slot from slots")}
    sleep_days = sorted(d for d, s in booked if s == "sleep")
    for i in range(days + 1):
        day = (now.date() + datetime.timedelta(days=i)).isoformat()
        for slot in SLOTS:
            if datetime.datetime.fromisoformat(publish_at(day, slot)) < now + datetime.timedelta(minutes=45): continue  # too late to schedule
            if (day, slot) in booked: continue
            if slot == "sleep":
                last = max([d for d in sleep_days if d <= day], default=None)
                if last and (datetime.date.fromisoformat(day) - datetime.date.fromisoformat(last)).days < SLEEP_EVERY: continue
            out.append((day, slot, publish_at(day, slot)))
    return out

if __name__ == "__main__":
    a = sys.argv[1:] or ["need"]
    if a[0] == "need":
        for d, s, p in need(int(a[1]) if len(a) > 1 else 2): print(f"OPEN {d} {s:6} publishAt={p}")
    elif a[0] == "book":
        c = db(); c.execute("insert into slots values (?,?,?,?,?)", (a[1], a[2], a[3], a[4], datetime.datetime.now(TZ).isoformat(timespec="minutes"))); c.commit()
        print("booked", a[1], a[2], publish_at(a[1], a[2]))
    elif a[0] == "show":
        for r in db().execute("select * from slots order by day, slot"): print(r)
