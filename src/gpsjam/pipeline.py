"""
This file orchestrates scraper, parser and database
"""
import logging
from datetime import date, datetime, timedelta

from db import GpsjamDB
from parser import parse
from scraper import GpsjamScraper

log = logging.getLogger(__name__)


class GpsjamPipeline:
    """
    Runs the full gpsjam data pipeline: fetch --> parse --> store
    """

    def __init__(self):
        self.scraper = GpsjamScraper()
        self.db      = GpsjamDB()

    def __enter__(self):
        self.db.__enter__()
        return self

    def __exit__(self, *args):
        self.db.__exit__(*args)

    def run_date(self, d: date):
        #runs pipeline for single date
        if self.db.has_date(d):
            log.info(f"{d}: already in DB, skipping")
            return

        result = self.scraper.fetch(d)
        if not result.success:
            log.warning(f"{d}: skipped: {result.reason}")
            return

        rows = parse(result.raw)
        inserted = self.db.insert(d, rows)
        log.info(f"{d}:{inserted} rows inserted")

    def run_range(self, start_date: date, end_date: date):
        #runs pipeline for date range
        for result in self.scraper.fetch_range(start_date, end_date):
            if not result.success:
                log.warning(f"{result.date}: skipped: {result.reason}")
                continue
            rows     = parse(result.raw)
            inserted = self.db.insert(result.date, rows)
            log.info(f"{result.date}: {inserted} rows inserted")

    def run_last(self, n: int):
        #runs pipeline for last N days
        today = date.today()
        self.run_range(today - timedelta(days=n - 1), today)

    def backfill(self, start: date, end: date):
        #only fetches dates not in DB
        missing = self.db.missing_dates(start, end)
        log.info(f"Backfilling {len(missing)} missing dates")
        for d in missing:
            self.run_date(d)

def run(start: str, end: str = None):
    """
    Fetch and store gpsjam data for a date range.   
    To execute from notebook run for example: run("2025-01-01", "2025-01-31")
    """
    start_date = datetime.strptime(start, "%Y-%m-%d").date()
    end_date   = datetime.strptime(end, "%Y-%m-%d").date() if end else date.today()
    with GpsjamPipeline() as pipeline:
        pipeline.backfill(start_date, end_date)