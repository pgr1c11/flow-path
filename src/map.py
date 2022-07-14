from typing import List, Tuple
import collections
import functools
import operator
from src.results import MapResults
from src.controls import Controls
from src.cell import Cell
from src.flow import Flow


class Map:
    def __init__(self, controls: Controls) -> None:
        self.__controls = controls
        self.results: MapResults

    def from_whole_dem(self) -> None:
        pass

    def __combine_flows(self, flows: List[Flow]) -> dict:
        flow_dict = [
            {
                f.results.affected_cells[i]: f.results.cell_values[i]
                for i in range(len(f.results.affected_cells))
            }
            for f in flows
        ]
        return dict(functools.reduce(operator.add, map(collections.Counter, flow_dict)))

    def from_box(
        self, top_left_coords: Tuple[int, int], bottom_right_coords: Tuple[int, int]
    ) -> None:
        rows = list(range(top_left_coords[0], bottom_right_coords[0]))
        cols = list(range(top_left_coords[1], bottom_right_coords[1]))
        cells = [
            Cell(controls=self.__controls, coords=(r, c)) for r in rows for c in cols
        ]
        flows = [Flow(controls=self.__controls, start_cell=cell) for cell in cells]
        collapsed_flows = self.__combine_flows(flows=flows)
        affected_cells = list(collapsed_flows.keys())
        cell_values = list(collapsed_flows.values())
        self.results = MapResults(
            controls=self.__controls,
            affected_cells=affected_cells,
            cell_values=cell_values,
        )

    def from_raster(self) -> None:
        pass

    def from_points(self) -> None:
        pass
