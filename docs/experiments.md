# Experiments & daily lessons log

Format per day: date · what changed · numbers (48h / 7d) · lesson · next change.

## 2026-11-22: Day 1
- Published EP002 (sleep, 28 min, soft dark voice, procedural visuals, original ambient pad).
- Baseline: brand-new channel, 0 subs. Hypothesis: sleep long-form drives watch hours; Shorts drive discovery.
- Lesson learned today: uploads via vidIQ work end to end (video + thumbnail). Wikimedia blocks this server,
  so original procedural visuals are the default asset source.
- Next change: start daily Shorts so the channel has a discovery engine; make sleep videos ≥60 min.
- Incident: first upload (vPvEdJxbaEA) was removed by YouTube "because it was too long": channel was unverified (15-min cap).
  Owner verified the channel; re-posted same video. Lesson: always check verification/limits before long uploads.

## 2026-11-22 10 AM stats (vidIQ)
- 82sf45vCeqM Moon sleep (28:22): **12 views, 1 like, 1 comment** ~8.5 h after publishing. Too early to judge (official guidance: evergreen videos grow over weeks).
- Lesson (writing): 100 facts at ~55 words each = 5.8K words ≈ 50 min. For a 2-hour sleep video, write ~120 words per fact (~12K words).

## 2026-11-22 12 PM create
- Published EP004 Short "The Moon Is Leaving Us (We Measure It With Lasers)", **30.4 s** (first test of the 30–40 s rule), voice `dark`, loop ending.
  Hypothesis: a short, absurd-but-true premise + loop → higher stay rate and AVD/length than a 70 s Short. Compare at 48 h / 7 d.
- Ops lesson: worker restarts kill background renders. Chapter writes are now atomic (.part → rename); the 10 AM/12 PM sessions must check and restart jobs.
- Tool: pipeline/vidiq_upload.sh (resumable upload) replaces pasting vidIQ's long command.
- 2026-11-22 ~13:15 CT: first vidiq_channel_analytics call returned 0 rows for 11/20–11/22 (Studio data lag 1–2 days, not zero views).

## 2026-11-23 (owner: 2 Shorts/day 6 h apart + sleep; schedule ahead; clips allowed)
- Scheduled Short A 09:30 "It May Rain Diamonds on Uranus and Neptune" (4fpv4LcdZJ4, 22.9 s) and Short B 15:30 "Will Andromeda Hit the Milky Way? Maybe Not" (qzlnjNx-9oU, 24.4 s): first **clip Shorts** (calm voice ×1.08) vs EP004's original 30 s what-if. Compare at 72 h.
- EP003 sleep **held back**: blind QA found "Fact N." heard as "Vact" in 7/12 samples (short-line emphasis smears the F). Fixed (colon labels, 3/3 clear), re-rendering; new slot 2026-11-24 21:00.
- Work block 02:23 CT: scheduled 11-24 09:30 clip (YdGlyoar9oo). QA fixes: US/UK spelling false-fails removed; headline cap ≤10 words; captions follow script spelling. EP003 re-render restarted (container reset).
- 2026-11-23 work blocks 06:23/08:23 CT: Voyager clip uploaded + drafted (postId 783bc9cc, slot 11-24 15:30) but vidiq_social_post_publish now needs per-call approval (permission mode changed); BLOCKED, owner notified. QA: years read as pairs (1977), comma-number fix, stray-hyphen captions fixed.
- 16:23 UTC block: EP003 v2 done (43.8 min; labels heard 11/12, was 5/12; loud −18.98 LUFS, motion pass); uploaded + drafted for 11-24 21:00. Both drafts listed in docs/pending_posts.md (publish blocked on approval).

## 2026-11-23 11 AM strategy
- Data: vidiq_channel_analytics (11-21→11-23, by video) = **0 rows** (Studio lag; 2nd day). Channel (vidiq_user_channels, free):
  **2 subscribers** (first subs), 3 public videos, channel viewCount still 0 (stale counter). Last per-video number: EP002 12 views at 8.5 h.
  24 h checkpoint for 82sf45vCeqM not recorded: no per-video data yet (will not estimate).
