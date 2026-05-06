# gnss-interference-analysis


This repository contains the data pipeline and visualisation code for an interactive analysis of global GPS interference patterns from February 2022 to May 2026, published at **https://lucavellage.github.io/gnss-interference-analysis/**.

## Collaboration 
This project is a collaboration of Luca Vellage and Daniel Boppert. 
- Luca Vellage: Data preparation/aggregation, HTML/CSS styling, Svelteplot & writing
- Daniel Boppert: Background research, scraper & writing


**This project is a collaboration of Luca Vellage and Daniel Boppert.**## Methodology

Daily interference data was scraped from [gpsjam.org](https://gpsjam.org), which aggregates ADS-B flight transponder data to detect GPS signal degradation. Affected airspace was estimated by counting hexagonal grid cells (~1,800 km² each) where more than 2% of aircraft reported poor GPS accuracy.

## Repository Structure

```
gnss-interference-analysis/
├── src/gpsjam/             # Scraping pipeline
│   ├── scraper.py          # fetching from gpsjam.org
│   ├── parser.py           # CSV parsing and interference calculation
│   ├── db.py               # PostgreSQL interface
│   └── pipeline.py         # Orchestrates scraping pipeline
├── analysis/
│   └── area_time_series.py # Aggregation, exports CSV files for svelte
├── notebooks/              # Data exploratoin 
└── viz/ src/
    ├── routes/
    │   ├── +page.svelte        # Page layout, text and section definitions
    │   ├── +page.js            # loads aggregated csv files 
    │   └── +layout.svelte      # layout wrapper
    └── lib/assets/
        ├── GNSSChart.svelte    # plot chart with animations
        └── GNSSScroller.svelte # Scroller wrapper around @gka/svelte-scroller
```

## Data Pipeline

1. **Scrape**: `src/gpsjam/pipeline.py` fetches daily CSV snapshots from gpsjam.org and stores raw data in a local PostgreSQL database
2. **Aggregate**: `analysis/area_time_series.py` computes affected airspace per day globally and by conflict zone, exporting CSVs to `data/`
## Visualisation

The scrollytelling app in `viz/` is built with **SvelteKit**, **SveltePlot** and **@gka/svelte-scroller**.

### Data inputs
Two CSVs exported by `analysis/area_time_series.py` have manually been moved into `viz/static/data/`:
- `affected_km2_per_week.csv`: weekly global totals
- `affected_km2_by_zone_week.csv`: weekly totals by conflict zone

The csv files are available in this repository for replication.

### Sources

- Interference data: https://gpsjam.org
- Based on ADS-B data from: https://globe.adsbexchange.com