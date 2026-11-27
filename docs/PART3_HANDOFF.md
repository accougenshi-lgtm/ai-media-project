This is Part 3 of the AI-run YouTube channel project (channel "Orders of significance", id UC8BNoObKWQuks2pzVrpHSbg). Part 2 ran out of context; everything is in this repo.

Start by reading, in order: CLAUDE.md, docs/DAILY_RUN.md (the playbook), docs/pending_posts.md, docs/experiments.md (latest entries at the bottom), docs/research_log.md (latest), docs/sleep_ep009_exoplanets_plan.md. Then run `bash pipeline/setup.sh` and `python3 pipeline/schedule.py need 2`.

State (2026-11-27 ~04:30 UTC):
- Scheduled: Fri 11-27 09:30 EP006 "Will an Asteroid Hit Earth in 2032? ☄️" (5xWsCf1yKso); Fri 15:30 EP007 "You're Moving 1.3 Million km/h Right Now 🌍" (k4kiK-XLHQA). After 09:30 CT confirm both went public (YouTube is blocked from the server; use vidiq_user_channels videoCount or ask the owner).
- DONE 11-27 08:25 UTC: scheduled Sat 11-28 09:30 EP008 as BPbXi4GOKks (1 vidIQ publish used today). Old note: EP008 "A Nearby Star Is Orbiting the Galaxy Backwards ⭐" (vidIQ postId d4088cc1-add2-4398-ad29-29f532266313, revision e16a448d). Publish with vidiq_social_post_publish after 08:00 UTC 11-27 (daily cap reset), then status → schedule.py book → ideas.py video → remove from pending_posts.md.
- Open: Sat 11-28 15:30 Short (planned: "Voyager 1 Is Now One Light-Day From Earth 📡", verify date/distance on NASA JPL first), and every 21:00 sleep slot.
- TOP PRIORITY: the Exoplanets sleep video (2–2.5 h, ~13–16K words, ~110 wpm). Plan + verification list in docs/sleep_ep009_exoplanets_plan.md. Fact-check into docs/factcheck_ep009.md, render with pipeline/sleep_engine.py (voice dark_soft) in the background, QA, schedule for a 21:00 slot. Then a sleep video every 3rd day.
- Shorts pipeline: pipeline/short_v2.py <storyboard.json> <out.mp4> (fixed in Part 2: difflib beat alignment, merged split numbers, counter matches digits, NASA ~orig fallback, HF xet off). QA: qa.py audio/motion/loud + docs/QUALITY.md gate → docs/qc_log.md. Check frames yourself: a NASA ID's image may not match its name (PIA24101 was a diagram, not Bennu).
- Clip Shorts need a rendered sleep episode's output dir (not in a fresh container), so until a sleep video is rendered, make originals.
- Current test: question titles (EP006) vs statement titles (EP007, EP008). Baseline: EP004 190 views, APV 183%. Channel 11-26: 8 subs, 5,664 views, 10 public videos.
- vidIQ: free plan, 3 YouTube publishes/day (reset 08:00 UTC), 0 credits until 12-22 (no per-video analytics; try Metricool getAnalyticsDataByMetrics, free). Metricool brand blogId 8280441 is the backup publisher.
- Rules: owner's standing approval to publish daily; ask before spending money, deleting, or changing anything outside the channel's videos. Never invent numbers. Disclose the AI voice in descriptions. Original/public-domain assets only; log credits in assets/pd/credits.json. Keep messages to the owner short and plain. Watch context headroom: write long scripts in chunks and commit often.

Scheduled tasks (research 10 AM, strategy 11 AM, work block every 2 h at :23, Sunday review) should point at this session. First, say hi to the owner in 2–3 lines, publish EP008 if the cap has reset, then start the Exoplanets sleep script.
