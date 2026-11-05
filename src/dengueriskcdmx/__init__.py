"""dengueriskcdmx: data and rasters for the dengue transmission risk map of the
Mexico City Metropolitan Area (Python version of the R package of the same name)."""

from ._data import (
    ae_raster_path,
    load_ae_aegypti,
    load_aoi,
    read_raster,
)

__version__ = "0.1.0"
__all__ = ["load_aoi", "load_ae_aegypti", "ae_raster_path", "read_raster", "__version__"]
