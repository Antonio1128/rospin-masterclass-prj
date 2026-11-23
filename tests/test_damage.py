import importlib

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import box

from pipeline.common import SCHEMA_FIELDS

damage_step = importlib.import_module("pipeline.03_damage")

LON, LAT, PIXEL = 36.30, 50.00, 0.0001


@pytest.fixture
def raster_path(tmp_path):
    values = np.full((20, 20), np.nan)
    values[:, :10] = 3.0
    values[0:5, 10:15] = 12.0
    path = tmp_path / "pwtt.tif"
    with rasterio.open(
        path, "w", driver="GTiff", height=20, width=20, count=1, dtype="float64",
        crs="EPSG:4326", transform=from_origin(LON, LAT, PIXEL, PIXEL),
    ) as dst:
        dst.write(values, 1)
    return path


def square(col, row, size):
    west = LON + col * PIXEL + PIXEL * 0.1
    north = LAT - row * PIXEL - PIXEL * 0.1
    return box(west, north - size * PIXEL * 0.8, west + size * PIXEL * 0.8, north)


@pytest.fixture
def buildings():
    rows = [
        {"building_id": "osm_a", "geometry": square(1, 5, 4)},
        {"building_id": "osm_b", "geometry": square(11, 1, 3)},
        {"building_id": "osm_c", "geometry": square(15, 10, 3)},
        {"building_id": "osm_d", "geometry": box(LON + 1, LAT + 1, LON + 1.001, LAT + 1.001)},
    ]
    return gpd.GeoDataFrame(rows, geometry="geometry", crs=4326)


def test_score_uses_the_pixels_inside_each_building(raster_path, buildings, monkeypatch):
    monkeypatch.setattr(damage_step, "RASTER", raster_path)
    out = damage_step.run(buildings).set_index("building_id")
    assert out.loc["osm_a", "damage_score"] == pytest.approx(3.0 / damage_step.SCORE_AT_FULL_DAMAGE)


def test_score_is_clipped_to_one(raster_path, buildings, monkeypatch):
    monkeypatch.setattr(damage_step, "RASTER", raster_path)
    out = damage_step.run(buildings).set_index("building_id")
    assert out.loc["osm_b", "damage_score"] == 1.0


def test_buildings_without_valid_pixels_stay_null(raster_path, buildings, monkeypatch):
    monkeypatch.setattr(damage_step, "RASTER", raster_path)
    out = damage_step.run(buildings).set_index("building_id")
    assert pd.isna(out.loc["osm_c", "damage_score"])
    assert pd.isna(out.loc["osm_d", "damage_score"])


def test_missing_raster_passes_data_through(tmp_path, buildings, monkeypatch):
    monkeypatch.setattr(damage_step, "RASTER", tmp_path / "missing.tif")
    out = damage_step.run(buildings)
    assert list(out.columns) == SCHEMA_FIELDS + ["geometry"]
    assert out["damage_score"].isna().all()


def test_scores_stay_between_zero_and_one(raster_path, buildings, monkeypatch):
    monkeypatch.setattr(damage_step, "RASTER", raster_path)
    scores = damage_step.run(buildings)["damage_score"].dropna()
    assert ((scores >= 0) & (scores <= 1)).all()
