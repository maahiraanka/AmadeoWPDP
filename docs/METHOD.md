# Method — weekly high/low timing and profile tests (NQ, MNQ)

## Data
- Databento GLBX.MDP3, `ohlcv-1m`, continuous front month (`NQ.v.0`, `MNQ.v.0`), 2019-01-01 to 2026-10-15.
- Cost ≈ $10 per instrument (from credits). Fetched with `research/fetch_data.py` (key from env only, cost shown first).
- Raw files in `research/data/` are git-ignored. Reports in `reports/` are committed.
- Databento flags some early-2019 days as "reduced quality". Not excluded yet; check the effect before the next run.
- Continuous series is spliced at contract rolls (quarterly). Rolls are detected by `instrument_id` changes (32 total).

## Definitions (decided here)
| Item | Definition |
|---|---|
| Trading week | Sunday 18:00 ET → Friday 17:00 ET (CME Globex) |
| Trading day | 18:00-to-18:00 ET session; Sunday 18:00 opens Monday |
| Weekday of an extreme | Trading weekday of the first 1m bar that prints the week's high/low |
| Week direction | Bull if weekly close > weekly open |
| Premium / discount | Monday open vs MIDPOINT of the PRIOR completed week (known before the week starts; no lookahead) |
| Roll-suspect week | Contract changes inside the week; excluded from all tests |
| Incomplete week | Fewer than 60 bars; excluded |

## Tests
1. **Base rates** — share of clean weeks whose high/low falls on each weekday (`weekly_profiles.py`).
2. **Significance vs 20%** — binomial test per weekday (`analyze.py`). Only a rough check: it ignores the random-walk effect below.
3. **Stability** — first half vs second half of the clean weeks (`analyze.py`).
4. **Null model (the key test)** — the 1m returns of each week are shuffled 200 times. This keeps each week's volatility and net move but removes timing. The weekday distribution under shuffling is the null. Edge = observed − null (`null_model.py`).
5. **Edge z-scores** — each edge divided by its null standard error. Bonferroni threshold for about 30 cells per instrument: |z| > 3.14 (`reports/edge_zscores.csv`).
6. **Sanity checks** — hand-checked one week against raw bars (matches); 5 synthetic-data tests (`tests/test_weekly_profiles.py`, all pass).

## Why the null model is required
A random walk with any drift puts its maximum late in the window and its minimum early (arcsine law). So "weekly high on Friday" and "weekly low on Monday" appear often even with no pattern at all. Plain base rates cannot separate pattern from arithmetic.

Note: the Monday/Friday pattern is an arithmetic effect. Any profile test must beat the shuffled null, not 20%.

## Limits
- Descriptive, in-sample over 2019–2026. No trading costs, no entries or stops.
- Premium/discount is one definition. Other definitions (daily ranges, dealing ranges, FVGs) would change the answer and are not tested yet.
- The 12-pattern guide's profiles need a rule for premium/discount and a rule for "sweep" before they can be tested.
