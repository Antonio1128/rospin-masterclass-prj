# re:build (DOCORO)

ROSPIN Satellite Data Processing Masterclass 2026 - Enterprise Software track, Defense domain.

A map of the large buildings in a bombed city (demo: Kharkiv) where each building gets a triage colour: red (destroyed), orange (standing, priority inspection), yellow (monitor), green (nothing urgent), plus an estimated reconstruction cost. Built from free Sentinel-1 radar data and public building data.

## Repository layout

| Folder | Content |
|---|---|
| `pipeline/` | One script per step, run in order, building `buildings.geojson` end to end: `01_aoi`, `02_buildings`, `03_damage`, `04_validate`, `05_triage.py` |
| `app/` | Streamlit app that reads `buildings.geojson` |
| `docs/schema.md` | Per-building fields, the contract between Data/AI and Development |
| `notebooks/` | Exploration; final code moves to `pipeline/` |
| `tests/` | pytest suite and fixtures |
| `data/` | Local inputs, not in Git. See `data/README.md` |

## Setup

Python 3.11.

```
pip install -r requirements.txt
```

You do not need any keys to run the app or the pipeline as it is now. Keys are only needed to regenerate the satellite results: step 03 (PWTT on Earth Engine) needs `GEE_PROJECT`. In that case put them in a `.env` file in the project root (it is gitignored):

```
GEE_PROJECT=your-earth-engine-project
```

Never commit keys, tokens or service-account files.

## Run the app

```
streamlit run app/main.py
```

It opens at http://localhost:8501 and currently shows 10 fictitious buildings from `tests/fixtures/buildings_fake.geojson`. Click a building to see its card, and use the sidebar to filter by triage colour.

## Run the pipeline

```
python -m pipeline.run_all
```

Runs steps 02 to 05 in order and writes `data/output/buildings.geojson`. Each step is a module in `pipeline/` with a `run(buildings)` function that takes the buildings table and returns it with its fields filled in. Step 02 reads `data/in_use/buildings_osm_ghsl.geojson`, keeps buildings of at least 400 m2 and converts them to the schema. Height and epoch come from GHSL (a height of 0 counts as missing); levels fall back to the GHSL height divided by 3. The epoch is the dominant one of the GHSL cell, not the age of the building. Step 03 reads `data/in_use/pwtt_raster_saltivka_10m.tif` and sets `damage_score` to the 90th percentile of the PWTT pixels inside each building, divided by 6 and clipped to 0-1. The divisor is provisional until Data/AI confirms the scale and threshold. Buildings outside the raster keep `damage_score` as `null`. Steps 04 and 05 pass the data through unchanged for now, and their fields stay `null`.

If `data/output/buildings.geojson` is open in QGIS the run fails when writing it. Close the layer first.

## Data contract

Every building is a GeoJSON Feature (Polygon) with these properties. Fields that are not computed yet are `null`, and the app must handle that. Geometry is stored in EPSG:4326; areas and distances are computed in EPSG:32637.

| Field | Type | Example | Filled by | Step |
|---|---|---|---|---|
| building_id | string | osm_123456 | Data/AI | 2 |
| area_m2 | number | 1250 | Data/AI | 2 |
| levels | integer | 9 | Data/AI | 2 |
| height_m | number | 27.0 | Data/AI | 2 |
| epoch | string | 1975-1990 | Data/AI | 2 |
| typology | string | panel_block | Data/AI | 5 |
| vuln_score | number 0-1 | 0.6 | Data/AI | 5 |
| damage_score | number 0-1 | 0.82 | Data/AI | 3 |
| unosat_label | string | destroyed | Data/AI | 4 |
| exposure_score | number 0-1 | 0.4 | Data/AI | 5 |
| triage_status | red / orange / yellow / green | red | Data/AI | 5 |
| cost_estimate_usd | number | 1850000 | Data/AI | 5 |

Triage colours: red = destroyed, orange = standing and highly exposed (priority inspection), yellow = near hit areas (monitor), green = no signs.

The same table, with more detail, lives in [docs/schema.md](docs/schema.md). Keep both in sync when a field changes.

## Tests

```
pytest
```

## Working on the project

- One branch per feature, for example `feat/pipeline-run-all`, merged into `main` through a pull request.
- `main` must always work. Do not push to it directly.
- Add files by name, not with `git add .`.

## Status

| Part | State |
|---|---|
| Repo structure, schema, fake sample data | Done |
| Streamlit map on fake data | Done |
| Pipeline runner and step 02 (real Kharkiv buildings, 15,811 above 400 m2) | Done |
| Pipeline step 03 (damage score from the PWTT raster, 2,240 of 15,811 buildings scored) | Done, scale provisional |
| Pipeline steps 04-05 (validation, triage) | Pass-through |
| Online deploy, export, "Data and limitations" page | Not started |
