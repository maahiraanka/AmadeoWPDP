# Profile-rule tests on NQ (step 2)

Script: `research/profile_tests.py`. Output: `reports/nq_profile_tests.csv`.
Sample: 375 clean NQ weeks (2019-01 → 2026-10). Null: 200 return shuffles per week.

## Features (fixed before running)
State = premium/discount at Monday open vs prior-week midpoint.
"Aligned extreme" = weekly LOW in discount weeks, weekly HIGH in premium weeks.

| Feature | Rule family (guide) |
|---|---|
| aligned_ext_mon / tue / wed / thu / fri | Which weekday sets the aligned extreme (Classic Tuesday/Wednesday, Thursday, Friday profiles) |
| mon_wed_range_broken_thu_fri | Mon–Wed range swept on Thu/Fri (Consolidation Thursday, Midweek profiles) |

Correction: Bonferroni over 18 tests → |z| > 2.99.

## Results
No feature passes. Largest |z|: premium Monday aligned extreme, −6.0 pts, z −2.15 (same cell as the Monday-high deficit in RESULTS.md, not significant after correction).

| State | Feature | Observed | Null | Edge | z |
|---|---|---|---|---|---|
| all | aligned_ext_tue | 0.149 | 0.135 | +1.4 | +0.8 |
| discount | aligned_ext_wed | 0.090 | 0.115 | −2.5 | −0.95 |
| discount | aligned_ext_thu | 0.103 | 0.128 | −2.4 | −0.87 |
| premium | aligned_ext_tue | 0.157 | 0.135 | +2.1 | +0.95 |
| premium | aligned_ext_wed | 0.148 | 0.129 | +1.9 | +0.85 |
| all | mon_wed_range_broken_thu_fri | 0.835 | 0.827 | +0.8 | +0.4 |

(full table: `reports/nq_profile_tests.csv`)

## What this does and does not show
- The guide's profile families, as I could operationalise them, do not beat the shuffled null on NQ 2019–2026.
- Tests use CLOSE prices for both observed and null, not the true highs/lows. This matches `null_model.py`, but it is a limitation.
- The rules are my operationalisation of loose text. A different operationalisation could give a different answer. Any new rule should be pre-registered before it is run.
- No holdout yet. Weeks after 2026-10-14 are reserved for testing the two candidate cells from RESULTS.md and any future rule.
- Not tested: higher-timeframe premium/discount beyond the prior week; sweep rules using true wicks; FVG/OTE/order-block entries.
