# data/

This folder is not tracked by Git, except this file. Copy the inputs from the team Drive (Data/AI folder) into the paths below.

## osm/ (buildings and area of interest, Kharkiv)

| File | Content |
|---|---|
| `buildings_final.geojson` | 86,519 OSM buildings with `area_m2`, `levels`, `peste_400_m2`, GHSL height and epoch, `nr_puncte_unosat`. Main buildings file |
| `final_data.geojson` | Same buildings with a different GHSL version (`ghsl_anbh_mean`, `ghsl_age_majority`, `ghsl_age_period`). The epochs disagree with `buildings_final.geojson`; to be decided by Data/AI |
| `kharkiv_aoi.geojson` | Area of interest: footprint of the WorldView image of 15 Jun 2022 |
| `kharkiv_buildings.geojson` | Older version, includes the AOI polygon as a row. Not used |
| `kharkiv_buildings_osm_ready_v2.geojson` | Oldest version, without GHSL. Not used |

## unosat/ (ground truth, Kharkiv)

| File | Content |
|---|---|
| `damage_points.gpkg` | 520 UNOSAT damage points, layer `Kharkiv_Damage_Points`, sensor date 24 Apr 2022. Classes are numeric codes. The layer `Area_Of_Interest` in this file is wrong: it spans most of eastern Ukraine |
| `Kharkiv_CDA_20220615/` | Shapefile with 894 points and several assessments per row. Main assessment, 15 Jun 2022 |
| `*.pdf` | UNOSAT maps for 15 Jun 2022 (748 structures classified) and 17 Oct 2022 (49 structures highlighted) |

## Data/AI deliveries (Saltivka, put directly in `data/`)

| File | Content |
|---|---|
| `saltivka_pwtt_10m.tif` | PWTT raster, one band `pwtt_score`, EPSG:4326, 10 m pixels. Values range 0-26 (raw score, not 0-1). About 68% of pixels are empty, and in a sample of 300 buildings inside its extent 170 had no valid pixel |
| `saltivka_pwtt.qgz` | QGIS project with the raster |
| `saltivka_typology_v0.geojson` | 7,961 Saltivka buildings with `typology_estimated`, `typology_rule` and `vuln_index_v0`. 2,228 are 400 m2 or larger; of those about 70% are `unknown` and only 676 have `vuln_index_v0`. Uses the GHSL version of `final_data.geojson`. Building ids have no `osm_` prefix |

## Generated

| File | Content |
|---|---|
| `buildings.geojson` | Output of `python -m pipeline.run_all`: 15,811 Kharkiv buildings of 400 m2 or larger, in the schema of `docs/schema.md`. Fields from steps 03 to 06 are `null` for now |

## Known limits

- Only about 28% of the 520 UNOSAT points fall within 10 m of a building of 400 m2 or larger (22% fall inside one). Most damage points are on smaller buildings, so validation on the large buildings uses about 145 points.
- The raster and the typology cover Saltivka only, while `buildings.geojson` covers the whole city.

## Source

UNOSAT damage assessments, via UNOSAT maps for Ukraine and HDX (CC BY-SA). Buildings from OpenStreetMap, height and epoch from GHSL.
