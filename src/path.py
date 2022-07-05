import numpy as np
from src.results import PathResults
from src.controls import Controls
from src.cell import Cell

class Path:
    def __init__(
        self,
        controls: Controls,
        start_cell: Cell
        ) -> None:

        self.__controls = controls
        self.__start_cell = start_cell
        self.affected_coords = [start_cell.coords]

    def __length(self, current_cell: Cell) -> float:
        r_diff = abs(self.__start_cell.coords[0] - current_cell.coords[0]) * self.__controls.dem.resolution[0]
        c_diff = abs(self.__start_cell.coords[1] - current_cell.coords[1]) * self.__controls.dem.resolution[0]
        return ((r_diff**2) + (c_diff**2)) ** 0.5

    def __angle(self, current_cell: Cell, path_length: float) -> float:
        elev_diff = self.__start_cell.value - current_cell.value
        tan_a = elev_diff / path_length
        rad_a = np.arctan(tan_a)
        return (rad_a * 180) / np.pi

    def run(self) -> None:
        step = 0
        on_boundary = self.__start_cell.on_boundary
        is_sink = self.__start_cell.is_sink
        path_length = 0
        path_angle = 90

        while all([
            step < self.__controls.max_n_steps,
            not on_boundary,
            not is_sink,
            path_length < self.__controls.max_length,
            path_angle > self.__controls.fahrboschung_angle
            ]):
            pass


