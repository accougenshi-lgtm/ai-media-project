# Daily run playbook (followed by the scheduled sessions)

Owner's standing rules: **post at least one video every day**, learn and improve something every day,
ask the owner only for what is truly needed. The owner has handed over the channel and given standing approval to publish.
Schedule (America/Chicago): **10 AM research → 12 PM create → 1:00 PM video goes public** (scheduled via publishAt).

## Channel
YouTube channel id UC8BNoObKWQuks2pzVrpHSbg (verified; long uploads allowed). Publish via vidIQ:
`vidiq_video_upload` (localFile) → `vidiq_upload_image` (thumbnail) → `vidiq_social_post_draft_create`
(privacyStatus public + publishAt 13:00 America/Chicago) → `vidiq_social_post_publish` → `vidiq_social_post_status`.
vidIQ free plan = 150 credits/month: spend them on research that changes decisions, not on routine checks.

## 10 AM research (no publishing)
1. `bash pipeline/setup.sh`.
2. **Our data:** stats for every published video → `docs/experiments.md` (views, avg view duration, CTR, subs gained).
   Verify yesterday's post is actually public (first upload was silently removed once).
3. **Outside data:** what's breaking out in our niches (vidIQ outliers / trending; `pipeline/research_niches.py`;
   small channels with views ≫ subs). Study 2–3 videos that teach YouTube growth/retention/packaging.
   Write dated, sourced takeaways in `docs/research_log.md`. Never invent numbers.
4. Re-rank `docs/content_queue.md`.
5. If a sleep video is due within 2 days: write + fact-check + start rendering it in the background now.

## 12 PM create
1. `bash pipeline/setup.sh`.
2. Pick today's video from the top of the queue, informed by this morning's notes and past results.
3. Write the script, then **self-critique**: hook in first line? every claim sourced? anything generic/templated? fix it.
   Fact-check into `docs/factcheck_epNNN.md`. Never reuse a previous script's wording.
4. Render (Short: `pipeline/engine.py`, voice `dark`; Sleep: `pipeline/sleep_engine.py`, voice `dark_soft`, ≥60 min target), QA frames + loudness.
5. Thumbnail (long-form) + honest title. Shorts: ≤60-char title with #shorts. Description discloses the AI voice.
6. Upload and **schedule public for 13:00 America/Chicago today**. Confirm the status is scheduled.
7. Commit + push; update queue + experiments; report to the owner in 3–5 lines.

## Formats
- Short (45–75 s, vertical): what-if with real math. Most days.
- Sleep long-form: at least every 3rd day, getting longer (60 → 120 min) as the pipeline speeds up.

## Guardrails
- No misleading titles, reused footage, copyrighted music, or realistic fakes of real events.
- If an upload is refused/removed or something looks risky for the channel, stop and ask the owner.
