# Quick Start

```python
import dengueriskcdmx as dr

x = dr.load_ae_aegypti("train")
print(x["class"].value_counts())

with dr.read_raster("risk") as r:
    risk = r.read(2)
```

Each data set has the class (`presence` / `pseudoabs`), nine predictors (`built`, `tree`, `ndvi`, `prcp`, `ia`, `ice`, `im`, `pop`, `hfp`) and the point geometry (EPSG:4326). The partition is 80/20, stratified by class, with seed 12345.
