import json
from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "fixtures" / "buildings_fake.geojson"
FIELDS = {
    "building_id",
    "area_m2",
    "levels",
    "height_m",
    "epoch",
    "typology",
    "vuln_score",
    "damage_score",
    "unosat_label",
    "exposure_score",
    "triage_status",
    "cost_estimate_usd",
}
TRIAGE = {"red", "orange", "yellow", "green", None}
SCORES = ["vuln_score", "damage_score", "exposure_score"]


@pytest.fixture(scope="module")
def features():
    return json.loads(FIXTURE.read_text())["features"]


def test_fixture_has_ten_buildings(features):
    assert len(features) == 10


def test_every_feature_has_all_fields(features):
    for f in features:
        assert set(f["properties"]) == FIELDS


def test_geometry_is_polygon_in_degrees(features):
    for f in features:
        assert f["geometry"]["type"] == "Polygon"
        lon, lat = f["geometry"]["coordinates"][0][0]
        assert -180 <= lon <= 180 and -90 <= lat <= 90


def test_triage_values_are_valid(features):
    for f in features:
        assert f["properties"]["triage_status"] in TRIAGE


def test_scores_are_between_zero_and_one(features):
    for f in features:
        for name in SCORES:
            v = f["properties"][name]
            assert v is None or 0 <= v <= 1


def test_building_ids_are_unique(features):
    ids = [f["properties"]["building_id"] for f in features]
    assert len(ids) == len(set(ids))


def test_fixture_contains_nulls_for_the_app_to_handle(features):
    assert any(f["properties"]["triage_status"] is None for f in features)
