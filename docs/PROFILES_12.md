# ICT Weekly Profiles — 12 patterns (source 8)

Source: "ICT Weekly Profiles — 12 Patterns to Identify the Weekly High & Low + Free PDF" (17-page text guide, uploaded PDF).
Attribution in the guide: Michael Huddleston. This is a third-party write-up, not a primary ICT source. Treat as a claim to test.

Status: **Text rules, not yet tested.** Every profile needs a data test before it is used.

## Shared definitions (from the guide)

- **Higher-timeframe PD array**: premium (above equilibrium, sell zone) and discount (below, buy zone). The guide does not define how to draw it. This must be defined in code before any test.
- **Bullish / bearish higher-timeframe context**: not defined in the guide. Must be defined.
- **Intra-week high / low**: the extremes so far in the week at each day.
- **Stop-hunts / "seek and destroy"**: price runs a shallow stop beyond a level, then reverses.
- Guide says the profiles are "tendencies, not predictions", and that Monday close rules out few profiles.

## The 12 profiles

| # | Profile | Written rule (summary) | Extreme |
|---|---|---|---|
| I | Classic Tuesday Low of Week | Bullish HTF context. Mon manipulates above HTF discount array. Tue drops into it. | Week low on Tue (London or NY) |
| II | Classic Tuesday High of Week | Bearish HTF context. Mon manipulates below HTF premium array. Tue rises into it. | Week high on Tue |
| III | Wednesday Low of Week | Bullish. Mon–Tue hover above HTF discount array. Wed drops into it. | Week low on Wed |
| IV | Wednesday High of Week | Bearish. Mon–Tue hover below HTF premium array. Wed rises into it. | Week high on Wed |
| V | Consolidation Thursday Bullish Reversal | Bullish. Consolidate Mon–Wed, run the intra-week low, reject it. Reversal. | Week low in Mon–Wed range, then reversal |
| VI | Consolidation Thursday Bearish Reversal | Bearish. Consolidate Mon–Wed, run the intra-week high, reject it. Reversal. | Week high in Mon–Wed range, then reversal |
| VII | Consolidation Midweek Rally | Bullish. Consolidate Mon–Wed, run intra-week high, expand higher into Fri. | Week high on Fri |
| VIII | Consolidation Midweek Decline | Bearish. Consolidate Mon–Wed, run intra-week low, expand lower into Fri. | Week low on Fri |
| IX | Seek and Destroy Bullish Friday | Neutral-low probability. Mon–Thu shallow stops under and above intra-week high. Runs high, expands higher Fri. | Fri (high) |
| X | Seek and Destroy Bearish Friday | Neutral-low probability. Mon–Thu shallow stops. Runs intra-week low, expands lower Fri. | Fri (low) |
| XI | Wednesday Weekly Bullish Reversal | Bullish. Consolidate Mon–Tue, drive lower into HTF discount on Wed (sell stops), reverse strongly. | Week low on Wed |
| XII | Wednesday Weekly Bearish Reversal | Bearish. Consolidate Mon–Tue, drive higher into HTF premium on Wed (buy stops), reverse strongly. | Week high on Wed |

Notes:
- The guide's intro and FAQ say profiles I–VIII, XI, XII are high-probability; IX and X are low-probability and tied to NFP / rate news in July–August.
- The guide says V and VI "pivot around the 02:00 PM NY" news drive (Thursday). This is a claim; time-of-day rules need data.

## Internal conflicts to resolve before testing

1. **Intro vs. FAQ on profile count.** The intro says "12 distinct profiles". The FAQ says the list includes "two Wednesday Weekly Reversal profiles" and "four Consolidation profiles", which matches the 12 list. No conflict found, but check the wording for IX/X against the diagrams.
2. **V/VI vs. VII/VIII**: V and VI are described as "consolidate Mon–Wed then reverse". VII and VIII are "consolidate Mon–Wed then expand". The only difference is whether the Mon–Wed range is swept and rejected. This needs a precise sweep rule.
3. **Overlap with TTrades profiles** (doc/PROFILES.md, sources 2–6): Classic Expansion, Midweek Reversal, Consolidation Reversal, Intraweek Reversal and Thursday Counter are not the same list as these 12. Map them against each other before combining.
4. **Weekly direction**: the guide says "bullish week" but also "bullish HTF context". These are two different things (weekly candle vs. HTF array). Pick one for the test.

## What to test (data, not text)

For each profile, label each week and measure:
- Day of the week-high and week-low (NY trading-day, 18:00 ET start).
- Whether the week's extreme prints in the day the profile predicts.
- Base rate: how often each weekday sets the weekly high/low, with no profile filter. Any profile must beat that base rate.
