"""Profile-rule tests on NQ against the shuffled-return null (step 2).

Features are FIXED here before the run (pre-registered in docs/PROFILE_TESTS.md). Each feature is a yes/no
label per week, built from the guide's rule families, using the Monday-open premium/discount state:
  discount -> the 'aligned' extreme is the weekly LOW; premium -> the aligned extreme is the weekly HIGH.

Observed and null both use CLOSE prices (same as null_model.py), so the comparison is like-for-like.
Edge = observed rate - shuffled rate. Two-sided z using the null standard error.
Correction: Bonferroni across all features x states.

  python3 research/profile_tests.py research/data/NQ_v_0_1m_2019-01-01_2026-10-15.csv.gz --out reports/nq
"""
import argparse
from math import sqrt

import numpy as np
import pandas as pd
from scipy.stats import norm

from weekly_profiles import add_trading_fields, load_bars, weekly_table

FEATURES = [
    "aligned_ext_mon", "aligned_ext_tue", "aligned_ext_wed", "aligned_ext_thu", "aligned_ext_fri",
    "mon_wed_range_broken_thu_fri",
]
STATES = ["all", "premium", "discount"]


def features(close, wd, state):
    """Return a dict of booleans for one week's close path (positions carry their session weekday)."""
    aligned_is_low = state == "discount"
    ext_pos = int(np.argmin(close)) if aligned_is_low else int(np.argmax(close))
    ext_wd = int(wd[ext_pos])
    early = wd <= 2  # Mon..Wed bars
    late = wd >= 3   # Thu..Fri bars
    out = {f"aligned_ext_{d}": ext_wd == i for i, d in enumerate(["mon", "tue", "wed", "thu", "fri"])}
    mw_hi, mw_lo = close[early].max(), close[early].min()
    late_close = close[late]
    out["mon_wed_range_broken_thu_fri"] = bool((late_close > mw_hi).any() or (late_close < mw_lo).any())
    return out


def run(path, perms, seed, out):
    rng = np.random.default_rng(seed)
    df = add_trading_fields(load_bars(path))
    wk = weekly_table(df)
    clean = wk[~wk["roll_suspect"]].dropna(subset=["prev_eq"])

    obs = {s: {f: 0 for f in FEATURES} | {"n": 0} for s in STATES}
    nul = {s: {f: 0.0 for f in FEATURES} | {"n": 0} for s in STATES}
    for _, row in clean.iterrows():
        g = df[df["week_mon"] == pd.Timestamp(row["week_mon"])]
        if len(g) < 60:
            continue
        close = g["close"].to_numpy()
        wd = g["sess_wd"].to_numpy()
        state = row["pd_at_open"]
        rets = np.diff(np.log(close))
        for key in ["all", state]:
            f = features(close, wd, state)
            obs[key]["n"] += 1
            for name in FEATURES:
                obs[key][name] += int(f[name])
        for _ in range(perms):
            sh = close[0] * np.exp(np.concatenate([[0.0], np.cumsum(rng.permutation(rets))]))
            f = features(sh, wd, state)
            for key in ["all", state]:
                nul[key]["n"] += 1
                for name in FEATURES:
                    nul[key][name] += int(f[name])

    n_tests = len(FEATURES) * len(STATES)
    z_crit = norm.ppf(1 - 0.025 / n_tests)
    rows = []
    for s in STATES:
        n_weeks = obs[s]["n"]
        for name in FEATURES:
            p_obs = obs[s][name] / n_weeks
            p_null = nul[s][name] / nul[s]["n"]
            se = sqrt(max(p_null * (1 - p_null), 1e-12) / n_weeks)
            z = (p_obs - p_null) / se
            rows.append({"state": s, "feature": name, "weeks": n_weeks,
                         "observed": round(p_obs, 3), "null": round(p_null, 3),
                         "edge": round(p_obs - p_null, 3), "z": round(z, 2),
                         "passes_bonferroni": abs(z) > z_crit})
    res = pd.DataFrame(rows)
    res.to_csv(f"{out}_profile_tests.csv", index=False)
    print(f"{n_tests} tests, Bonferroni |z| > {z_crit:.2f}")
    print(res.to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--perms", type=int, default=200)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    run(a.path, a.perms, a.seed, a.out)
