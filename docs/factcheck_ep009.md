# Fact-check EP009 sleep "Exoplanets" (plan: docs/sleep_ep009_exoplanets_plan.md), started 2026-11-28
Built in chunks; every fact used in the script must have a row here. Status: chapter 2 started.

## Ch 2 — How we find them
| Claim | Source | Note |
|---|---|---|
| More than 6,000 confirmed exoplanets | NASA passed 6,000 in Sept 2025 (Scientific American: 6,007); the Exoplanet Archive 2025 news page later lists 6,065 https://exoplanetarchive.ipac.caltech.edu/docs/2025news.html ; IPAC https://www.ipac.caltech.edu/news/the-nasa-exoplanet-archive-hits-6-000-planets | Script: "more than six thousand". Live count not fetched (check exoplanetarchive counts page before render). |
| A planet needs confirmation and peer-reviewed publication to be listed | Exoplanet Archive criteria (via search, 2026-11-28) | |
| First confirmed exoplanets: two planets around pulsar PSR B1257+12, Wolszczan & Frail, Nature, 9 Jan 1992, Arecibo, found from pulse-timing irregularities | NASA "Will the real first exoplanet please stand up" https://science.nasa.gov/universe/exoplanets/will-the-real-first-exoplanet-please-stand-up ; Space.com https://www.space.com/35253-exoplanet-discovery-anniversary-25-years.html | Third planet came ~1994 (sources differ on the exact year: don't date it) |
| 51 Pegasi b: first planet around a Sun-like star, Mayor & Queloz (Geneva), announced 6 Oct 1995, radial velocity; 2019 Nobel Prize | NASA (same page); Live Science https://www.livescience.com/how-nobel-winning-alien-planet-found.html | |
| ~6,350 confirmed by late Aug 2026 | EarthSky (2026) https://earthsky.org/space/how-do-astronomers-discover-exoplanets | Supersedes 6,065; script still says "more than six thousand" (safe floor) |
| About three quarters were found by the transit method (Kepler, TESS) | EarthSky 2026 (same); per-method tables in secondary sources (e.g. jcrass.space citing the Exoplanet Archive: transit ~4,650) | Say "about three in four". Check archive counts page before render |
| Radial velocity is 2nd (~1,100); microlensing ~200–280; direct imaging fewer than ~100 | arXiv:2404.09143 table; jcrass.space table | Numbers differ by date → script uses only "a few hundred" / "fewer than a hundred" |
| Microlensing planets are often seen only once; Roman telescope expected to find many more | EarthSky/secondary | Verify Roman numbers on NASA before use |

## Ch 3 — Hot Jupiters (in progress)
| Claim | Source | Note |
|---|---|---|
| WASP-76b, ~640 light-years away: iron vaporises on the dayside, winds carry it to the night side, where it condenses (iron "rain") | ESPRESSO/VLT, Ehrenreich et al., Nature 2020; Scientific American https://www.scientificamerican.com/article/molten-iron-rain-falls-on-scorching-hot-exoplanet/ ; Space.com https://space.com/alien-planet-iron-rain-WASP-76b.html | Say "likely rains iron" (it is inferred from spectra, not seen) |
| HD 189733b, ~63 light-years: Hubble measured its colour as deep blue (July 2013, the first measured exoplanet colour); the blue comes from a hazy sky with high silicate clouds, not oceans; it may rain glass sideways in ~4,500 mph (~7,000 km/h) winds; dayside ~2,000 °F (~1,100 °C) | NASA "Hubble finds a true blue planet" https://science.nasa.gov/missions/hubble/nasa-hubble-finds-a-true-blue-planet/ ; Scientific American blog 2013 | Wind is "about seven thousand km/h" (do NOT use 5,400 mph). Say "may rain glass" |
| WASP-12b is spiralling into its star: its year shortens by ~29 ms every year; about 3 million years left (decay timescale 3.25 ± 0.23 Myr) | Yee et al. 2020, ApJL 888 L5 https://iopscience.iop.org/article/10.3847/2041-8213/ab5c16/ ; Princeton release 2020-01-07 https://www.princeton.edu/news/2020/01/07/planet-wasp-12b-death-spiral-say-scientists ; TESS update −29.81 ± 0.94 ms/yr arXiv:2201.08370 | "about three million years" is a timescale, not a date; why it decays this fast is debated (arXiv:2609.11925) — say "astronomers aren't sure why it's so fast" |

## Ch 4 — Lava & diamond worlds
| Claim | Source | Note |
|---|---|---|
| 55 Cancri e: JWST (NIRCam + MIRI) found evidence of an atmosphere, likely CO₂ or CO, maybe fed by a magma ocean; dayside ~1,500 °C vs ~2,200 °C expected with no atmosphere | Hu et al., Nature, May 2024, arXiv:2405.04744 https://arxiv.org/abs/2405.04744v1 ; EurekAlert https://www.eurekalert.org/news-releases/1044236 ; Scientific American https://www.scientificamerican.com/article/in-a-first-jwst-confirms-an-atmosphere-on-a-rocky-exoplanet/ | Composition "not conclusively determined" (Space.com) → say "probably" |
| The diamond idea: in 2012, Madhusudhan et al. proposed that ≥⅓ of its mass (~3 Earth masses) could be diamond, based on the star appearing carbon-rich | ApJL 2012 "A Possible Carbon-rich Interior in Super-Earth 55 Cancri e"; Yale https://news.yale.edu/2012/10/11/nearby-super-earth-likely-diamond-planet | Later work questioned the star's carbon-to-oxygen ratio (Teske et al. 2013, arXiv:1309.6032). Script: "an idea, not a finding: later measurements of its star made it less likely". TODO confirm Teske's conclusion before using "less likely" |
| K2-141b: about two-thirds of it is always day; rock evaporates there, winds over 5,000 km/h carry it to the night side, where it falls back as "rocky rain" into a magma ocean | Nguyen, Cowan et al., MNRAS 2020; McGill https://reporter.mcgill.ca/supersonic-winds-rocky-rains-forecasted-on-lava-planet/ ; Physics World https://physicsworld.com/a/hell-like-exoplanet-experiences-rocky-rain-and-supersonic-wind/ | It's a model prediction → "scientists predict". The magma ocean depth (100 km, EarthSky only) is not used |
| CoRoT-7b | TODO | |

## Ch 5 — Puffy & strange
| Claim | Source | Note |
|---|---|---|
| WASP-107b is a "super-puff": density ~0.13 g/cm³ (Jupiter 1.33, Earth 5.51). JWST (2 Nature papers, 20 May 2024) found much less methane than expected, which means a hot interior (~460 K intrinsic) and a small core (<5 Earth masses); tidal heating from its oval orbit is the leading explanation | Sing et al. 2024 arXiv:2405.11018 ; Welbanks et al. 2024 arXiv:2405.11027 ; Physics World https://physicsworld.com/a/jwst-data-reveal-interior-structure-of-puffy-exoplanet/ ; Sky at Night https://skyatnightmagazine.com/news/wasp-107-b | Comparison: "about a tenth of Jupiter's density" (0.13/1.33 = 0.098) ✓ |
| TrES-2b reflects less than 1% of the light that hits it, darker than coal or black acrylic paint; found from a 6 ppm brightness change in Kepler data (Kipping & Spiegel 2011); why it is so dark is unknown | Harvard CfA https://www.cfa.harvard.edu/news/alien-world-blacker-coal ; ScienceDaily 2011-08-11 | Use "less than one percent", not the 99.9% figure (it's from a later analysis I haven't checked) |
| Kepler-51 super-puffs | TODO (search returned nothing) | |
