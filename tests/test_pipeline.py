import importlib

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import MultiPolygon, box

from pipeline.common import SCHEMA_FIELDS

buildings_step = importlib.import_module("pipeline.02_buildings")

LON, LAT = 36.30, 50.00
DEG = 0.0001


def square(x, y, size_m):
    width = size_m / (111320 * 0.6428)
    height = size_m / 110574
    return box(LON + x * DEG, LAT + y * DEG, LON + x * DEG + width, LAT + y * DEG + height)


@pytest.fixture
def raw():
    rows = [
        {"building_id": "r1", "levels": 9.0, "ghsl_anbh_mean": 27.0,
         "ghsl_age_period": "1980-1985", "geometry": square(0, 0, 40)},
        {"building_id": "w2", "levels": None, "ghsl_anbh_mean": 14.6,
         "ghsl_age_period": None, "geometry": square(10, 0, 30)},
        {"building_id": "w3", "levels": None, "ghsl_anbh_mean": 10.0,
         "ghsl_age_period": "Inainte de 1975", "geometry": square(20, 0, 25)},
        {"building_id": "w4", "levels": 1.0, "ghsl_anbh_mean": 3.0,
         "ghsl_age_period": None, "geometry": square(30, 0, 10)},
        {"building_id": "r5", "levels": 3.0, "ghsl_anbh_mean": 9.0,
         "ghsl_age_period": "1990-1995",
         "geometry": MultiPolygon([square(40, 0, 30), square(60, 0, 8)])},
        {"building_id": "w6", "levels": None, "ghsl_anbh_mean": 0.0,
         "ghsl_age_period": None, "geometry": square(70, 0, 30)},
    ]
    return gpd.GeoDataFrame(rows, geometry="geometry", crs=4326)


def test_small_buildings_are_dropped(raw):
    out = buildings_step.adapt(raw)
    assert "osm_w4" not in set(out["building_id"])
    assert len(out) == 5


def test_ids_get_osm_prefix_and_stay_unique(raw):
    out = buildings_step.adapt(raw)
    assert set(out["building_id"]) == {"osm_r1", "osm_w2", "osm_w3", "osm_r5", "osm_w6"}
    assert out["building_id"].is_unique


def test_output_has_exactly_the_schema_columns(raw):
    out = buildings_step.adapt(raw)
    assert list(out.columns) == SCHEMA_FIELDS + ["geometry"]


def test_geometry_is_single_polygon_in_degrees(raw):
    out = buildings_step.adapt(raw)
    assert set(out.geom_type) == {"Polygon"}
    assert out.crs.to_epsg() == 4326


def test_levels_fall_back_to_height(raw):
    out = buildings_step.adapt(raw).set_index("building_id")
    assert out.loc["osm_r1", "levels"] == 9
    assert out.loc["osm_w3", "levels"] == 3
    assert out.loc["osm_w2", "levels"] == 5


def test_zero_height_is_treated_as_missing(raw):
    out = buildings_step.adapt(raw).set_index("building_id")
    assert pd.isna(out.loc["osm_w6", "height_m"])
    assert pd.isna(out.loc["osm_w6", "levels"])
    assert out.loc["osm_w3", "height_m"] == 10.0


def test_epoch_is_cleaned(raw):
    out = buildings_step.adapt(raw).set_index("building_id")
    assert out.loc["osm_r1", "epoch"] == "1980-1985"
    assert out.loc["osm_w3", "epoch"] == "before-1975"
    assert pd.isna(out.loc["osm_w2", "epoch"])


def test_unfilled_fields_are_null(raw):
    out = buildings_step.adapt(raw)
    for field in ["damage_score", "triage_status", "cost_estimate_usd"]:
        assert out[field].isna().all()


def test_area_is_computed_in_metres(raw):
    out = buildings_step.adapt(raw).set_index("building_id")
    assert out.loc["osm_r1", "area_m2"] == pytest.approx(1600, rel=0.02)
