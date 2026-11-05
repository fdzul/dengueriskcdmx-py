<div class="hero" markdown>
<img src="assets/logo.png" alt="dengueriskcdmx hexagon logo">
</div>

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](license.md)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.9-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/dengueriskcdmx?logo=pypi&logoColor=white)](https://pypi.org/project/dengueriskcdmx/)
[![R package](https://img.shields.io/badge/R%20package-dengueriskcdmx-276DC3?logo=r&logoColor=white)](https://fdzul.github.io/dengueriskcdmx/)
[![GitHub](https://img.shields.io/badge/GitHub-fdzul%2Fdengueriskcdmx--py-181717?logo=github)](https://github.com/fdzul/dengueriskcdmx-py)

# dengueriskcdmx

Data and rasters supporting the **Risk Map of Dengue Transmission in the Metropolitan Area of Mexico City**. This is the Python version of the R package [`dengueriskcdmx`](https://fdzul.github.io/dengueriskcdmx/); it ships the same data sets and rasters.

## Installation

```bash
pip install dengueriskcdmx            # data loaders (GeoPandas)
pip install "dengueriskcdmx[raster]"  # plus rasterio, to read the rasters
```

## What is included

| Function | Returns |
|---|---|
| `load_ae_aegypti("all")` | *Ae. aegypti* ovitrap presences and pseudo-absences, 2017-2024, with the `split` column (train / test) |
| `load_ae_aegypti("train")` / `("test")` | Training (80%) and test (20%) partitions |
| `load_ae_aegypti("external")` | External validation data, 2025 |
| `load_aoi()` | Study area (Mexico City Metropolitan Area) |
| `ae_raster_path(layer)` / `read_raster(layer)` | Path to / open GeoTIFF of `"aedes"`, `"dengue"` or `"risk"` |

!!! note "Data availability"
    The ovitrap data are included. The data on confirmed dengue cases used to fit the case model are **not** published; only the derived probability and risk rasters are provided.
