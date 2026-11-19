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

## Source

UNOSAT damage assessments, via UNOSAT maps for Ukraine and HDX (CC BY-SA). Buildings from OpenStreetMap, height and epoch from GHSL.
