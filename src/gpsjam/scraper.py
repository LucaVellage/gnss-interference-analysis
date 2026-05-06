"""
Script for scraing gps interference data from gpsjam.org
"""

import time
import logging
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Generator
 
import requests as re

from config import (
    EARLIEST_DATE,
    GPSJAM_URL,
    KNOWN_GAPS,
    HEADERS,
    REQUEST_TIMEOUT,
    SLEEP_SEC,
)
 
log = logging.getLogger(__name__)

@dataclass
class ScrapeResult:
    date: date
    success: bool
    raw: str | None  = None
    reason: str | None = None 

class GpsjamScraper:
    """"
    Class fetches daily csv data from gpsjam.org
    """
    def __init__(self, sleep: float = SLEEP_SEC):
        self.sleep = sleep
        self.session = re.Session()
        self.session.headers.update(HEADERS)
   

    def fetch(self, d: date):
        """Fetches a single date and returns a ScrapeResult object"""
        skip = self._skip_reason(d)
        if skip:
            log.info(f"Skipping {d}: {skip}")
            return ScrapeResult(date=d, success=False, reason=skip)
        
        url = GPSJAM_URL.format(date=d)
        try:
            r = self.session.get(url, timeout=REQUEST_TIMEOUT)
        except re.RequestException as e:
            log.warning(f"{d}: request error: {e}")
            return ScrapeResult(date=d, success=False, reason=str(e))
        
        if r.status_code == 404:
            log.info(f"{d}: 404, no data available")
            return ScrapeResult(date=d, success=False, reason="404 not found")
 
        if r.status_code != 200:
            log.warning(f"{d}: HTTP {r.status_code}")
            return ScrapeResult(
                date=d, success=False, reason=f"HTTP {r.status_code}"
            )
 
        if not r.text.strip():
            return ScrapeResult(date=d, success=False, reason="empty response")
 
        log.info(f"{d}: fetched {len(r.text)} bytes")
        return ScrapeResult(date=d, success=True, raw=r.text)
        
    
    def fetch_range(self, start_date: date, end_date: date):
        """Fetches defined date range"""
        if start_date > end_date: 
            raise ValueError(f"Start date must be before end date.")
        
        dates = list(self._date_range(start_date, end_date))
        results = []

        for i, d in enumerate(dates):
            if i > 0:
                time.sleep(self.sleep) #pause between requests
            results.append(self.fetch(d))
        return results
    
    
    #helpers
    def _date_range(start_date: date, end_date: date) -> list[date]:
        dates = []
        d = start_date
        while d <= end_date:
            dates.append(d)
            d += timedelta(days=1)
        return dates
    
    def fetch_last(self, n: int) -> list[ScrapeResult]:
        """fetches last N days including today"""
        today = date.today()
        start = today - timedelta(days=n - 1)
        return self.fetch_range(start, today)
    
    @staticmethod
    def _skip_reason(d: date) -> str | None:
        """returns reason string if date should be skipped, otherwise None"""

        if d < EARLIEST_DATE:
            return f"before earliest available date ({EARLIEST_DATE})"
        if d > date.today():
            return "future date"
        if str(d) in KNOWN_GAPS:
            return "known data gap"
        return None
    
    