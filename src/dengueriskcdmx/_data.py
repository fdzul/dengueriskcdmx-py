"""Loaders for the data shipped with the package (same objects as the R package)."""

from __future__ import annotations

from importlib import resources
from pathlib import Path

import geopandas as gpd
import pandas as pd

_RASTERS = {
    "aedes": "ae_aegypti_probability.tif",
    "dengue": "dengue_probability.tif",
    "risk": "epidemiological_risk.tif",
}
_SPLITS = ("all", "train", "test", "external")
_CLASS_LEVELS = ["presence", "pseudoabs"]


def _data_dir() -> Path:
    return Path(str(resources.files("dengueriskcdmx").joinpath("data")))


def _file(name: str) -> Path:
    p = _data_dir() / name
    if not p.exists():
        raise FileNotFoundError(
            f"file not found in the installed package: {name}. "
            "Run scripts/export_from_R.R and copy the output into src/dengueriskcdmx/data/."
        )
    return p


def load_aoi() -> gpd.GeoDataFrame:
    """Study area (Mexico City Metropolitan Area), polygon in WGS 84."""
    return gpd.read_file(_file("aoi.gpkg"))


def load_ae_aegypti(split: str = "all") -> gpd.GeoDataFrame:
    """Aedes aegypti ovitrap presences and pseudo-absences.

    Parameters
    ----------
    split : {"all", "train", "test", "external"}
        "all": full 2017-2024 database (column ``split`` marks train/test);
        "train": 80% training partition; "test": 20% test partition;
        "external": 2025 external validation data.

    Columns: ``class`` (categorical: presence / pseudoabs), nine predictors
    (``built``, ``tree``, ``ndvi``, ``prcp``, ``ia``, ``ice``, ``im``, ``pop``,
    ``hfp``) and the point geometry (EPSG:4326).
    """
    if split not in _SPLITS:
        raise ValueError(f"split must be one of {_SPLITS}, got {split!r}")
    if split == "external":
        d = gpd.read_file(_file("ae_aegypti_2025.gpkg"))
    else:
        d = gpd.read_file(_file("ae_aegypti_2017_2024.gpkg"))
        if split in ("train", "test"):
            d = d[d["split"] == split].drop(columns="split").reset_index(drop=True)
    d["class"] = pd.Categorical(d["class"], categories=_CLASS_LEVELS)
    return d


def ae_raster_path(layer: str = "aedes") -> str:
    """Path to a GeoTIFF shipped with the package.

    ``layer``: "aedes" (probability of Ae. aegypti occurrence), "dengue"
    (probability of confirmed imported dengue cases) or "risk" (five-level
    epidemiological risk; bands ``cluster`` and ``risk``).
    """
    if layer not in _RASTERS:
        raise ValueError(f"layer must be one of {tuple(_RASTERS)}, got {layer!r}")
    return str(_file(_RASTERS[layer]))


def read_raster(layer: str = "aedes"):
    """Open a shipped raster with rasterio (about 500 m). Use as a context manager::

        with read_raster("risk") as r:
            risk = r.read(2)

    "aedes" and "dengue" hold the probability (0-1), the mean of the Random Forest,
    LightGBM and XGBoost models. "risk" has two bands: ``cluster`` (k-means cluster)
    and ``risk`` (five-level epidemiological risk). Requires ``rasterio``
    (``pip install dengueriskcdmx[raster]``).
    """
    try:
        import rasterio
    except ImportError as e:  # pragma: no cover
        raise ImportError("rasterio is required to read the rasters: pip install dengueriskcdmx[raster]") from e
    return rasterio.open(ae_raster_path(layer))
