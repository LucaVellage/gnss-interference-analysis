import logging
from datetime import date, timedelta
 
import psycopg2
import psycopg2.extras
 
from config import DATABASE_URL
from parser import ParsedRow
 
log = logging.getLogger(__name__)


class GpsjamDB:
    """
    PostgreSQL interface for table
    """
 
    def __init__(self, dsn: str = DATABASE_URL):
        self.dsn   = dsn
        self._conn = None
 
    def __enter__(self):
        log.info(f"Connecting to database")
        self._conn = psycopg2.connect(self.dsn)
        return self
 
    def __exit__(self, *_):
        if self._conn and not self._conn.closed:
            self._conn.close()
 
    def insert(self, d: date, rows: list[ParsedRow]) -> int:
        """
        Bulk inserts rows for a given date. 
        Skips duplicates 
        """
        if not rows:
            return 0
 
        data = [
            (d, r.hex, r.count_good_aircraft, r.count_bad_aircraft, r.pct_bad)
            for r in rows
        ]
 
        with self._conn.cursor() as cur:
            psycopg2.extras.execute_values(
                cur,
                """
                INSERT INTO interference
                    (date, hex, count_good_aircraft, count_bad_aircraft, pct_bad)
                VALUES %s
                ON CONFLICT (date, hex) DO NOTHING
                """,
                data,
            )
            inserted = cur.rowcount
        self._conn.commit()
 
        log.info(f"{d} — inserted {inserted}/{len(rows)} rows")
        return inserted
 

    def has_date(self, d: date) -> bool:
        """Return True if data for this date is already in db."""
        with self._conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM interference WHERE date = %s LIMIT 1", (d,)
            )
            return cur.fetchone() is not None
 
    def missing_dates(self, start: date, end: date) -> list[date]:
        """Return dates in [start, end] not yet in the database."""
        all_dates = {start + timedelta(days=i)
                     for i in range((end - start).days + 1)}
 
        with self._conn.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT date FROM interference WHERE date BETWEEN %s AND %s",
                (start, end)
            )
            stored = {row[0] for row in cur.fetchall()}
 
        missing = sorted(all_dates - stored)
        log.info(f"{len(missing)} dates missing between {start} and {end}")
        return missing
 
    def summary(self) -> list[dict]:
        """Per-date summary of stored interference data."""
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    date,
                    COUNT(*)               AS hex_count,
                    ROUND(AVG(pct_bad), 2) AS avg_pct,
                    MAX(pct_bad)           AS max_pct
                FROM interference
                GROUP BY date
                ORDER BY date DESC
                """
            )
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]