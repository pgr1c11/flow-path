import random
from src.controls import Controls
from src.cell import Cell

class Step:
    def __init__(
        self,
        controls: Controls,
        from_cell: Cell
        ) -> None:
        self.__controls = controls
        self.from_cell = from_cell
        __to_cell_probs = self.__to_cell_probs()
        __to_cell_idx = self.__to_cell_idx(to_cell_probs=__to_cell_probs)
        self.to_cell = self.__to_Cell(to_cell_idx=__to_cell_idx)

    def __valid_step_cells_idx(self) -> list:
        return [i
            for i in range(len(self.from_cell.neighbour_yis))
            if self.from_cell.neighbour_yis[i] > 0
            and((self.from_cell.max_yis > 1
            and self.from_cell.neighbour_yis[i] == self.from_cell.max_yis)
            or self.from_cell.neighbour_yis[i] >= (self.from_cell.max_yis ** self.__controls.divergent_flow))]

    def __persistence_factor(self, valid_step_cells_idx: list) -> float:
        first_step = True if self.from_cell.previous_direction_idx == 0 else False
        same_direction = self.from_cell.previous_direction_idx in valid_step_cells_idx
        return self.__controls.persistence if not first_step and same_direction else 1

    def __to_cell_probs(self) -> list:
        valid_step_cells_idx = self.__valid_step_cells_idx()
        p = self.__persistence_factor(
            valid_step_cells_idx=valid_step_cells_idx)
        prob_valid_steps = [(self.from_cell.neighbour_tan_slopes[i] * p) / self.from_cell.neighbour_tan_slopes_sum
            for i in valid_step_cells_idx]
        prob_cells = [0.0] * len(self.from_cell.neighbour_coords)
        for i in range(len(valid_step_cells_idx)):
            prob_cells[valid_step_cells_idx[i]] = prob_valid_steps[i]
        return prob_cells

    def __to_cell_idx(self, to_cell_probs: list) -> int:
        return random.choices(list(range(len(to_cell_probs))),
            weights=to_cell_probs, k=1)[0]

    def __to_Cell(self, to_cell_idx: int) -> Cell:
        return Cell(controls=self.__controls,
            coords=self.from_cell.neighbour_coords[to_cell_idx],
            previous_direction=to_cell_idx)