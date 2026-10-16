# Results — weekly high/low timing, NQ and MNQ

Sample: NQ 375 clean weeks (2019-01 → 2026-10); MNQ 358 clean weeks (2019-05 → 2026-10).
All figures are weekday shares of the weekly high or low. Null = shuffled-return expectation.

## Headline
- The well-known "Friday high / Monday low" pattern is arithmetic, not an edge. Observed vs null: Friday high 35.5% vs 35.3%; Monday low 34.9% vs 35.9%.
- No cell passes the multiple-testing bar (|z| > 3.14). Largest: Monday weekly high 6 points below null (z ≈ −2.8, both instruments).
- NQ and MNQ agree on the weekday of the weekly high in 99% of common weeks, so they share one market, not two independent samples.

## Edge vs shuffled null (all weeks)
| Weekday | High observed | High null | Edge | Low observed | Low null | Edge |
|---|---|---|---|---|---|---|
| Mon | 0.176 | 0.238 | −6.2 pts (z −2.8) | 0.349 | 0.359 | −1.0 |
| Tue | 0.171 | 0.133 | +3.8 (z +2.2) | 0.160 | 0.149 | +1.1 |
| Wed | 0.131 | 0.122 | +0.8 | 0.120 | 0.124 | −0.4 |
| Thu | 0.168 | 0.153 | +1.5 | 0.149 | 0.131 | +1.8 |
| Fri | 0.355 | 0.353 | +0.1 | 0.221 | 0.237 | −1.6 |

Edges in percentage points. Full table incl. premium and discount: `reports/nq_null.csv`, `reports/mnq_null.csv`.

## Premium / discount at Monday open (NQ; MNQ in same file)
| State | Weeks | Cell | Edge | z |
|---|---|---|---|---|
| Discount | 145 | Tue weekly high | +6.0 pts | +2.1 |
| Premium | 230 | Mon weekly high | −6.4 pts | −2.3 |
| Discount | 145 | Mon weekly low | +3.3 pts | — (below |z| 2 threshold) |

The discount-Tuesday-high result runs OPPOSITE to the 12-pattern guide's "Classic Tuesday High" idea, which places the high in premium. Not significant after correction.

## Verdict
- No day-of-week timing edge for NQ or MNQ over 2019–2026 that survives the null model and multiple-testing correction.
- Two cells are worth a pre-registered out-of-sample test on new weeks (after 2026-10-14):
  1. Monday weekly high below chance.
  2. Tuesday weekly high above chance in discount weeks.
- Do not build an indicator on these yet.

## Next
1. Pre-register the two cells (written before new data arrives). Test on weeks after 2026-10-14.
2. Test the profile rules as conditional tests against the same null (shuffled returns within premium/discount state).
3. Test alternative premium/discount definitions (prior-day range, current-week running range). Pick one per test, no peeking.
