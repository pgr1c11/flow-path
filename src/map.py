from src.results import MapResults
from src.controls import Controls
from src.cell import Cell
from src.path import Path
from src.flow import Flow
from typing import List, Tuple


class Map:
    def __init__(self, controls: Controls) -> None:
        self.__controls = controls
        self.results: MapResults
        self.temp: List[Flow]

    def from_whole_dem(self) -> None:
        pass

    def from_box(
        self, top_left_coords: Tuple[int, int], bottom_right_coords: Tuple[int, int]
    ) -> None:
        rows = list(range(top_left_coords[0], bottom_right_coords[0]))
        cols = list(range(top_left_coords[1], bottom_right_coords[1]))
        cells = [
            Cell(controls=self.__controls, coords=(r, c)) for r in rows for c in cols
        ]
        flows = [Flow(controls=self.__controls, start_cell=cell) for cell in cells]
        self.temp = flows

    def from_raster(self) -> None:
        pass

    def from_points(self) -> None:
        pass
