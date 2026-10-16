# Weekly profiles — rule specification

Status legend:
- **Text** = rule is written out in the source slides.
- **Diagram** = rule is only inferred from the candle pictures. Confirm against the video before coding.

Weekday abbreviations: M T W Th F. "Bullish/bearish week" = weekly close direction.

## 1. TGIF Setup — Text (source 7)

Valid setup, bullish version (bearish is the mirror):
1. Weekly low formed on Monday or Tuesday.
2. Expansion through Thursday into a key level ("Important Level" = Thursday's extreme, shown as a horizontal line).
3. Weekly objective met → look for Friday to return into the weekly range.

Targets (Text, source 8): two take-profit levels at **20%** and **30%** of the weekly range.
- Open: which anchor the percentages are measured from (weekly open, weekly low/high) — diagram shows the bracket spans the full weekly range; confirm measuring side.

## 2. Classic Expansion — Diagram (source 2)

- Bearish: Monday (small candle) sets the weekly high; Tue–Wed–Thu expand down; Fri closes up; weekly candle bearish.
- Bullish: mirror. Monday/Tue sets the weekly low; expansion up; weekly candle bullish.
- Rule to confirm: the extreme is set Mon or Tue, and no new extreme is made after that.

## 3. Midweek Reversal — Diagram (source 3)

- Bearish: weekly high forms Mon–Wed (Wed high in the example); Thu–Fri sell off; weekly bearish.
- Bullish: mirror; weekly low forms Mon–Wed; Thu–Fri rally.
- Rule to confirm: the extreme is set midweek (Wed), then reversal on Thursday.

## 4. Consolidation Reversal — Diagram (source 4)

- Mon–Wed form a tight range (inside candles).
- Thursday expands out of the range; Friday continues.
- Direction of the Thursday break vs. the prior-week bias is not clear from the slides. Confirm.

## 5. Intraweek Reversal — Diagram (source 5)

- Monday is a large candle that sets the weekly high (bearish example) or low (bullish example).
- Tue–Wed pull back against Monday's direction (small candles).
- Thu–Fri continue Monday's direction through the weekly extreme side.
- Rule to confirm: whether the reversal is in the Tue/Wed pullback or in the Thu/Fri move.

## 6. Thursday Counter — Diagram (source 6)

- Bearish: Mon–Wed up (weekly high set Wed/Thu area); Thursday turns down; Friday closes down.
- Bullish: mirror.
- Rule to confirm: the counter move starts on Thursday, against Mon–Wed direction.

## Common to all profiles (to define in code)

- Weekday of each extreme (high/low), using NY trading-day definitions (Sunday 18:00 ET session start, as used in the existing research pipeline).
- Weekly candle direction at Friday close.
- Daily-bias rule per profile (the source slides do not state one in text).

## Verification status

| Profile | Source type | Verified rules |
|---|---|---|
| TGIF | Text + diagrams | Steps 1–3 and targets (20%/30%) read from text; target anchor open |
| Classic Expansion | Diagrams | No |
| Midweek Reversal | Diagrams | No |
| Consolidation Reversal | Diagrams | No |
| Intraweek Reversal | Diagrams | No |
| Thursday Counter | Diagrams | No |

## Additional source: 12-pattern guide

The 12-profile text guide (source 8) is in `docs/PROFILES_12.md`. It has written rules for all 12 profiles, but its premium/discount arrays and bias are not defined in code yet.
