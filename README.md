# AmadeoWPDP

ICT Weekly Profile research and indicator.

## Scope
- Instruments: NQ, MNQ, ES, MES, GC, MGC
- Profiles: Classic Expansion, Midweek Reversal, Consolidation Reversal, Intraweek Reversal, Thursday Counter, TGIF Setup

## Layout
- `docs/SOURCES.md` — source articles and their status
- `docs/PROFILES.md`, `docs/PROFILES_12.md` — profile rule specifications (text)
- `docs/METHOD.md`, `docs/RESULTS.md` — method and results
- `research/` — Python data loading, labelling, statistics
- `indicator/` — Pine Script v6 indicator (indicator only)
- `reports/` — walk-forward and calibration results

## Status
- NQ and MNQ 1-minute data (2019–2026) fetched; raw files git-ignored.
- Weekly high/low timing measured with a shuffled-return null model: no edge survives correction (see `docs/RESULTS.md`).
- 12-pattern and TTrades profile rules recorded as text (`docs/PROFILES*.md`); not yet testable without premium/discount and sweep rules.
- No indicator yet.

## Commands
- `python3 research/fetch_data.py --symbol NQ.v.0 --start 2019-01-01 --end 2026-10-15 --yes`
- `python3 research/weekly_profiles.py research/data/NQ_v_0_1m_*.csv.gz --out reports/nq`
- `python3 research/null_model.py research/data/NQ_v_0_1m_*.csv.gz --out reports/nq`
- `python3 research/analyze.py reports/nq reports/mnq`
- `python3 -m pytest tests -q`
