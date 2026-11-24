import re

import geopandas as gpd
import pandas as pd

from pipeline.common import DATA, METRIC_CRS, ensure_schema

RAW = DATA / "in_use" / "buildings_osm_ghsl.geojson"
MIN_AREA_M2 = 400
METERS_PER_LEVEL = 3

EPOCH_RANGE = re.compile(r"(\d{4})\s*-\s*(\d{4})")
EPOCH_BEFORE = re.compile(r"[IiÎî]nainte de (\d{4})")


def clean_epoch(value):
    if not isinstance(value, str):
        return None
    match = EPOCH_RANGE.search(value)
    if match:
        return f"{match.group(1)}-{match.group(2)}"
    match = EPOCH_BEFORE.search(value)
    if match:
        return f"before-{match.group(1)}"
    return None


def ghsl_height(raw):
    height = pd.to_numeric(raw["ghsl_anbh_mean"], errors="coerce")
    return height.where(height > 0)


def resolve_levels(raw):
    levels = pd.to_numeric(raw["levels"], errors="coerce")
    from_height = ghsl_height(raw) / METERS_PER_LEVEL
    return levels.fillna(from_height).round().clip(lower=1).astype("Int64")


def to_polygon(geometry):
    if geometry.geom_type == "Polygon":
        return geometry
    return max(geometry.geoms, key=lambda part: part.area)


def adapt(raw):
    area = raw.to_crs(METRIC_CRS).geometry.area
    keep = area >= MIN_AREA_M2
    raw = raw[keep]
    area = area[keep]
    adapted = gpd.GeoDataFrame(
        {
            "building_id": "osm_" + raw["building_id"].astype(str),
            "area_m2": area.round(1),
            "levels": resolve_levels(raw),
            "height_m": ghsl_height(raw).round(1),
            "epoch": raw["ghsl_age_period"].map(clean_epoch),
        },
        geometry=raw.geometry.map(to_polygon),
        crs=raw.crs,
    )
    return ensure_schema(adapted.reset_index(drop=True))


def run(buildings=None):
    return adapt(gpd.read_file(RAW))
