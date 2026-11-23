# SOP: Autonomous Calm-Science YouTube Agent (owner-supplied 2026-11-23; adopted with the adaptations below)
The full owner prompt is the reference for: blind QA (§1), visuals & render budget (§2), voice/sound (§3),
data & experiments (§4), audience loop (§5), memory/reliability (§6), 90-day plan (§7), spend/ask gate (§8).

## Implemented
- §1A/C + loudness: `pipeline/qa.py audio|motion|loud` (Whisper small.en WER + number/term check, frame-diff MAD, LUFS/TP). Exit 1 = block.
- §3C targets: Shorts −14 LUFS / −1 dBTP; sleep −19 LUFS / −2 dBTP (sleep_engine updated from −20).
- §4A: log at 24 h, but **no decisions before 72 h**; a change counts only if it beats the 14-day median by ≥25% on 3 consecutive same-format uploads.
- §6C weekly self-review (Sunday) → docs/weekly_review.md (STOP/START/CONTINUE ×3).

## Adapted (and why)
- §1A WER threshold: SOP says ≤2%. Whisper's own error floor on TTS is ~2–4%, so the gate is **≤5% WER AND zero missed numbers/technical terms**.
  Numbers are compared as words (3.8 → "three point eight"); US/UK spelling unified; trailing-silence hallucinations dropped.
- §1B A/V sync ±150 ms: not built yet (needs word timestamps mapped to scene starts). Next tooling task.
- §2C "pure #000000 world": kept black, but stars stay in the world shader (that's where the SOP's §2C star recipe lives).
- §6A "commit every 30 PNG frames to GitHub": **not done**; image sequences would bloat the repo past usable size.
  Frames stay on disk; renders resume by frame/chapter index (atomic .part → rename); only code, scripts and logs go to git.
- §4A N ≥ 1,000 views before trusting a result: kept, so early weeks are logged as directional only.
- §5 comments/pins/playlists/end screens/A-B tests: vidIQ can reply to comments only after the owner grants comment permission (one link);
  pinning, playlists, end screens and Test & Compare have **no tool access here**, so they are queued as a 2-minute owner checklist when needed.
- Publishing time stays 1:00 PM America/Chicago (≥1/day UTC is satisfied).

## Lessons logged
- 2026-11-23: EP004 narration said "twenty two thousand km" while the screen showed 22,800. QA now compares spoken numbers to on-screen numbers.
