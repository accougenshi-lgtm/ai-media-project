# Research log (dated, sourced takeaways from the 10 AM sessions)

## 2026-11-22
- Baseline research: see docs/STRATEGY.md and docs/tiktok_creator_study.md.
- Narration study (owner's suggestion): 5 transcripts across sleep / scary / informative → docs/narration_study.md.
  Biggest finding: our pace (129 wpm) matches the leaders (131–142), but our length (28 min) is far below theirs (2–2.5 h).

## 2026-11-22: 10 AM session (vidIQ: 25 credits used; 80 left this cycle, resets 2026-12-22)
### Outliers: sleep long-form (vidIQ outliers, last 3 months, channels ≤200K subs)
- Slumber Science (3.3K subs): "100 Weird Psychology Facts to Fall Asleep to — No Adverts", 2:30:44, **221.1K views, 388× breakout**, AI-labeled.
  Same channel: "The Strange Ways Your Mind Works — Psychology for Sleep", 2:21, 15.5K (30×).
- Sleepy Mystery Channel (28.2K): "5 Hours of Mind-Bending Mysteries | Will Make You Sleep", 5:40, 339K; "Uncovering The World's Most Secretive Projects | Bedtime Documentary", 2:47, 113K.
- Stephen Dalton's Humorously Dull History for Sleep (11.2K): "History of the Bicycle is So Boring...You'll Fall Asleep", 3:00, 11.9K in 3 days, **8.2% engagement** (humour wins comments).
- Science Into Sleep (1.5K): "100 Quiet Facts About Places No Human Has Ever Seen", 2:49, 3.1K in 1 day.
- Pattern: **2–3+ hours**, "100 [adjective] facts", "to fall asleep to", humour or mystery angle. Several winners are AI-labeled, so AI narration isn't a blocker.
### Outliers: science what-if Shorts (last 3 months)
- Poly Guy 3D (3.4K): "What If Sound Moved at Walking Speed?" 0:33, **182K (106×)**.
- Technically Unwise (46 subs!): "What If 8 Billion People Jumped on One Trampoline?" 0:29, 31K (23×).
- PeanutFilms (3.1K): "8 billion people on a diving board" 0:47, 453K (41×).
- Theory of Odd (1.5K): "What If You Fell Straight Through Earth?" 0:30, 14K, 6.9% engagement.
- BioChok (7.3K): "What If Earth Spun the Other Way? New York Goes Underwater" 1:35, 1.3M (38×).
- Pattern: **26–47 s**, an absurd but concrete premise in the title, the payoff visual. Our EP001 (72 s) is too long.
### Growth lessons
- **YouTube official** (Creator Insider, "YouTube Algorithm 2026", Todd Beaupré, YouTube Growth & Discovery, rHLjxrbXmmY):
  recommendations are *pulled* per viewer, with no single magic metric (long-term satisfaction + surveys); new channels get matched via topic signals,
  "find some viewers who are interested and then build from there"; don't judge a video in the first hours, since evergreen videos can peak months later;
  long videos are often saved for **TV at night** (good for sleep content); series work on TV because they reduce decision fatigue;
  compare retention against similar-length videos; mixing Shorts and long-form on one channel is fine (the system separates audiences); don't turn off subscriber notifications.
- **Shorts retention** (Deven Seenath, KS4GuYap7gg; sells mentorship, so take with salt): two levers, the 3-second stay rate ("swipe ratio") and
  AVD ÷ length; aim for ≥100% via rewatches/loops. Cycle emotions; don't stack the same emotion twice in a row.
### Decisions
1. Shorts: target **30–40 s**, open on the absurd premise, loopable last line. Re-cut EP001 or replace it.
2. Next sleep video: "100 facts" format, ≥85 min (scaling to 2–3 h as render speed improves), a gentle-humour pass.
3. Keep both formats on one channel (official guidance says this is fine).

## 2026-11-23: 10 AM session (free sources only; 0 vidIQ credits)
- yt-dlp search "facts to fall asleep to space", uploaded this week: 8 new videos from ≥7 channels (Soft Lightyears, What A Wonderful World,
  Curious Minds Official, Space Facts to Fall Asleep To, Mustard Explains, Science Sleep Station, Starlitude Space), 43 min–8 h long, 3–292 views so far.
  → The niche is filling fast with near-identical "Space Facts to Fall Asleep To" titles; new uploads start slowly (evergreen pattern).
- Differentiators seen: **news-pegged sleep titles**, e.g. "What Artemis II Saw Behind the Moon" (292 views, best of the week) and
  "Voyager 1 Reaches One Light-Day"; distinctive series names ("Dragon Galaxy Facts"). Generic titles dominate, so a specific premise stands out.
- Decision: next sleep title gets a specific, timely or unusual premise, not "Space Facts to Fall Asleep To". Clip Shorts can ride news pegs
  (our Voyager clip already says "nearly a full day").
- "what if science shorts" this-week filter returned nothing (search filter quirk); rely on vidIQ outliers (Nov 22) for Shorts.

## 2026-11-24: owner-shared reference (different niche: ocean), "Ocean Trenches: The Abyssal Worlds Humanity Still Cannot Explain"
Underwater Earth 4K (tBjrD_BikTg), published 2026-11-21: **6,420 views, 65 likes, 9 comments at ~3 days, ~97 VPH**, 3:52:52 long (vidIQ).
Speech (speech_stats): 24.4K words, **105 wpm**, median sentence 16 words, almost no "you". Slower than our sleep pace (129).
Why it works: (1) mystery-framed title "…Humanity Still Cannot Explain" + "4K"; (2) opening = title restated → vivid image →
paradox ("These are not empty scars") → open question → welcome + like/sub CTA in minute 1; (3) **recency**: cites research "published in 2026",
named trenches/species/exact depths, which beats generic "calm facts"; (4) long SEO description: emoji bullet per segment, many hashtags, closing comment question.
Apply to space (don't copy): long-form "[Topic]: The [Worlds/Signals] Science Still Can't Explain"-style titles that stay true; a **recent-discoveries segment**
in every sleep video (JWST/2025–26 papers, sourced); slow the sleep voice toward ~110 wpm; description template with emoji chapter bullets + closing question.
- 2026-11-24 10 AM (context-limited): transcript snapshot; next sleep script (Exoplanets, 2–3 h, recent JWST findings, ~110 wpm) still to be written in a fresh-context block.
- 2026-11-25: expert research (Anthropic agent docs, 200-day faceless case study, TikTok corpus) -> docs/expert_notes.md

## 2026-11-25: "Real Questions" harvest -> research/real_questions.json (160 questions, 10 topics)
Method: Agent-Reach 1.6.1 (GitHub release, read-only) `youtube search`, 30 question-phrased queries (3 per topic), 12 results each,
keeping titles that contain "?" (Bowie songs, playlists and kids-compilation noise dropped). Wording is verbatim video titles; `how_popular` = view count
returned by the search at fetch time (null when the search didn't report it). Limits: these are **creator** titles, not viewer comments
(video pages and comments were bot-blocked from the cloud run; vidIQ comments cost 5 credits/call, not spent without owner OK). Reddit not used.
Top 10 for Shorts (biggest demand per topic, plus the strongest conspiracy hooks):
1. "Is Earth Actually Flat?" (38,752,028 views) https://www.youtube.com/watch?v=VNqNnUJVcVs
2. "The Fermi Paradox — Where Are All The Aliens? (1/2)" (35,548,607) https://www.youtube.com/watch?v=sNhhvQGsMEc
3. "What If The Sun Disappeared?" (20,882,039) https://www.youtube.com/watch?v=rltpH6ck2Kc
4. "What If You Fall into a Black Hole?" (19,342,746) https://www.youtube.com/watch?v=QqsLTNkzvaY
5. "Can Humanity Stop A Planet-Killing Asteroid?" (9,734,928) https://www.youtube.com/watch?v=dKm7T13X7n4
6. "Is Our Universe Inside a Black Hole?" (8,902,598) https://www.youtube.com/watch?v=vKeCr-MAyH4
7. "How far can Voyager 1 go before we lose contact?" (6,736,049) https://www.youtube.com/watch?v=aalfNIvQaJ4
8. "Will An Asteroid Hit Earth in 2032?" (4,276,096) https://www.youtube.com/watch?v=_-ZB2Z7VtmE
9. "Why is NASA Worried About Betelgeuse Explosion?" (1,303,277) https://www.youtube.com/watch?v=5f9Kz5GsbDE
10. "Nibiru is real  - Want to see proof?" (815,300) https://www.youtube.com/watch?v=O9na0AhFk54
Also notable: "Why Haven't We Been Back To The Moon In 52 Years?" (375,593, RJKg_moRy5w); "Could CERN Create a Black Hole and Destroy Earth?" (1CIr230a_4E, views not shown).
Next: if the owner approves, pull top viewer comments on 3–5 of these via vidIQ (or yt-dlp on the laptop) to get audience wording rather than creator wording.
