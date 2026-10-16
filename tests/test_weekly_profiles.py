"""Synthetic-data checks for the weekly labelling logic (no market data needed)."""
import os
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "research"))
from weekly_profiles import add_trading_fields, weekly_table  # noqa: E402

NY = "America/New_York"


def make_bars(start, minutes, closes, instrument=1):
    """1-minute bars: open=high=low=close=value (exact extremes, easy to reason about)."""
    idx = pd.date_range(start, periods=minutes, freq="1min", tz=NY)
    vals = np.resize(np.asarray(closes, dtype=float), minutes)
    return pd.DataFrame({"open": vals, "high": vals, "low": vals, "close": vals,
                         "volume": 1.0, "instrument_id": instrument}, index=idx)


def test_sunday_1800_opens_monday_session():
    df = make_bars("2024-01-07 18:00", 5, [100])  # Sunday 18:00 ET
    out = add_trading_fields(df)
    assert (out["sess_wd"] == 0).all()  # belongs to Monday's session


def test_friday_after_1700_is_outside_the_week():
    df = make_bars("2024-01-12 17:00", 120, [100])  # Friday 17:00 -> Friday 19:00 ET
    out = add_trading_fields(df)
    # Friday 18:00 ET onward opens Saturday's session, which the week excludes
    assert out.loc[out.index >= pd.Timestamp("2024-01-12 18:00", tz=NY)].empty
    # Friday 17:00-17:59 is still Friday's session (weekday 4) and stays in the week
    assert (out["sess_wd"] == 4).all()


def test_weekly_extremes_and_weekdays():
    # Build one week: Monday 18:00 -> Friday 16:59 ET, with a known high on Thursday and low on Tuesday.
    start = "2024-01-07 18:00"
    n = 6825  # about a full week of 1m bars
    closes = np.full(n, 100.0)
    days = add_trading_fields(make_bars(start, n, closes))
    df = make_bars(start, n, closes)
    pos_low = 2000   # Monday session, deep in the week -> Tuesday session
    pos_high = 4000
    df.iloc[pos_low, df.columns.get_loc("low")] = 50.0
    df.iloc[pos_high, df.columns.get_loc("high")] = 150.0
    wk = weekly_table(add_trading_fields(df))
    row = wk.iloc[0]
    assert row["high"] == 150.0 and row["low"] == 50.0
    assert row["high_wd"] == int(add_trading_fields(df).iloc[pos_high]["sess_wd"])
    assert row["low_wd"] == int(add_trading_fields(df).iloc[pos_low]["sess_wd"])


def test_roll_bar_flags_the_week_it_sits_in():
    start = "2024-01-07 18:00"
    n = 6825
    df = make_bars(start, n, np.full(n, 100.0))
    df.iloc[3000:, df.columns.get_loc("instrument_id")] = 2  # contract roll mid-week
    wk = weekly_table(add_trading_fields(df))
    assert bool(wk.iloc[0]["roll_suspect"]) is True


def test_premium_discount_uses_prior_week_midpoint():
    # Week 1: range 100..200 (midpoint 150). Week 2 opens at 160 -> premium; opens at 140 -> discount.
    w1 = make_bars("2024-01-07 18:00", 6825, np.linspace(100, 200, 6825))
    w2_open = 160.0
    w2 = make_bars("2024-01-14 18:00", 6825, np.full(6825, w2_open))
    wk = weekly_table(add_trading_fields(pd.concat([w1, w2])))
    assert wk.iloc[1]["pd_at_open"] == "premium"
    w2b = make_bars("2024-01-14 18:00", 6825, np.full(6825, 140.0))
    wk2 = weekly_table(add_trading_fields(pd.concat([w1, w2b])))
    assert wk2.iloc[1]["pd_at_open"] == "discount"


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
