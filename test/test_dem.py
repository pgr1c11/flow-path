import sys
import os
import numpy as np
import pytest as pt

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT_DIR))
from src.dem import Dem, DemTif, DemDummy

test_dem_tif_path = os.path.join(ROOT_DIR, "test", "test_dem.tif")
test_dem_tif = DemTif(path=test_dem_tif_path)


def test__boundary(test_dem_tif: Dem = test_dem_tif):
    boundary = test_dem_tif.boundary
    assert boundary[8, 8] == 1


def test___get_resolution(test_dem_tif: Dem = test_dem_tif):
    resolution = test_dem_tif.resolution
    assert resolution == (2.0, -2.0)


def test___get_origin(test_dem_tif: Dem = test_dem_tif):
    origin = test_dem_tif.origin
    assert origin == ((465002, 154998))


def test___get_crs(test_dem_tif: Dem = test_dem_tif):
    assert len(test_dem_tif.crs) == 653


def test__load_tif():
    test_load = DemTif(path=test_dem_tif_path)
    test_load_shape = test_load.dem.shape
    assert test_load_shape == (9.0, 9.0)


def test_xy_coord_from_map_coords_tif(test_dem_tif: DemTif = test_dem_tif):
    test_xy_coord = test_dem_tif.xy_coord_from_map_coords(
        map_coords=(465004.32, 154993.52)
    )
    assert test_xy_coord == (2, 1)


def test__load_dummy():
    np.random.seed(0)
    test_dummy = DemDummy(dimensions=(3, 3))
    assert test_dummy.dem[2, 2] == pt.approx(49.4839)
