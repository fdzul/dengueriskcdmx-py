"""Fixtures: synthetic data with the same structure as the real data, to test the loaders."""
import numpy as np
import pytest
import geopandas as gpd
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import Point, box

import dengueriskcdmx._data as _data

PRED = ["built", "tree", "ndvi", "prcp", "ia", "ice", "im", "pop", "hfp"]


def _puntos(n, split=None, seed=0):
    rng = np.random.default_rng(seed)
    d = gpd.GeoDataFrame(
        {"class": rng.choice(["presence", "pseudoabs"], n), **{p: rng.random(n) for p in PRED}},
        geometry=[Point(-99.2 + rng.random(), 19.3 + rng.random()) for _ in range(n)], crs=4326)
    if split is not None:
        d["split"] = split
    return d


@pytest.fixture
def datos_sinteticos(tmp_path, monkeypatch):
    split = ["train"] * 8 + ["test"] * 2
    _puntos(10, split).to_file(tmp_path / "ae_aegypti_2017_2024.gpkg", driver="GPKG")
    _puntos(5, seed=1).to_file(tmp_path / "ae_aegypti_2025.gpkg", driver="GPKG")
    gpd.GeoDataFrame({"id": [1]}, geometry=[box(-99.3, 19.2, -98.9, 19.7)], crs=4326).to_file(
        tmp_path / "aoi.gpkg", driver="GPKG")
    for f, bands in (("ae_aegypti_probability.tif", 1), ("dengue_probability.tif", 1), ("epidemiological_risk.tif", 2)):
        with rasterio.open(tmp_path / f, "w", driver="GTiff", height=4, width=4, count=bands, dtype="float32",
                           crs="EPSG:4326", transform=from_origin(-99.3, 19.7, 0.1, 0.1)) as r:
            for b in range(bands):
                r.write(np.random.default_rng(b).random((4, 4)).astype("float32"), b + 1)
    monkeypatch.setattr(_data, "_data_dir", lambda: tmp_path)
    return tmp_path
