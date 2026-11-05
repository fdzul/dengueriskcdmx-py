# dengueriskcdmx (Python)

Data and rasters supporting the **Risk Map of Dengue Transmission in the Metropolitan Area of Mexico City**. Python version of the R package [`dengueriskcdmx`](https://github.com/fdzul/dengueriskcdmx); it ships the same data sets and rasters.

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

Each data set has the class (`presence` / `pseudoabs`), nine predictors (`built`, `tree`, `ndvi`, `prcp`, `ia`, `ice`, `im`, `pop`, `hfp`) and the point geometry (EPSG:4326). The partition is 80/20, stratified by class, with seed 12345.

The rasters (about 500 m) are derived from the consensus (mean of the probabilities) of Random Forest, LightGBM and XGBoost models: `"aedes"` = probability of *Ae. aegypti* occurrence; `"dengue"` = probability of confirmed imported dengue cases; `"risk"` = two bands, `cluster` (k-means) and `risk` (five-level epidemiological risk).

## Example

```python
import dengueriskcdmx as dr

x = dr.load_ae_aegypti("train")
print(x["class"].value_counts())

with dr.read_raster("risk") as r:
    risk = r.read(2)
```

## Data availability

The ovitrap data are included. The data on confirmed dengue cases used to fit the case model are **not** published; only the derived probability and risk rasters are provided. The Quarto code of the machine-learning workflow is in the vignettes of the R package.

## License

MIT.
