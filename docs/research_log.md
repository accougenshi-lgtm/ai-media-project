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
- 2026-11-25 10 AM (context-limited): added 5 Real Questions ideas from research/real_questions.json to ideas DB (CERN, 2032 asteroid, universe-in-black-hole, Moon return, Nibiru).

## 2026-11-26: viewer-worded Real Questions (YouTube comments) -> research/real_questions.json (+29, now 189)
Method: no laptop was connected to the cloud session, so Agent-Reach/yt-dlp couldn't be used (YouTube bot-blocks the cloud). With owner OK we used
vidIQ `vidiq_video_comments` (order=relevance, maxResult=100, 5 credits/call) on the top-viewed video of 7 topics: 35 credits spent, 40 -> 0
(the 8th call, Planet X wy8fi77t8zU, was refused for lack of credits and not charged). 700 top-level threads plus the replies returned were filtered by
script to non-channel-owner comments containing "?" (306), then hand-picked to **genuine questions** (29). Wording is verbatim. The only edits:
HTML entities decoded, `<b>/<i>` tags removed, and a leading "@handle" of the person being replied to dropped. `how_popular` = likeCount as returned.
Reddit not used. **Short of the 60 target**: most "?" comments on these videos are jokes and memes ("Or is it?", "yesn't", Crysis, Pluto), not questions.
Per topic: mars 7 · aliens / fermi paradox 6 · flat earth 6 · voyager 4 · black holes 3 · asteroid impact 3 · sun dying 0 (all 100 threads were jokes)
· not fetched: planet x / nibiru, betelgeuse, moon landing hoax.
Top 10 viewer questions by likes:
1. "…Will we evolve to be smarter? Will we kill each other? Or will we colonize the stars?…" (4,078 likes) https://www.youtube.com/watch?v=sNhhvQGsMEc
2. "I have a question for flat earth theorists. how far down to I have to dig before I fall out of the world? 10m? 1km? 10km??" (1,662) https://www.youtube.com/watch?v=VNqNnUJVcVs
3. "\"Shouldn't the universe be teeming with spaceships?\" Perhaps it is. … how in the hell are we supposed to see a single starship?" (998) https://www.youtube.com/watch?v=sNhhvQGsMEc
4. "How is that even possible though? There's 200 billion to possibly 2 trillion galaxies… Are the odds of intelligent life just that scarce…?" (70) https://www.youtube.com/watch?v=sNhhvQGsMEc
5. "If they can produce a battery that lasts that long, why can't they make batteries that last longer than a couple of months?" (55) https://www.youtube.com/watch?v=aalfNIvQaJ4
6. "What about sealife? Is there anything in the seawater that would survive for any meaningful length of time on mars?" (51) https://www.youtube.com/watch?v=FkUNHhVbQ1Q
7. "Have you tried traveling to the South pole and keep going down there?" (51) https://www.youtube.com/watch?v=VNqNnUJVcVs
8. "What if Galaxies were spinning flat discs wait they are … What if Earth was a spinning gas planet?…" (49) https://www.youtube.com/watch?v=VNqNnUJVcVs
9. "We only have TWO rockets that can holster tungsten projectiles into a planet killing rock?…" (47) https://www.youtube.com/watch?v=dKm7T13X7n4
10. "…how in the hell is it EQUALLY terrifying that we are not alone as opposed to alone?…" (36) https://www.youtube.com/watch?v=sNhhvQGsMEc
Viewer vs creator wording: creator titles are short, clean "What if X?" / "Is X?" hooks. Viewers (a) ask **follow-ups the video skipped**, e.g. how bright an iced Mars would look,
whether white holes send you to the past, why Voyager's power source outlasts phone batteries, whether 2 trillion galaxies make loneliness impossible;
(b) argue in **concrete, physical, often wrong-but-intuitive** terms ("how do we have sea level", "so the moon just follows us?", "dig before I fall out");
(c) put the question at the end of a long ramble, with typos and "?!" stacks; (d) wrap the core question in jokes: the joke dialogue "Are we alone in the Universe?"
got 4,511 likes but isn't logged as a question. Idea: open Shorts with the viewer's concrete objection ("If the Earth is flat, how far down would you dig?"),
then do the math. Follow-up costs (vidIQ credits renew 2026-12-22, or yt-dlp on the laptop): Planet X, Betelgeuse and Moon-hoax comments.

## 2026-11-26: reference channel @cosmoinmotion_001 (owner-shared), Shorts list via yt-dlp flat list (fetched 2026-11-26, rounded public counts)
Top: "Every star you see is dragging its worlds through the galaxy in a spiral" 1.0M; "A star 13 light-years from us is going the wrong way around the Milky Way" 387K;
"Never Sitting Still" 315K; "Voyager 1 is leaving the Sun at 38,000 mph" 116K; "You live inside a giant bubble — and it's under attack right now." 66K; Cartwheel Galaxy 48K;
"How Earth Will End?" 44K; "The oldest things in our galaxy are still flying around it..." 42K; "Nibiru never came, but astronomers really are hunting a hidden planet..." 37K.
Why it works: one theme (cosmic MOTION) = recognisable series; titles are one surprising true statement aimed at "you/us", the claim IS the hook but the
"why/how" stays open; questions underperform statements on this channel (How Earth Will End? 44K vs statement titles up to 1M). Debunk-adjacent framing works
("Nibiru never came, but... real hidden-planet hunt"). Caution: the "spiral/vortex" solar-system idea is often shown wrongly; our version must show the true geometry.
Takeaways for us: (1) build a series identity (e.g. "things moving that you never feel"), (2) test statement-hook titles vs Real Questions, (3) motion visuals > static.

## 2026-11-26 10 AM research (context-limited, one web search)
- News pegs this week (web search 2026-11-26, ScienceDaily/NASA listings; verify each on the primary page before use):
  Voyager 1 nearing one light-day from Earth (NASA, Nov 2026) → added idea "Voyager 1 Is Now One Light-Day From Earth 📡" (Short; ties to the 6.7M-view
  Real Question aalfNIvQaJ4 and the 55-like viewer question about its power source); ESA Euclid's first comet discovery (images 16–24 Sep 2026);
  first of three consecutive supermoons on 24 Nov; a reported large new dwarf-planet candidate beyond Pluto (unverified, do not use until checked).
  Sources: https://www.sciencedaily.com/news/space_time/astronomy/ ; https://science.nasa.gov/solar-system/skywatching/whats-up-november-2026-skywatching-tips-from-nasa/ ;
  https://sciencedaily.com/releases/2026/11/261124055852.htm
- Sleep video is overdue (both 21:00 slots open); plan in docs/sleep_ep009_exoplanets_plan.md, script to be written in a fresh-context session.
