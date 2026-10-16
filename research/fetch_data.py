"""Download 1-minute bars (CME Globex, continuous front month) from Databento.

The key is read ONLY from DATABENTO_API_KEY. The cost is shown first; nothing is bought above --max-cost.

  python3 research/fetch_data.py --symbol NQ.v.0 --start 2019-01-01 --end 2026-10-15 --max-cost 25 --yes
Output: research/data/<SYMBOL>_1m_<start>_<end>.csv.gz (git-ignored).
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="NQ.v.0")
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--max-cost", type=float, default=25.0, help="refuse above this many US$")
    ap.add_argument("--yes", action="store_true", help="download without asking")
    a = ap.parse_args()

    if not os.environ.get("DATABENTO_API_KEY"):
        sys.exit("DATABENTO_API_KEY is not set.")
    import databento as db

    client = db.Historical()
    q = dict(dataset="GLBX.MDP3", symbols=[a.symbol], stype_in="continuous",
             schema="ohlcv-1m", start=a.start, end=a.end)
    cost = client.metadata.get_cost(**q)
    print(f"{a.symbol} ohlcv-1m {a.start} to {a.end}: cost ${cost:.2f}")
    if cost > a.max_cost:
        sys.exit(f"Above --max-cost ${a.max_cost:.0f}; nothing downloaded.")
    if not a.yes and input("Download? [y/N] ").strip().lower() != "y":
        sys.exit("Cancelled.")

    df = client.timeseries.get_range(**q).to_df()
    out_dir = os.path.join(HERE, "data")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{a.symbol.replace('.', '_')}_1m_{a.start}_{a.end}.csv.gz")
    df.reset_index().to_csv(path, index=False)
    print(f"{len(df):,} rows -> {path}")


if __name__ == "__main__":
    main()
