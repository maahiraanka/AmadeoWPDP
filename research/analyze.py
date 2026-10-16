"""Stability and significance checks on the weekly tables written by weekly_profiles.py.

  python3 research/analyze.py reports/nq reports/mnq

Chance level: each weekday equally likely = 20%. Two-sided binomial p-value per weekday.
Stability: first half vs second half of the sample (by week). Roll-suspect weeks excluded.
"""
import sys

import numpy as np
import pandas as pd
from scipy.stats import binomtest

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def share_table(wk, col):
    counts = wk[col].value_counts().reindex(range(5), fill_value=0)
    n = int(counts.sum())
    rows = []
    for i, c in counts.items():
        p = binomtest(int(c), n, 0.2).pvalue if n else np.nan
        rows.append({"weekday": WEEKDAYS[i], "weeks": int(c), "share": round(c / n, 3) if n else np.nan, "p_vs_20pct": round(p, 4)})
    return pd.DataFrame(rows).set_index("weekday")


def run(prefix):
    wk = pd.read_csv(f"{prefix}_weeks.csv", parse_dates=["week_mon"])
    clean = wk[~wk["roll_suspect"]].dropna(subset=["prev_eq"]).copy()
    mid = len(clean) // 2
    first, second = clean.iloc[:mid], clean.iloc[mid:]
    print(f"\n=== {prefix}: {len(clean)} clean weeks, {clean['week_mon'].min().date()} to {clean['week_mon'].max().date()} ===")
    for col in ["high_wd", "low_wd"]:
        name = "WEEKLY HIGH" if col == "high_wd" else "WEEKLY LOW"
        full = share_table(clean, col)
        h1 = share_table(first, col)["share"].rename("1st half")
        h2 = share_table(second, col)["share"].rename("2nd half")
        print(f"\n{name} day (share of clean weeks)")
        print(pd.concat([full, h1, h2], axis=1).to_string())
    print("\nPREMIUM / DISCOUNT at Monday open (vs prior week midpoint)")
    for state in ["premium", "discount"]:
        g = clean[clean["pd_at_open"] == state]
        print(f"\n  {state}: {len(g)} weeks")
        for col in ["high_wd", "low_wd"]:
            print(f"    {col.replace('_wd', ''):4s}", " ".join(f"{d}={s:.2f}" for d, s in share_table(g, col)["share"].items()))
    print("\nNOTE: 'roll' weeks excluded; results are descriptive frequencies, not trading edges.")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        run(p)
