""""Parses raw gpsjam csv text into filtered rows"""

import csv
import io
import logging
from dataclasses import dataclass
 
log = logging.getLogger(__name__)

@dataclass
class ParsedRow:
    hex:                 str
    count_good_aircraft: int
    count_bad_aircraft:  int
    pct_bad:             float


def parse(raw: str) -> list[ParsedRow]:
    """
    Parse raw CSV text from gpsjam.org.
    Returns only rows where interference exceeds min_pct
 
    Interference formula (from gpsjam): pct_bad = 100 * (count_bad - 1) / (count_good + count_bad)
    """
    rows = []
    reader = csv.DictReader(io.StringIO(raw))
 
    for row in reader:
        try:
            good   = int(row["count_good_aircraft"])
            bad    = int(row["count_bad_aircraft"])
            hex_id = row["hex"].strip()
        except (KeyError, ValueError):
            log.debug(f"Skipping malformed row: {row}")
            continue
 
        total  = good + bad
        pct    = 100.0 * max(bad - 1, 0) / total if total > 0 else 0.0
 
        rows.append(ParsedRow(
            hex=hex_id,
            count_good_aircraft=good,
            count_bad_aircraft=bad,
            pct_bad=round(pct, 2),
        ))
 
    rows.sort(key=lambda r: r.pct_bad, reverse=True)
    log.info(f"Parsed {len(rows)} rows")
    return rows
 