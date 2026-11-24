# Daily run playbook (followed by the scheduled sessions)

Owner's standing rules: **post at least one video every day**, learn and improve something every day,
ask the owner only for what is truly needed. The owner has handed over the channel and given standing approval to publish.
Schedule (America/Chicago), owner update 2026-11-23: **work ahead and schedule**. Posting slots (never two at once):
**Short A 09:30 · Short B 15:30 (6 h apart) · Sleep 21:00** (ultra-long; whenever a render is ready, min 1 day apart).
Sessions: 10 AM research · 11 AM strategy · **work block every 2 h at :23** (fills open slots up to 48 h ahead, else learns) · Sunday weekly review.
Planner: `pipeline/schedule.py need|book|show`. Clip Shorts from our own sleep videos: `pipeline/clip_short.py rank|make` (owner OK'd clipping).
Full brief: `docs/MISSION.md`; SOP + adaptations: `docs/SOP.md`. Idea database + per-video tracker: `pipeline/ideas.py` (tables ideas / videos / checks).

## vidIQ credit budget (free plan: 150 per month, resets on the 22nd)
- 11 AM: **one** `vidiq_channel_analytics` call per day (dimension video: views, engagedViews, minutes, AVD, AVP, subs, likes, comments) covers every 24 h/72 h/7 d check. 5 credits.
- Retention curve (`report: audience_retention`): only for a video worth diagnosing, at most 2 per week.
- Research: free sources first (yt-dlp search, web). vidIQ outliers/transcripts at most about 3 per day.
- Studio data lags 1–2 days; empty rows ≠ zero views. Swipe-away rate and CTR need the vidIQ browser extension (not available here).
- If credits run low before the reset, tell the owner (vidIQ Boost may be worth it once data justifies; ask before any spend).

## Channel
YouTube channel id UC8BNoObKWQuks2pzVrpHSbg (verified; long uploads allowed). Publish via vidIQ:
`vidiq_video_upload` (localFile) → `vidiq_upload_image` (thumbnail) → `vidiq_social_post_draft_create`
(privacyStatus public + publishAt 13:00 America/Chicago) → `vidiq_social_post_publish` → `vidiq_social_post_status`.
**vidIQ free plan: max 3 YouTube uploads (publishes) per day, reset at midnight Pacific (08:00 UTC)**, which fits 2 Shorts + 1 sleep/day exactly; never use more than 3 publishes in one Pacific day. vidIQ free plan = 150 credits/month: spend them on research that changes decisions, not on routine checks.

## 10 AM research (no publishing)
1. `bash pipeline/setup.sh`. If the TikTok transcriber isn't running and isn't finished, restart it
   (`HF_HUB_DISABLE_XET=1 nohup python3 pipeline/tiktok_transcribe.py blakeryan052 sina.growthtech &`);
   snapshot progress with `sqlite3 .backup` into `research/tiktok/tiktok_snapshot.db` and commit it.
2. **Our data:** stats for every published video → `docs/experiments.md` (views, avg view duration, CTR, subs gained).
   Verify yesterday's post is actually public (first upload was silently removed once).
3. **Outside data:** what's breaking out in our niches (vidIQ outliers / trending; `pipeline/research_niches.py`;
   small channels with views ≫ subs). Study 2–3 videos that teach YouTube growth/retention/packaging.
   Write dated, sourced takeaways in `docs/research_log.md`. Never invent numbers.
4. Re-rank `docs/content_queue.md`.
5. Pre-render tomorrow's Blender hero shot(s) in the background (pipeline/blender/space_shot.py).
6. If a sleep video is due within 2 days: write + fact-check + start rendering it in the background now.

## 11 AM strategy & development
1. `python3 pipeline/ideas.py due`, then one analytics call → record each due checkpoint with `ideas.py check`; `ideas.py report` vs baseline.
2. Track the 14-day median views per upload vs the owner's investment trigger (~2,000/video, see docs/SOP.md).
   Name what is gaining traction and what is underperforming; log one concrete weakness + fix in `docs/experiments.md`.
