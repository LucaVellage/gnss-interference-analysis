import os
import psycopg2
import pandas as pd
import h3
import geopandas as gpd
from shapely.geometry import Point, Polygon
from sqlalchemy import create_engine

import sys
sys.path.insert(0, "../src/gpsjam")
from config import DATABASE_URL

OUTPUT_DIR = "../data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

#hex area derived from hex grid
HEX_RESOLUTION = 4
HEX_AREA_KM2 = h3.average_hexagon_area(HEX_RESOLUTION, unit="km^2")

#conflict zones defined as bounding polygons
CONFLICT_ZONES = {
    "Black Sea & Ukraine": Polygon([
        (22.8, 41.1), (46.8, 40.7), (37.0, 52.3), (22.0, 52.5)
    ]),
    "Baltic Sea Region": Polygon([
        (14.0, 53.5), (32.0, 53.5), (32.0, 65.0), (14.0, 65.0)
    ]),
    "Eastern Mediterranean & Levant": Polygon([
        (33.5, 27.6), (41.9, 27.6), (41.9, 36.6), (20.5, 37.3)
    ]),
    "Middle East (Iraq/Iran)": Polygon([
        (38.6, 30.5), (61.9, 19.2), (62.1, 37.2), (41.9, 37.2)
    ]),
    "Arabian Peninsula & Red Sea": Polygon([
        (32.3, 27.2), (43.3, 7.3), (62.0, 16.5), (40.5, 31.5)
    ]),
    "South Asia": Polygon([
        (59.9, 3.8), (100.6, 6.1), (100.0, 35.0), (60.0, 35.0)
    ]),
}

#Subregion mapping for previous analysis
SUBREGION_MAP = {
    "Eastern Europe":             "Eastern Europe",
    "Northern Europe":            "Baltic & Northern Europe",
    "Western Asia":               "Middle East",
    "Eastern Asia":               "East Asia",
    "Central Asia":               "Central Asia",
    "Southern Asia":              "South Asia",
    "South-Eastern Asia":         "South-East Asia",
    "Northern Africa":            "North Africa",
    "Middle Africa":              "Africa",
    "Western Africa":             "Africa",
    "Eastern Africa":             "Africa",
    "Southern Africa":            "Africa",
    "Southern Europe":            "Southern Europe",
    "Western Europe":             "Western Europe",
    "Northern America":           "North America",
    "Central America":            "Latin America",
    "Caribbean":                  "Latin America",
    "South America":              "Latin America",
    "Australia and New Zealand":  "Other",
    "Melanesia":                  "Other",
    "Antarctica":                 "Other",
    "Seven seas (open ocean)":    "Other",
}


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def classify_hex_to_zone(hex_id: str) -> str:
    """Returns the conflict zone name for a hex centroid."""
    lat, lon = h3.cell_to_latlng(hex_id)
    pt = Point(lon, lat)
    for zone_name, polygon in CONFLICT_ZONES.items():
        if polygon.contains(pt):
            return zone_name
    return "Other"


def build_hex_zone_lookup(engine) -> pd.DataFrame:
    """
    Maps every unique hex ID in the DB to a conflict zone.
    Caches mapping in db
    """
    df = pd.read_sql("SELECT DISTINCT hex FROM interference", engine)
    df["zone"] = df["hex"].map(classify_hex_to_zone)

    print("Zone distribution across all hexes:")
    print(df["zone"].value_counts().to_string())
    return df


