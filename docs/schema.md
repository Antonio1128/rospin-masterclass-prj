# Building schema

Contract between Data/AI and Development. Every building in `buildings.geojson` is one GeoJSON Feature (Polygon) with these properties. A field that is not computed yet is `null`, and the app must work with nulls.

Geometry is stored in EPSG:4326. Areas and distances are computed in EPSG:32637 (metres).

| Field | Type | Example | Filled by | Pipeline step |
|---|---|---|---|---|
| building_id | string | osm_123456 | Iarina | 2 |
| area_m2 | number | 1250 | Iarina | 2 |
| levels | integer | 9 | Iarina | 2 |
| height_m | number | 27.0 | Iarina | 2 |
| epoch | string | 1975-1990 | Iarina | 2 |
| typology | string | panel_block | Iarina | 6 |
| vuln_score | number 0-1 | 0.6 | Iarina | 6 |
| damage_score | number 0-1 | 0.82 | Diana | 3 |
| unosat_label | string | destroyed | Diana | 4 |
| insar_disp_mm | number | -7.5 | Iarina | 5 |
| insar_n_points | integer | 14 | Iarina | 5 |
| exposure_score | number 0-1 | 0.4 | Iarina | 6 |
| triage_status | red / orange / yellow / green | red | Diana + Iarina | 6 |
| cost_estimate_usd | number | 1850000 | Iarina | 6 |

## Triage status

| Value | Meaning | Action |
|---|---|---|
| red | Destroyed | Nobody enters |
| orange | Standing, but moving or highly exposed | Priority inspection |
| yellow | Near hit areas, no direct signs | Monitor |
| green | No signs | Nothing urgent |

## Sample file

`tests/fixtures/buildings_fake.geojson` has 10 fictitious buildings that follow this schema, including nulls. Use it to build the app before real data exists.