3. `ideas.py rank`; pick today's video by expected performance, originality, feasibility, appeal; write a short production plan in `docs/experiments.md`.
4. Keep ≥1 controlled variable per day (hook style, length, voice, structure) and record the hypothesis.

## 2-hour work blocks (production)
Fill the earliest open slot from `schedule.py need 2`; the steps below apply to every video produced.

## Production steps
1. `bash pipeline/setup.sh`.
2. Pick today's video from the top of the queue, informed by this morning's notes and past results.
3. Write the script following the rules in `docs/narration_study.md`, then **self-critique**: hook in first line? every claim sourced? anything generic/templated? fix it.
   Fact-check into `docs/factcheck_epNNN.md`. Never reuse a previous script's wording.
4. Plan shots first (storyboard list in the episode file: which shots are Blender hero shots, which are 2D). Render (Short: `pipeline/engine.py`, voice `dark`; Sleep: `pipeline/sleep_engine.py`, voice `dark_soft`, ≥60 min target), QA frames + loudness.
4a. **Original Shorts now use `pipeline/short_v2.py <storyboard.json> <out.mp4>`** (validator + real NASA media + word-synced captions + 5-stem mix). See docs/CHANGELOG_shorts_v2.md.
4b. **Sound design (owner Audio Director brief, 2026-11-24):** after render, `python3 pipeline/sound.py <work_dir> <dry.mp4> <final.mp4> --key <K> --reveals <scene idx> --pops <idx>`.
   All sounds synthesized (no third-party assets); bed locked to the video's key, ducked ~8 dB under VO; whoosh on cuts; riser cut ~50 ms before impacts on reveals (≥3.5 s apart); micro-pops pitch-varied ±3 st. Manifest saved as audio_manifest.json.
5. **Blind QA (must pass):** `python3 pipeline/qa.py audio <mp4> <script>`, `qa.py motion <mp4> short|sleep`, `qa.py loud <mp4> short|sleep`.
   Spoken numbers must match on-screen numbers. Fix only the failing line/shot.
   **QC gate per docs/QUALITY.md**: score all 10 categories into docs/qc_log.md; hard blockers stop publishing; max 2 fixes per defective shot.
6. Thumbnail (long-form) + title per the **Title rule** (owner, 2026-11-24): open a curiosity gap and never answer it in the title
   ("Will Andromeda hit us? Maybe not" = bad, answers itself). Provocative and emotional is fine, one emoji OK, but it must stay TRUE:
   no fake doom ("this new galaxy could end us all" is false; Andromeda isn't new and wouldn't hurt us) because misleading titles break YouTube policy and advertiser suitability.
   Good: "Our Galaxy Is on a Collision Course 😳", "We Can Still Talk to Something 24 Billion km Away 📡".
   Owner refinement (2026-11-24): dramatic QUESTIONS are fine when the video takes that exact question seriously and answers it honestly
   ("Is a Black Hole Screaming at Us? 😱" → yes, Perseus' pressure waves = a B-flat 57 octaves below middle C).
   **"Real Questions" format:** harvest dramatic questions people actually ask (conspiracy/forum/comment/autocomplete phrasing),
   use the question as the title, open by taking it seriously, then reveal the real science, which is often stranger than the theory. Cite where the question came from in research_log. Shorts: ≤60-char title with #shorts. Description discloses the AI voice.
6. Upload and **schedule public for 13:00 America/Chicago today**. Confirm the status is scheduled.
7. `ideas.py used <id> <videoId>`, `ideas.py video ...`; add a row to `docs/creative_log.md`.
8. Verify the upload succeeded (`vidiq_social_post_status`, then `vidiq_user_videos` after 1 PM).
9. Commit + push; report to the owner in 3–5 lines.

## Formats
- Short (45–75 s, vertical): what-if with real math. Most days.
- Sleep long-form: at least every 3rd day, target 90–150 min (top competitors run 2–2.5 h), rendered ahead in the 10 AM session.

## Guardrails
- No misleading titles, reused footage, copyrighted music, or realistic fakes of real events.
- If an upload is refused/removed or something looks risky for the channel, stop and ask the owner.
