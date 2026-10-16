"""Weekly high/low timing for NQ / MNQ (CME Globex week, New York time).

Definitions (decided here, documented in docs/METHOD.md):
- Trading week: Sunday 18:00 ET -> Friday 17:00 ET.
- Trading day of a bar: the 18:00-to-18:00 ET session it belongs to (Sunday 18:00 opens Monday).
- Weekly high/low day: trading weekday (Mon..Fri) of the first 1m bar that prints the week's extreme.
- Premium/discount at Monday open: compare the Monday open with the MIDPOINT of the PRIOR completed week.
- Roll-suspect weeks: the front-month contract (instrument_id) changes inside the week. The continuous
  series is spliced at the roll, so a week containing one can carry a fake high or low.

Usage:
  python3 research/weekly_profiles.py research/data/NQ_v_0_1m_*.csv.gz --out reports/nq
"""
import argparse
import os

import numpy as np
import pandas as pd

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def load_bars(path):
    df = pd.read_csv(path)
    ts_col = df.columns[0]
    df[ts_col] = pd.to_datetime(df[ts_col], utc=True)
    df = df.set_index(ts_col).sort_index()
    df = df[["open", "high", "low", "close", "volume", "instrument_id"]].astype({"open": float, "high": float, "low": float, "close": float, "volume": float, "instrument_id": int})
    df.index = df.index.tz_convert("America/New_York")
    return df


def add_trading_fields(df):
    """Session day = date after shifting 18:00 ET to midnight; weekday 0=Mon .. 6=Sun."""
    shifted = df.index + pd.Timedelta(hours=6)
    df = df.copy()
    # Roll marker on consecutive bars BEFORE dropping weekend rows
    df["roll_bar"] = df["instrument_id"] != df["instrument_id"].shift(1)
    df["sess_date"] = shifted.normalize().tz_localize(None)
    df["sess_wd"] = df["sess_date"].dt.weekday
    # Keep Monday..Friday sessions. Sat/Sun sessions (weekday 5/6) are outside the week.
    df = df[df["sess_wd"] <= 4]
    # Week id = Monday of the session's week
    df["week_mon"] = df["sess_date"] - pd.to_timedelta(df["sess_wd"], unit="D")
    return df


def weekly_table(df):
    rows = []
    for week_mon, g in df.groupby("week_mon", sort=True):
        if len(g) < 60:  # incomplete week (holiday or data gap)
            continue
        # First bar (positional) that prints the extreme; argmax/argmin return the earliest on ties
        hi_pos = int(np.argmax(g["high"].to_numpy()))
        lo_pos = int(np.argmin(g["low"].to_numpy()))
        rows.append({
            "week_mon": week_mon.date(),
            "open": g["open"].iloc[0],
            "close": g["close"].iloc[-1],
            "high": g["high"].iloc[hi_pos],
            "low": g["low"].iloc[lo_pos],
            "high_wd": int(g["sess_wd"].iloc[hi_pos]),
            "low_wd": int(g["sess_wd"].iloc[lo_pos]),
            "roll_suspect": bool(g["roll_bar"].any()),
            "first_ts": g.index[0],
        })
    wk = pd.DataFrame(rows).sort_values("week_mon").reset_index(drop=True)
    wk["direction"] = np.where(wk["close"] > wk["open"], "bull", np.where(wk["close"] < wk["open"], "bear", "flat"))
    # Prior completed week range (known before this week starts) and Monday open premium/discount
    wk["prev_high"] = wk["high"].shift(1)
    wk["prev_low"] = wk["low"].shift(1)
    wk["prev_eq"] = (wk["prev_high"] + wk["prev_low"]) / 2
    wk["pd_at_open"] = np.where(wk["open"] > wk["prev_eq"], "premium", "discount")
    return wk


def base_rates(wk, label):
    out = []
    for mask_name, mask in [("all weeks", wk.index == wk.index), ("excl. roll-suspect", ~wk["roll_suspect"])]:
        w = wk[mask].dropna(subset=["prev_eq"])
        for kind in ["high_wd", "low_wd"]:
            counts = w[kind].value_counts().reindex(range(5), fill_value=0)
            for i, c in counts.items():
                out.append({"instrument": label, "sample": mask_name, "extreme": kind.split("_")[0],
                            "weekday": WEEKDAYS[i], "weeks": int(c), "share": c / len(w)})
    return pd.DataFrame(out)


def conditional(wk, label):
    w = wk[~wk["roll_suspect"]].dropna(subset=["prev_eq"])
    out = []
    for pd_state, g in w.groupby("pd_at_open"):
        for kind in ["high_wd", "low_wd"]:
            counts = g[kind].value_counts().reindex(range(5), fill_value=0)
            for i, c in counts.items():
                out.append({"instrument": label, "pd_at_open": pd_state, "extreme": kind.split("_")[0],
                            "weekday": WEEKDAYS[i], "weeks": int(c), "share": c / len(g)})
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--out", required=True, help="output prefix, e.g. reports/nq")
    a = ap.parse_args()
    label = os.path.basename(a.path).split("_1m")[0]
    df = add_trading_fields(load_bars(a.path))
    wk = weekly_table(df)
    base = base_rates(wk, label)
    cond = conditional(wk, label)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    wk.to_csv(f"{a.out}_weeks.csv", index=False)
    base.to_csv(f"{a.out}_base_rates.csv", index=False)
    cond.to_csv(f"{a.out}_pd_conditional.csv", index=False)
    print(f"{label}: {len(wk)} weeks, {int(wk['roll_suspect'].sum())} roll-suspect")
    print(base[base["sample"] == "excl. roll-suspect"].pivot_table(index="weekday", columns="extreme", values="share").reindex(WEEKDAYS).round(3))


if __name__ == "__main__":
    main()
