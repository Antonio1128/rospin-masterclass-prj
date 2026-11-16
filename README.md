# re:build (DOCORO)

ROSPIN Satellite Data Processing Masterclass 2026 - Enterprise Software track, Defense domain.

A map of the large buildings in a bombed city (demo: Kharkiv) where each building gets a triage colour: red (destroyed), orange (standing, priority inspection), yellow (monitor), green (nothing urgent), plus an estimated reconstruction cost. Built from free Sentinel-1 radar data and public building data.

## Repository layout

| Folder | Content |
|---|---|
| `pipeline/` | One script per step, run in order, building `buildings.geojson` end to end: `01_aoi`, `02_buildings`, `03_damage`, `04_validate`, `05_insar`, `06_triage` |
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

Copy your keys into a `.env` file in the project root (it is gitignored). `EARTHDATA_*` is only needed for the InSAR step:

```
GEE_PROJECT=your-earth-engine-project
EARTHDATA_USERNAME=...
EARTHDATA_PASSWORD=...
```

Never commit keys, tokens or service-account files.

## Run the app

```
streamlit run app/main.py
```

It opens at http://localhost:8501 and currently shows 10 fictitious buildings from `tests/fixtures/buildings_fake.geojson`. Click a building to see its card, and use the sidebar to filter by triage colour.

## Data contract

Every building is a GeoJSON Feature with the fields in [docs/schema.md](docs/schema.md). Fields that are not computed yet are `null`, and the app must handle that. Geometry is stored in EPSG:4326; areas and distances are computed in EPSG:32637.

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
| Pipeline steps 01-06 | Stubs only |
| Real buildings and damage scores | Not started |
| Online deploy, export, "Data and limitations" page | Not started |
