import numpy as np
import rasterio
from rasterio.mask import mask

from pipeline.common import DATA, ensure_schema

RASTER = DATA / "saltivka_pwtt_10m.tif"
PERCENTILE = 90
SCORE_AT_FULL_DAMAGE = 6.0


def pixel_values(raster, geometry):
    try:
        masked, _ = mask(raster, [geometry], crop=True, all_touched=True, filled=False)
    except ValueError:
        return np.array([])
    values = masked[0].compressed()
    return values[~np.isnan(values)]


def damage_score(values):
    if values.size == 0:
        return None
    return float(np.clip(np.percentile(values, PERCENTILE) / SCORE_AT_FULL_DAMAGE, 0, 1))


def run(buildings):
    if not RASTER.exists():
        return ensure_schema(buildings)
    with rasterio.open(RASTER) as raster:
        scores = [damage_score(pixel_values(raster, geometry)) for geometry in buildings.to_crs(raster.crs).geometry]
    scored = buildings.copy()
    scored["damage_score"] = scores
    return ensure_schema(scored)
