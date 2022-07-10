import numpy as np
from src.results import PathResults
from src.controls import Controls
from src.cell import Cell
from src.step import Step

class Path:
    def __init__(
        self,
        controls: Controls,
        start_cell: Cell
        ) -> None:
        self.__controls = controls
        self.start_cell = start_cell
        self.results = self.__run()

    def __length(self, current_cell: Cell) -> float:
        r_diff = abs(self.start_cell.coords[0] - current_cell.coords[0]) * abs(self.__controls.dem.resolution[0])
        c_diff = abs(self.start_cell.coords[1] - current_cell.coords[1]) * abs(self.__controls.dem.resolution[0])
        return ((r_diff**2) + (c_diff**2)) ** 0.5

    def __angle(self, current_cell: Cell, path_length: float) -> float:
        elev_diff = self.start_cell.value - current_cell.value
        tan_a = elev_diff / path_length
        rad_a = np.arctan(tan_a)
        return (rad_a * 180) / np.pi

    def __run(self) -> PathResults:
        cell = self.start_cell
        length = self.__length(current_cell=cell)
        angle = 90
        sink = cell.is_sink
        on_boundary = cell.on_boundary
        affected_cells = [cell.coords]
        i = 0
        while all([
            i < self.__controls.max_n_steps,
            length < self.__controls.max_length,
            angle > self.__controls.fahrboschung_angle,
            not sink,
            not on_boundary]):

            step = Step(controls=self.__controls,
                from_cell=cell)
            
            cell = step.to_cell
            length = self.__length(current_cell=cell)
            angle = self.__angle(current_cell=cell, path_length=length)
            sink = cell.is_sink
            on_boundary = cell.on_boundary
            affected_cells.append(cell.coords)
            i = i + 1
        return PathResults(
            controls=self.__controls,
            affected_cells=affected_cells)