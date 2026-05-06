"""
command line interface for gpsjam pipeline.

Example: 
python run.py --date 2024-06-01
python run.py --start 2024-01-01 --end 2024-01-31
python run.py --backfill --start 2022-02-14
python run.py --summary
"""

import argparse
import logging
from datetime import date, datetime

from db import GpsjamDB
from pipeline import GpsjamPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def main():
    parser = argparse.ArgumentParser(description="gpsjam.org → PostgreSQL")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--date",    type=parse_date, help="Single date (YYYY-MM-DD)")
    group.add_argument("--last",    type=int,        help="Last N days")
    group.add_argument("--start",   type=parse_date, help="Start of date range")
    group.add_argument("--summary", action="store_true", help="Show DB summary")
    parser.add_argument("--end",      type=parse_date, help="End of date range (default: today)")
    parser.add_argument("--backfill", action="store_true", help="Only fetch dates missing from DB")
    args = parser.parse_args()

    if args.summary:
        with GpsjamDB() as db:
            rows = db.summary()
        if not rows:
            print("No data in DB yet.")
            return
        print(f"\n{'Date':<12} {'Hexes':>6} {'Avg %':>7} {'Max %':>7}")
        print("-" * 35)
        for r in rows:
            print(f"{str(r['date']):<12} {r['hex_count']:>6} "
                  f"{float(r['avg_pct']):>7.1f} {float(r['max_pct']):>7.1f}")
        return

    with GpsjamPipeline() as pipeline:
        if args.date:
            pipeline.run_date(args.date)

        elif args.last:
            pipeline.run_last(args.last)

        elif args.start:
            end = args.end or date.today()
            if args.backfill:
                pipeline.backfill(args.start, end)
            else:
                pipeline.run_range(args.start, end)


if __name__ == "__main__":
    main()