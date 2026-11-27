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
- 2026-11-25: Metricool connected as backup publisher (20/month free). Best-time data supports 09:30/15:30 slots.
- 2026-11-25 02:23–06:23 CT blocks: Sun clip uploaded + drafted for 11-26 15:30; publish stalled on approval 3× in unattended runs even with .claude/settings.json allow rule (cloud auto mode still asks for outward actions). Publishes only succeed when the owner is present.

## 2026-11-25 11 AM strategy
- Studio (11-21→11-25, lagged ~1-2 days; one call, 5 credits): **EP004 Moon Leaving Short (30.4 s, original what-if, loop ending): 190 views, 71 engaged, 70 min, AVD 56 s, APV 182.6%, 3 likes.**
  EP002 Moon sleep: 40 views, 28 engaged, 202 min, AVD 7:07, APV 25.1%, 1 sub, 1 comment. Newer Shorts: no Studio rows yet (lag).
- Traction: the loop ending works: APV 183% means the average viewer watched the 30 s Short ~1.8 times. Original what-if + loop is our best format so far.
- Underperforming: sleep video discovery (40 views in ~3 days), though watch time per view is strong (7 min).
- Weakness: unattended publishes stall on approval prompts (Sun clip waiting). Fix: publish while the owner is present; keep 1-2 days of buffer.
- Plan: next original Short = "Will an Asteroid Hit Earth in 2032?" (idea #18, Real Question, 4.3M-view demand) built with short_v2, ~30 s, loop ending.
  Variable tested: Real Questions title (question) vs statement titles, same length/loop structure. Verify 2024 YR4 latest impact odds (NASA CNEOS / ESA) before scripting.
- 2026-11-26: vidIQ credits exhausted (0 left until 12-22 reset); paid vidIQ tools unavailable, use free tools + web search. Owner shared reference channel @cosmoinmotion_001.
- 2026-11-26 work blocks: scheduled Fri 11-27 09:30 EP006 "Will an Asteroid Hit Earth in 2032? ☄️" (5xWsCf1yKso, 25.3 s, question title) and 15:30 EP007 "You're Moving 1.3 Million km/h Right Now 🌍" (k4kiK-XLHQA, 27.5 s, statement title).
  **Variable tested: Real Question title vs statement title** (both original short_v2 Shorts with loop endings, similar length); compare 72 h views + APV, baseline EP004 190 views / APV 183%.
  Pipeline fixes: beat alignment by normalized word matching (old word-count method drifted ~1 s when Whisper wrote numbers as digits), split-number captions merged, qa.norm handles "%" and "seventeen hundred", NASA ~orig fallback, HF xet off, opencv+jiwer in setup. vidIQ publishes today: 3/3 used (Sun clip + these two).
  Open: no sleep render ready for tonight's or Friday's 21:00 slot (Exoplanets sleep script still not written).
- 2026-11-26 14:23 UTC block (context-limited): wrote docs/sleep_ep009_exoplanets_plan.md (13 chapters, verification list). Next blocks: fill Sat 11-28 15:30 Short; publish EP008 draft after 08:00 UTC 11-27; then Exoplanets script chapters 1–6 in a fresh-context session and start the render.

## 2026-11-26 11 AM strategy (context-limited; vidIQ credits 0 → no per-video analytics)
- Free channel counter (vidiq_user_channels, 2026-11-26 16:53 UTC): **8 subscribers, 5,664 channel views, 10 public videos** (was 2 subs / counter 0 on 11-23).
  Per-video 24h/72h checkpoints due for 8 videos (ideas.py due) **not recorded**: no per-video data without credits; not estimating.
- Traction: subs 2 → 8 in 3 days; channel views 5,664 total (cannot attribute per video). Best known per-video result still EP004 (190 views, APV 183%, 11-25 data).
- Underperforming / unknown: everything since 11-24 lacks per-video numbers until credits renew 12-22 (or the owner checks Studio).
- Weakness: no way to measure per-video results for ~4 weeks → A/B tests can't be read. Fix: ask owner for a weekly Studio screenshot/CSV (free), or
  Metricool analytics (getAnalyticsDataByMetrics, free plan) — try it next strategy session.
- Plan for the next open Short (Sat 11-28 15:30): "Voyager 1 Is Now One Light-Day From Earth 📡" (idea added today; news peg + 6.7M-view Real Question demand),
  short_v2, ~30 s, statement title, loop ending. Verify date/distance on NASA JPL first. Variable still under test: statement vs question titles
  (EP006 question, EP007/EP008/this statement). Sleep video (Exoplanets) remains top priority for a fresh-context session.

## 2026-11-27 11 AM strategy
- Data (vidiq_user_channels, free, fetched 2026-11-27 16:53 UTC): **10 subs, 6,511 views, 12 videos**. Change since 11-26: +2 subs, +847 views, +2 videos (EP006 asteroid went public at 09:30 CT; the second is most likely DheBD0PdbKA or a count lag; not verified). EP007 is still scheduled for 15:30 CT.
- 12 checkpoints are due (24h/72h for 4fpv4LcdZJ4, qzlnjNx-9oU, YdGlyoar9oo, ehqacZVfdMQ, -BlXAL_div4, P7W93AWOSmQ, 0SmO4YZxau4, DheBD0PdbKA, pSZKjWZYPZM). **None recorded**: vidIQ credits are 0 until 12-22, YouTube is blocked from the server, and Metricool analytics were not tried this session. No per-video numbers are invented.
- Traction: the channel is growing about 850 views a day with no per-video split. I can't say which video is driving it.
- Weakness: per-video measurement is blind, so the title test (question vs statement) can't be scored. **Fix:** in Part 3, try Metricool getAnalyticsDataByMetrics (free) for YouTube per-video views first, or ask the owner for a Studio screenshot of the last 7 days.
- Today's video: idea #24 "Voyager 1 Is Now One Light-Day From Earth 📡" (rank 4.55, top), EP010 storyboard written 11-27 for Sat 11-28 15:30.
  - Overlap risk: clip Short ehqacZVfdMQ "Voyager 1 Is 24 Billion km Away and Still Listening" went out 11-24 15:30. EP010 uses a different angle (the light-day milestone, the 2-day reply time, 18,000 days, Pale Blue Dot) and different visuals. It must not reuse EP003 fact 35 wording.
  - The old "Still Listening" title may now be shaky because of the Oct comms pause. Leave it; don't repeat that claim.
  - Variable under test: statement title (same arm as EP007 and EP008). No other change to the format.
