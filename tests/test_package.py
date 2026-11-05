import pytest
import dengueriskcdmx as d


def test_aoi(datos_sinteticos):
    a = d.load_aoi()
    assert len(a) == 1 and a.crs.to_epsg() == 4326


def test_splits_consistentes(datos_sinteticos):
    full, tr, te = d.load_ae_aegypti("all"), d.load_ae_aegypti("train"), d.load_ae_aegypti("test")
    assert len(tr) == (full["split"] == "train").sum() and len(te) == (full["split"] == "test").sum()
    assert len(tr) + len(te) == len(full)
    assert "split" not in tr.columns and "split" not in te.columns


def test_clase_categorica(datos_sinteticos):
    x = d.load_ae_aegypti("external")
    assert list(x["class"].cat.categories) == ["presence", "pseudoabs"]
    assert len(x) == 5


def test_argumentos_invalidos(datos_sinteticos):
    with pytest.raises(ValueError):
        d.load_ae_aegypti("otro")
    with pytest.raises(ValueError):
        d.ae_raster_path("otro")


def test_rasters(datos_sinteticos):
    for layer, bandas in (("aedes", 1), ("dengue", 1), ("risk", 2)):
        with d.read_raster(layer) as r:
            assert r.count == bandas


def test_archivo_faltante(tmp_path, monkeypatch):
    import dengueriskcdmx._data as m
    monkeypatch.setattr(m, "_data_dir", lambda: tmp_path)
    with pytest.raises(FileNotFoundError):
        d.load_aoi()
