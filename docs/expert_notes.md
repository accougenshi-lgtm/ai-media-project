# Expert notes: how high-level AI users run long autonomous work (2026-11-25)
Sources (fetched 2026-11-25): Anthropic Engineering "Building effective agents" (BEA), "Effective harnesses for long-running agents" (EH),
Claude Code best practices (code.claude.com/docs/en/best-practices, CCBP); vidIQ transcript of mJld3pDws_c "I tried Faceless YouTube
Automation for 200 days" (Darragh Lucey, 911K views); our TikTok corpus (1,043 transcripts, research/tiktok). YouTube captions via yt-dlp
were bot-blocked; simonwillison.net, karpathy.bearblog.dev, support.google.com not on the network allowlist (not read).

## Agent operations (Anthropic)
- Simplest thing that works; scripted workflows for predictable steps, agent judgment only where steps can't be predicted (BEA). Our pipeline already fits this.
- Each step needs ground truth from the environment and pass/fail checks (BEA, CCBP). We have qa.py; keep every gate machine-checkable.
- Long-running harness: progress file + machine-readable task list (JSON; agents edit JSON less destructively than Markdown),
  start every session by reading git log + progress, run a smoke check, do ONE unit of work, end clean with a commit (EH).
  -> Adopt docs/STATE.json (open slots, pending drafts, in-flight renders) read first in every session.
- Use a fresh-context reviewer for verification and demand evidence (CCBP). -> Score QUALITY.md with a separate reviewer pass, not the maker.
- Keep CLAUDE.md short; rules that must never break belong in hooks/permission rules, not prose (CCBP).
  -> Our publish stalls are a permission prompt problem; fix is an allow rule for the vidIQ publish tool (owner decision).
- Pilot before scaling batch work (CCBP).

## Channel strategy (200-day faceless case study)
- Two early viral videos, then 6+ flops despite higher quality: they chased trends/new viewers instead of serving the audience they had.
- "A great idea and poor execution will do better than a poor idea with great execution." Idea/topic choice > polish.
- Ship good-enough to test; a month perfecting one video was the biggest waste. Strict deadlines. One niche, no shiny objects.
- Value is a recurring audience (built for one avatar), not one-time views. Think profit, not revenue.

## TikTok corpus (sina.growthtech top videos)
- Top views (1.3M) are conspiracy-claim hooks and brand-new-tool news, not tutorials -> supports our "Real Questions" format
  (take the viral claim seriously, then reveal the real science).
