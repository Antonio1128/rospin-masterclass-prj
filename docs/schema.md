# Building schema

Contract between Data/AI and Development. Every building in `buildings.geojson` is one GeoJSON Feature (Polygon) with these properties. A field that is not computed yet is `null`, and the app must work with nulls.

Geometry is stored in EPSG:4326. Areas and distances are computed in EPSG:32637 (metres).

| Field | Type | Example | Filled by | Pipeline step |
|---|---|---|---|---|
| building_id | string | osm_123456 | Data/AI | 2 |
| area_m2 | number | 1250 | Data/AI | 2 |
| levels | integer | 9 | Data/AI | 2 |
| height_m | number | 27.0 | Data/AI | 2 |
| epoch | string | 1975-1990 | Data/AI | 2 |
| typology | string | panel_block | Data/AI | 6 |
| vuln_score | number 0-1 | 0.6 | Data/AI | 6 |
| damage_score | number 0-1 | 0.82 | Data/AI | 3 |
| unosat_label | string | destroyed | Data/AI | 4 |
| insar_disp_mm | number | -7.5 | Data/AI | 5 |
| insar_n_points | integer | 14 | Data/AI | 5 |
| exposure_score | number 0-1 | 0.4 | Data/AI | 6 |
| triage_status | red / orange / yellow / green | red | Data/AI | 6 |
| cost_estimate_usd | number | 1850000 | Data/AI | 6 |

## Triage status

| Value | Meaning | Action |
|---|---|---|
| red | Destroyed | Nobody enters |
| orange | Standing, but moving or highly exposed | Priority inspection |
| yellow | Near hit areas, no direct signs | Monitor |
| green | No signs | Nothing urgent |

## Sample file

`tests/fixtures/buildings_fake.geojson` has 10 fictitious buildings that follow this schema, including nulls. Use it to build the app before real data exists.