def build_hex_country_lookup(engine) -> pd.DataFrame:
    """
    Maps every unique hex ID to a country and subregionwith Natural Earth boundaries.
    """
    df = pd.read_sql("SELECT DISTINCT hex FROM interference", engine)
    df["lat"], df["lon"] = zip(*df["hex"].map(h3.cell_to_latlng))

    world = gpd.read_file(
        "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    )

    gdf = gpd.GeoDataFrame(
        df,
        geometry=[Point(lon, lat) for lat, lon in zip(df["lat"], df["lon"])],
        crs="EPSG:4326",
    )
    joined = gpd.sjoin(
        gdf, world[["NAME", "SUBREGION", "geometry"]],
        how="left", predicate="within"
    )
    joined["region"] = joined["SUBREGION"].map(SUBREGION_MAP).fillna("Other")

    return (
        joined[["hex", "NAME", "SUBREGION", "region"]]
        .rename(columns={"NAME": "country"})
        .drop_duplicates("hex")
    )


def affected_km2_per_day(engine) -> pd.DataFrame:
    """sql query for global affected airspace."""
    query = """
        SELECT
            date,
            COUNT(*)                                         AS affected_hexes,
            COUNT(*) * %(hex_area)s                          AS affected_km2,
            COUNT(*) FILTER (WHERE pct_bad > 10)             AS high,
            COUNT(*) FILTER (WHERE pct_bad BETWEEN 2 AND 10) AS medium
        FROM interference
        WHERE pct_bad > 2
        GROUP BY date
        ORDER BY date
    """
    return pd.read_sql(query, engine, params={"hex_area": HEX_AREA_KM2})


def affected_km2_by_zone(engine, lookup: pd.DataFrame) -> pd.DataFrame:
    """
    Affected airspace per day by conflict zone.
    Joins interference rows with the hex-zone lookup
    """
    df = pd.read_sql(
        "SELECT date, hex, pct_bad FROM interference WHERE pct_bad > 2",
        engine,
    )
    df = df.merge(lookup[["hex", "zone"]], on="hex", how="left")
    df["zone"] = df["zone"].fillna("Other")

    result = (
        df.groupby(["date", "zone"])
        .agg(
            affected_hexes=("hex", "count"),
            high=("pct_bad", lambda x: (x > 10).sum()),
            medium=("pct_bad", lambda x: ((x > 2) & (x <= 10)).sum()),
        )
        .reset_index()
    )
    result["affected_km2"] = result["affected_hexes"] * HEX_AREA_KM2
    return result.sort_values(["date", "zone"])

 
 
def main():
    conn = get_connection()             
    engine = create_engine(DATABASE_URL) 
 
    # Global time series
    df_global = affected_km2_per_day(engine)
    df_global["date"] = pd.to_datetime(df_global["date"])
    path = os.path.join(OUTPUT_DIR, "affected_km2_per_day.csv")
    df_global.to_csv(path, index=False)
 
    #builds or load hex lookup
    cur = conn.cursor()
    cur.execute("SELECT to_regclass('hex_zone')")
    if cur.fetchone()[0] is None:
        print("Building hex-zone lookup table")
        lookup = build_hex_zone_lookup(engine)
        lookup.to_sql("hex_zone", engine, if_exists="replace", index=False)
    else:
        print("hex_zone table already exists, loading from DB")
        lookup = pd.read_sql("SELECT hex, zone FROM hex_zone", engine)
    cur.close()
 
    # Conflict zone breakdown
    df_zones = affected_km2_by_zone(engine, lookup)
    df_zones["date"] = pd.to_datetime(df_zones["date"]) 
    path = os.path.join(OUTPUT_DIR, "affected_km2_by_zone.csv")
    df_zones.to_csv(path, index=False)
 
    # Weekly global
    weekly = df_global.set_index("date").resample("W-MON").mean().round(0)
    path = os.path.join(OUTPUT_DIR, "affected_km2_per_week.csv")
    weekly.to_csv(path)
 
    # Weekly by zone
    weekly_z = (
        df_zones.set_index("date")
        .groupby("zone")[["affected_hexes", "affected_km2", "high", "medium"]]
        .resample("W-MON").mean().round(0)
    )
    path = os.path.join(OUTPUT_DIR, "affected_km2_by_zone_week.csv")
    weekly_z.to_csv(path)
 
    conn.close()
    engine.dispose()
 
 
if __name__ == "__main__":
    main()