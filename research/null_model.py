"""Null model: how often would each weekday set the weekly high/low if there were NO weekday structure?

For each clean week, the 1-minute log returns are shuffled (permutation test). Shuffling keeps each week's
volatility and total move but destroys timing. The weekday of the weekly high/low under shuffles is the null.
Observed and null both use CLOSE prices so the comparison is like-for-like.

  python3 research/null_model.py research/data/NQ_v_0_1m_2019-01-01_2026-10-15.csv.gz --perms 200 --out reports/nq
"""
import argparse

import numpy as np
import pandas as pd

from weekly_profiles import add_trading_fields, load_bars, weekly_table

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def weekly_close_paths(df, wk):
    clean = wk[~wk["roll_suspect"]].dropna(subset=["prev_eq"])
    for _, row in clean.iterrows():
        g = df[df["week_mon"] == pd.Timestamp(row["week_mon"])]
        if len(g) < 60:
            continue
        yield row["pd_at_open"], g["close"].to_numpy(), g["sess_wd"].to_numpy()


def extremes_weekday(path, wd):
    return wd[int(np.argmax(path))], wd[int(np.argmin(path))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--out", required=True)
    ap.add_argument("--perms", type=int, default=200)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)

    df = add_trading_fields(load_bars(a.path))
    wk = weekly_table(df)
    # counts[state] = [obs_hi, obs_lo, null_hi, null_lo, weeks]
    counts = {s: {"obs_hi": np.zeros(5), "obs_lo": np.zeros(5), "null_hi": np.zeros(5), "null_lo": np.zeros(5), "weeks": 0}
              for s in ["all", "premium", "discount"]}
    for state, close, wd in weekly_close_paths(df, wk):
        for key in ["all", state]:
            c = counts[key]
            c["weeks"] += 1
            h, l = extremes_weekday(close - close[0], wd)
            c["obs_hi"][h] += 1
            c["obs_lo"][l] += 1
        rets = np.diff(np.log(close))
        for _ in range(a.perms):
            shuffled = np.concatenate([[0.0], np.cumsum(rng.permutation(rets))])
            h, l = extremes_weekday(close[0] * np.exp(shuffled) - close[0], wd)
            for key in ["all", state]:
                counts[key]["null_hi"][h] += 1
                counts[key]["null_lo"][l] += 1
    rows = []
    for key, c in counts.items():
        n = c["weeks"]
        for i, day in enumerate(WEEKDAYS):
            oh, ol = c["obs_hi"][i] / n, c["obs_lo"][i] / n
            nh, nl = c["null_hi"][i] / (n * a.perms), c["null_lo"][i] / (n * a.perms)
            rows.append({"state": key, "weeks": n, "weekday": day,
                         "high_observed": round(oh, 3), "high_null": round(nh, 3), "high_edge": round(oh - nh, 3),
                         "low_observed": round(ol, 3), "low_null": round(nl, 3), "low_edge": round(ol - nl, 3)})
    out = pd.DataFrame(rows)
    out.to_csv(f"{a.out}_null.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
