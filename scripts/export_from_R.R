# export_from_R.R  -- run in R (Mac) with the R package dengueriskcdmx installed.
# Writes the data sets as GeoPackage and copies the three GeoTIFF rasters into the data folder
# of the Python package.  Usage:  Rscript export_from_R.R <path to dengueriskcdmx_py>
args <- commandArgs(trailingOnly = TRUE)
out  <- file.path(path.expand(args[1]), "src", "dengueriskcdmx", "data")
stopifnot(dir.exists(out))
suppressMessages({ library(sf); library(dengueriskcdmx) })

full <- ae_aegypti_2017_2024
# consistency checks: the partitions are subsets of the full database
stopifnot(nrow(ae_aegypti_2017_2024_train) == sum(full$split == "train"),
          nrow(ae_aegypti_2017_2024_test)  == sum(full$split == "test"))
full$class <- as.character(full$class)
ext  <- ae_aegypti_2025; ext$class <- as.character(ext$class)

st_write(full, file.path(out, "ae_aegypti_2017_2024.gpkg"), layer = "ae_aegypti_2017_2024", delete_dsn = TRUE, quiet = TRUE)
st_write(ext,  file.path(out, "ae_aegypti_2025.gpkg"),      layer = "ae_aegypti_2025",      delete_dsn = TRUE, quiet = TRUE)
st_write(aoi,  file.path(out, "aoi.gpkg"),                  layer = "aoi",                  delete_dsn = TRUE, quiet = TRUE)

for (l in c("aedes", "dengue", "risk")) file.copy(ae_raster_path(l), out, overwrite = TRUE)
cat("rows: full", nrow(full), "| train", sum(full$split == "train"), "| test", sum(full$split == "test"),
    "| 2025", nrow(ext), "\n")
print(list.files(out))
