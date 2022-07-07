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
        self.Cells = [[start_cell]]
        self.cells_probs = [[1]]

    def __length(self, current_cell: Cell) -> float:
        r_diff = abs(self.Cells[0][0].coords[0] - current_cell.coords[0]) * self.__controls.dem.resolution[0]
        c_diff = abs(self.Cells[0][0].coords[1] - current_cell.coords[1]) * self.__controls.dem.resolution[0]
        return ((r_diff**2) + (c_diff**2)) ** 0.5

    def __angle(self, current_cell: Cell, path_length: float) -> float:
        elev_diff = self.Cells[0][0].value - current_cell.value
        tan_a = elev_diff / path_length
        rad_a = np.arctan(tan_a)
        return (rad_a * 180) / np.pi

    def __get_valid_step_cells_idx(self, current_cell: Cell) -> list:
        return [i
            for i in range(len(current_cell.neighbour_yis))
            if current_cell.neighbour_yis[i] > 0
            and ((current_cell.max_yis > 1 and current_cell.neighbour_yis[i] == current_cell.max_yis)
            or current_cell.neighbour_yis[i] >= (current_cell.max_yis ** self.__controls.divergent_flow)
            )]

    def __get_persistence_factor(self, current_cell: Cell, valid_step_cells_idx: list) -> float:
        first_step = True if current_cell.previous_direction_idx == 0 else False
        same_direction = current_cell.previous_direction_idx in valid_step_cells_idx
        return self.__controls.persistence if not first_step and same_direction else 1

    def __get_next_cells_prob_all(self, current_cell: Cell) -> list:
        valid_step_cells_idx = self.__get_valid_step_cells_idx(current_cell=current_cell)
        p = self.__get_persistence_factor(current_cell=current_cell, valid_step_cells_idx=valid_step_cells_idx)      
        
        prob_valid_steps = [(current_cell.neighbour_tan_slopes[i] * p) / current_cell.neighbour_tan_slopes_sum
            for i in valid_step_cells_idx]

        prob_cells = [0.0] * len(current_cell.neighbour_coords)
        for i in range(len(valid_step_cells_idx)):
            prob_cells[valid_step_cells_idx[i]] = prob_valid_steps[i]

        return prob_cells

    def __get_next_cells_prob(self, next_cells_prob_all: list) -> list:
        return [i for i in next_cells_prob_all if i > 0]

    def __get_next_cells_ids(self, current_cell: Cell, next_cells_prob_all: list) -> list:
        return [current_cell.neighbour_coords[i] for i in range(len(next_cells_prob_all)) if next_cells_prob_all[i] > 0]

    def __get_previous_directions(self, next_cells_prob_all: list) -> list:
        return [i for i in range(len(next_cells_prob_all)) if next_cells_prob_all[i] > 0]

    def __get_next_Cells(self, next_cell_ids: list, previous_directions: list) -> list:
        return [Cell(controls=self.__controls,
                coords=next_cell_ids[i],
                previous_direction=previous_directions[i])
            for i in range(len(next_cell_ids))]

    def run(self) -> None:
        step = 0


        while all([
            step < self.__controls.max_n_steps,
            ]):
            pass


