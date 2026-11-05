# Data

| Layer | Content |
|---|---|
| `"aedes"` | Probability of *Ae. aegypti* occurrence |
| `"dengue"` | Probability of confirmed imported dengue cases |
| `"risk"` | Two bands: `cluster` (k-means) and `risk` (five-level epidemiological risk) |

The rasters (about 500 m) are derived from the consensus (mean of the probabilities) of Random Forest, LightGBM and XGBoost models.
