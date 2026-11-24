from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUTPUT = DATA / "output" / "buildings.geojson"

WEB_CRS = 4326
METRIC_CRS = 32637

SCHEMA_FIELDS = [
    "building_id",
    "area_m2",
    "levels",
    "height_m",
    "epoch",
    "typology",
    "vuln_score",
    "damage_score",
    "unosat_label",
    "insar_disp_mm",
    "insar_n_points",
    "exposure_score",
    "triage_status",
    "cost_estimate_usd",
]


def ensure_schema(buildings):
    out = buildings.copy()
    for field in SCHEMA_FIELDS:
        if field not in out.columns:
            out[field] = None
    return out[SCHEMA_FIELDS + ["geometry"]]


def write(buildings, path=OUTPUT):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    buildings.to_crs(WEB_CRS).to_file(path, driver="GeoJSON")
