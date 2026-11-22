# Daily run playbook (followed by the scheduled daily task)

Owner's standing rules: **post at least one video every day**, learn and improve something every day,
ask the owner for anything needed. Owner granted standing approval to publish to the channel.

## Channel
YouTube `@desecrated-you` (channel id UC8BNoObKWQuks2pzVrpHSbg), published via the vidIQ connector
(`vidiq_social_account_list` → `vidiq_video_upload` localFile → `vidiq_upload_image` → `vidiq_social_post_draft_create` → `vidiq_social_post_publish`).

## Every day
1. `bash pipeline/setup.sh` (fresh containers lose models/deps).
2. **Learn:** pull stats for every published video (`vidiq_user_videos` / `vidiq_video_stats`), log them in `docs/experiments.md`
   (views, avg view duration, CTR when available). Write one concrete lesson + one change for today.
3. **Make today's video**, alternating formats per `docs/content_queue.md`:
   - Short (what-if with real math, 45–75 s, vertical, voice `dark`) via `pipeline/engine.py`, or
   - Sleep long-form (voice `dark_soft`) via `pipeline/sleep_engine.py`, at least 1 every 3 days, getting longer (target 60–120 min).
   Fact-check every claim into `docs/factcheck_epNNN.md`. Never repeat a script or template wording.
4. QA: contact-sheet frames, loudness check, title/thumbnail honest and readable.
5. Publish (public). Shorts: title ≤ 60 chars + `#shorts`. Disclose AI voice in description.
6. Commit + push everything; update `docs/experiments.md` and `docs/content_queue.md`.
7. Report to the owner in 3–5 lines: what was posted (link), numbers so far, what was learned, anything needed.

## Guardrails
- No misleading titles, no reused footage, no copyrighted music, no realistic fakes of real events.
- If an upload is refused or something looks risky to the channel, stop and ask the owner.
