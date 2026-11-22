# Daily run playbook (followed by the scheduled sessions)

Owner's standing rules: **post at least one video every day**, learn and improve something every day,
ask the owner only for what is truly needed. The owner has handed over the channel and given standing approval to publish.
Schedule (America/Chicago): **10 AM research → 11 AM strategy → 12 PM produce → 1:00 PM public** (scheduled via publishAt).
Full brief: `docs/MISSION.md`. Idea database + per-video tracker: `pipeline/ideas.py` (tables ideas / videos / checks).

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
vidIQ free plan = 150 credits/month: spend them on research that changes decisions, not on routine checks.

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
2. Name what is gaining traction and what is underperforming; log one concrete weakness + fix in `docs/experiments.md`.
3. `ideas.py rank`; pick today's video by expected performance, originality, feasibility, appeal; write a short production plan in `docs/experiments.md`.
4. Keep ≥1 controlled variable per day (hook style, length, voice, structure) and record the hypothesis.

## 12 PM create
1. `bash pipeline/setup.sh`.
2. Pick today's video from the top of the queue, informed by this morning's notes and past results.
3. Write the script following the rules in `docs/narration_study.md`, then **self-critique**: hook in first line? every claim sourced? anything generic/templated? fix it.
   Fact-check into `docs/factcheck_epNNN.md`. Never reuse a previous script's wording.
4. Plan shots first (storyboard list in the episode file: which shots are Blender hero shots, which are 2D). Render (Short: `pipeline/engine.py`, voice `dark`; Sleep: `pipeline/sleep_engine.py`, voice `dark_soft`, ≥60 min target), QA frames + loudness.
5. **QC gate per docs/QUALITY.md**: score all 10 categories into docs/qc_log.md; hard blockers stop publishing; max 2 fixes per defective shot.
6. Thumbnail (long-form) + honest title. Shorts: ≤60-char title with #shorts. Description discloses the AI voice.
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
