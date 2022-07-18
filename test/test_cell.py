import sys
import os
import numpy as np
import pytest as pt

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT_DIR))
from src.dem import Dem, DemTif, DemDummy
from src.controls import Controls
from src.cell import Cell

np.random.seed(0)
test_dem = DemDummy(dimensions=(3, 3))
test_controls = Controls(
    dem=test_dem,
    slope_threshold=45,
    divergent_flow=2,
    persistence=1,
    horizontal_flow=True,
    fahrboschung_angle=5,
    max_n_steps=1000,
    max_length=2000,
    paths_per_flow=50,
)
test_cell = Cell(controls=test_controls, coords=(1, 1))


def test___neighbour_coords(test_cell: Cell = test_cell):
    coords = test_cell.neighbour_coords
    assert coords == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]


def test___neighbour_values(test_cell: Cell = test_cell):
    neighbour_values = test_cell.neighbour_values
    np.testing.assert_almost_equal(
        neighbour_values,
        [
            0.0,
            26.000393020918054,
            54.8936899205287,
            0.0,
            45.113610600617946,
            0.0,
            24.621606979255755,
            49.48390574103221,
        ],
    )


def test___on_boundary(test_cell: Cell = test_cell):
    boundary_test_cell = Cell(controls=test_controls, coords=(0, 0))
    assert test_cell.on_boundary == False
    assert boundary_test_cell.on_boundary == True


def test___current_cell_value(test_cell: Cell = test_cell):
    cell_value = test_cell.value
    assert cell_value == pt.approx(29.668894975374922)


def test___is_sink(test_cell: Cell = test_cell):
    test_dem_force_sink = test_dem
    test_dem_force_sink.dem = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    test_controls_force_sink = test_controls
    test_controls_force_sink.dem = test_dem_force_sink
    test_cell_force_sink = Cell(controls=test_controls_force_sink, coords=(1, 1))
    assert test_cell_force_sink.is_sink == True
    assert test_cell.is_sink == False


def test___neighbour_tan_slopes(test_cell: Cell = test_cell):
    neighbour_tan_slopes = test_cell.neighbour_tan_slopes
    neighbour_tan_slopes_no_None = [i for i in neighbour_tan_slopes if i is not None]
    np.testing.assert_almost_equal(
        neighbour_tan_slopes_no_None,
        [
            29.668894975374922,
            3.668501954456868,
            29.668894975374922,
            29.668894975374922,
            5.047287996119167,
        ],
    )
    neighbour_tan_slopes_None = [i for i in neighbour_tan_slopes if i is None]
    assert len(neighbour_tan_slopes_None) == 3


def test___neighbour_yis(test_cell: Cell = test_cell):
    neighbour_yis = test_cell.neighbour_yis
    np.testing.assert_almost_equal(
        neighbour_yis,
        [
            29.668894975374926,
            3.6685019544568687,
            0,
            29.668894975374926,
            0,
            29.668894975374926,
            5.0472879961191675,
            0,
        ],
    )