- Traction: first 2 subs within ~33 h of the first upload. Underperforming: insufficient data.
- Weakness: publishing pipeline depends on a per-call approval that went unanswered twice → 2 finished videos waiting (docs/pending_posts.md).
  Fix: owner asked to "Always allow" vidiq publish or re-enable Auto mode; meanwhile keep producing ahead.
- Plan for the next open slots (11-25 shortA/shortB): shortA = **original what-if Short** "What if all 8 billion people stood in one place?" (idea #5, top-ranked;
  evidence 453K/41× and 31K at 46 subs). shortB = best remaining clip. **Variable tested: original what-if vs clip format** (same slot times, compare 72 h views + APV).
- Analytics budget: skip tomorrow's paid call unless today's Studio data appears in the free channel counter first (save credits during lag).
- 18:23 UTC block (context-limited): made + QA'd clip_venus.mp4 for 11-25 15:30 (WER 3.2%, loud/motion pass); caught + fixed wrong-colour planet (blue → new pale-yellow Venus kind). Not uploaded until publishing is unblocked.
- 20:23 UTC block: Venus clip uploaded + drafted for 11-25 09:30; publish refused: **vidIQ free = 3 YouTube publishes/day** (reset 08:00 UTC). Rule added to DAILY_RUN. Original what-if now targets 11-25 15:30.
- 2026-11-24: owner feedback → retitled 3 Shorts for curiosity gaps (Andromeda now 13 views/1 like pre-change; compare after). Schedules verified intact. Title rule added to DAILY_RUN.
- 02:23 UTC block: rendered EP005 original Short (34.9 s; WER 2.6%, loud/motion pass); fixed caption overflow (auto-fit font). Upload after 08:00 UTC reset.
- Sound design v1 (owner brief): pipeline/sound.py, all-synth stems; EP005 remixed: −14.21 LUFS, WER unchanged 2.6%. Owner ear-check requested (new audio config = allowed SOP escalation).

## 2026-11-24 11 AM strategy
- First Studio rows (11-21→11-24 window, lagged ≈ day 1 only): EP002 Moon sleep **4 views, 3 engaged, 27 min watched, AVD 553 s (9:13), APV 32.5%**. Recorded as its 24 h checkpoint.
  Shorts have no Studio rows yet. Public counters earlier: Andromeda Short 13 views / 1 like. Channel: 2 subs.
- Traction: sleep format holds viewers ~9 min per view on day 1, encouraging for watch hours (N tiny, directional only).
- Weakness: publishing depends on a per-call approval that resets after worker restarts → Wed Shorts stuck. Fix requested: owner sets Auto mode.
- Plan: once unblocked, schedule Venus (Wed 09:30) + EP005v2 black hole (Wed 15:30). Next production: Exoplanets sleep script (2–3 h, recent JWST findings, ~110 wpm). Variable under test: original v2 Short vs clip Shorts.
- 2026-11-24 afternoon: Auto mode on → Venus clip (P7W93AWOSmQ, Wed 09:30) + first short_v2 original (0SmO4YZxau4, Wed 15:30) scheduled. A/B: clip vs original v2, same slot times; compare 72 h views + APV. Fix: short_v2 encode was 124 MB for 17 s (grain) → crf 22 + 12 Mbps cap.
- 2026-11-24 20:23/22:23 CT blocks: made clip_alcohol (Sgr B2, 23.4 s, WER 0, loud/motion pass), drafted for 11-26 09:30; publish call stalled on an approval prompt twice and the worker restarted each time. Kept in pending_posts.md.
- 2026-11-24 20:23 CT block: vidIQ cap reached; rendered clip_sun_mass (21.9 s, WER 3.6%, loud/motion pass) for 11-26 15:30, upload after reset. Metricool connector reports no network linked yet (owner checking).
