# Quality standard & QC gate (adopted 2026-11-22 from the owner's animation brief)

Every video is inspected **after rendering**: contact-sheet frames at every scene change, the first 3 s and last 3 s,
loudness (`volumedetect`), duration/format (`ffprobe`), and a read-through of captions against the fact check.
Score 1–10 and log it in `docs/qc_log.md`.

| Category | What "8+" means for us |
|---|---|
| Visual quality | Looks deliberate and premium on a phone; no flat placeholder art |
| Animation | Real motion (camera moves, parallax, 3D); never a still image with a zoom |
| Consistency | Same objects/characters keep their look and proportions across shots |
| Storytelling | Hook → escalation → payoff; understandable on first watch |
| Retention | No dead stretch > 3 s (Shorts) / no repetitive module (sleep) |
| Audio | Clear voice, consistent level (Shorts −14 LUFS, sleep −20), no clipping |
| Editing | Cuts/transitions on purpose, pacing matches the narration |
| Originality | Script, math and visuals are ours; not interchangeable with other channels |
| Technical | Correct resolution/aspect, no artefacts, full length, captions in sync |
| Policy & copyright | Licensed/self-made assets only, facts sourced, advertiser-friendly |

## Gate
- **Hard blockers (any failure = do not publish):** copyright, factual error, technical defect, policy/safety.
- **Craft categories:** target **8+**. Publishing floor **6** while the animation pipeline is being upgraded, because the owner's
  "post once a day" rule comes first. The floor rises to 7 once Blender hero shots are routine, and to 8 when every category
  reaches 8 on 5 consecutive videos.
- Fix loop: name the defect → smallest fix → re-inspect that section → one final full check. **Max 2 fix attempts per defective shot.**
- If a video can't pass, try one alternative concept; if that fails, report the blocker to the owner rather than posting filler.

## Honest baseline (videos already published)
| Video | Visual | Anim | Consist. | Story | Retention | Audio | Editing | Orig. | Tech | Policy |
|---|---|---|---|---|---|---|---|---|---|---|
| EP002 Moon sleep | 6 | 4 (slow pan on stills) | 8 | 7 | 7 | 7 | 6 | 8 | 8 | 9 |
| EP004 Moon leaving (Short) | 5 | 5 (2D motion graphics) | 8 | 7 | 7 | 6 (no music/SFX) | 6 | 7 | 8 | 9 |
Weakest areas: **animation and visual quality**, then **audio** (no SFX/music in Shorts).

## Upgrade roadmap (free tools only)
1. **Blender 3D hero shots** (installed 2026-11-22, `pipeline/blender/space_shot.py`): Cycles on CPU ≈ 12 s/frame at 540×960
   while sharing the CPU → a 4 s shot ≈ 20 min. Plan 1–2 hero shots per Short, rendered ahead in the 10 AM session.
   Next: a proper day/night terminator, a moon variant, camera paths (orbit, flyby, push-in).
2. **2D engine upgrades:** parallax star layers, eased camera moves, whip/crossfade transitions, kinetic typography.
3. **Sound design:** synthesized whooshes, impact hits, a subtle music bed for Shorts (original, generated with ffmpeg).
4. **Brand element:** one recurring visual signature (an "amber measuring line" that draws the key number every video).
5. Paid AI video (Higgsfield has 8 free credits ≈ 1 clip): only with the owner's OK, and only if a test clip clearly beats Blender.
