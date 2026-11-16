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

```
pip install -r requirements.txt
```

Copy your keys into a `.env` file in the project root (it is gitignored):

```
GEE_PROJECT=your-earth-engine-project
EARTHDATA_USERNAME=...
EARTHDATA_PASSWORD=...
```

## Tests

```
pytest
```
