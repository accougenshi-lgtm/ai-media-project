# EP009 sleep plan: "Exoplanets: The Strangest Worlds Science Still Can't Explain" (idea #16), written 2026-11-26
Status: PLAN ONLY. No facts below are verified yet; every number must be sourced into docs/factcheck_ep009.md before scripting.
Format (from EP003 + research_log 2026-11-24): ~110 wpm, 2–2.5 h → ~13,000–16,000 words; ~100 "Fact N:" items at ~120–140 words;
calm intro with CTA in the first minute; gentle humour; a **recent-discoveries chapter** (JWST 2023–2026, sourced); voice `dark_soft`, pipeline/sleep_engine.py.
Do not reuse EP003 wording (EP003 had an exoplanet section: check script.md and avoid repeating those facts).

## Chapters (≈8–10 facts each) and what to verify
1. Settling In: intro, CTA, "you don't need to remember anything".
2. How we find them: transits (Kepler/TESS), wobble (radial velocity, 51 Peg b 1995), direct imaging, microlensing, pulsar planets (1992). Verify: NASA confirmed-exoplanet count + date (NASA Exoplanet Archive).
3. Hot Jupiters: 51 Peg b, WASP-12b (being eaten), WASP-76b (iron rain), HD 189733b (glass rain, blue). Verify each claim + paper.
4. Lava & diamond worlds: 55 Cancri e (JWST atmosphere 2024), K2-141b (rock vapour), CoRoT-7b. Verify; diamond-planet claim is disputed, say so.
5. Puffy & strange: WASP-107b (cotton-candy density, JWST 2024), Kepler-51 "super-puffs", TrES-2b (darker than coal).
6. Many suns: Kepler-16b (Tatooine), circumbinary planets, triple-star systems; PSR B1620-26b (oldest-known planet).
7. The TRAPPIST-1 family: 7 planets, resonances, JWST results on b/c (no thick atmospheres?). Verify latest 2025–26 papers.
8. Nearby neighbours: Proxima b/d, Barnard's Star planets (2024–25 discoveries), Tau Ceti, Epsilon Eridani b.
9. Rogue planets: free-floating planets, JWST JuMBOs in Orion (and the 2024–25 doubts about them), Roman telescope plans.
10. Water worlds & habitability: K2-18b (DMS claim 2025 and the pushback: present as unresolved), LHS 1140b, TOI-270d.
11. Recent discoveries (2025–2026): pick 8–10 from NASA/ESA/JWST press releases dated 2025-2026, each with date + link.
12. Unexplained: radius valley, hot-Neptune desert, why no super-Earth in our system, Planet Nine as the local mystery.
13. Drifting Off: slow closing, no new facts.

## Production notes
- Visuals: sleep_engine paintings (add kinds: lava world, puffy planet, binary sunset, red-dwarf system) + NASA PD illustrations (PIA series), labelled "illustration".
- Thumbnail + title per DAILY_RUN title rule (curiosity gap, true). Long-form: AI-voice disclosure, chapters with emoji bullets, closing question.
- Render takes hours: start in background as soon as chapters 1–6 are written; QA "Fact N" label clarity (EP003 lesson) on 12 samples.
- Then a sleep video every 3rd day; clips (pipeline/clip_short.py) need the rendered output dir, which does not survive container resets: keep the
  episode's chapter WAVs/alignment in output/ only while clipping, or re-render.
