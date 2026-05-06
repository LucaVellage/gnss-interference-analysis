import os
from datetime import date

#gpsjam scraper
GPSJAM_URL = "https://gpsjam.org/data/{date}-h3_4.csv"
EARLIEST_DATE = date(2022, 2, 14)
REQUEST_TIMEOUT = 15
SLEEP_SEC = 0.5
 
HEADERS = {
    "User-Agent": "Mozilla/5.0 (research scraper; contact jjwiseman@gmail.com)"
}
 
KNOWN_GAPS = {
    "2022-06-08", "2022-06-09",
    "2022-10-13", "2022-10-14",
    "2022-12-27",
    "2024-01-28", "2024-01-30",
    "2024-07-14", "2024-07-15",
    "2025-01-08", "2025-01-09",
}

#db 
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://localhost/gpsjam"
)