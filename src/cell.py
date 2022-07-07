from typing import Tuple
import numpy as np
from src.controls import Controls

_RAD_TO_DEG = np.pi / 180

class Cell:
    def __init__(
        self,
        controls: Controls,
        coords: Tuple[int, int],
        previous_direction: int = 0
        ) -> None:

        self.__controls = controls
        self.coords = coords
        self.on_boundary = self.__on_boundary()
        self.value = self.__current_cell_value()
        self.neighbour_coords = self.__neighbour_coords()
        self.neighbour_values = self.__neighbour_values()
        self.is_sink = self.__is_sink()
        self.neighbour_tan_slopes = self.__neighbour_tan_slopes()
        self.neighbour_tan_slopes_sum = sum(filter(None, self.neighbour_tan_slopes))
        self.neighbour_yis = self.__neighbour_yis()
        self.previous_direction_idx = previous_direction

    def __neighbour_coords(self) -> list:
        r_min = self.coords[0]-1
        r_max = self.coords[0]+2
        c_min = self.coords[1]-1
        c_max = self.coords[1]+2
        if self.on_boundary:
            r_c_lims = np.shape(self.__controls.dem.dem)
            r_min = 0 if r_min < 0 else r_min
            r_max = r_c_lims[0] if r_max > r_c_lims[0] else r_max
            c_min = 0 if c_min < 0 else c_min
            c_max = r_c_lims[1] if c_max > r_c_lims[1] else c_max
        coords = [(i, j) for i in list(range(r_min, r_max)) for j in list(range(c_min, c_max))]
        coords.remove(self.coords)
        return coords

    def __neighbour_values(self) -> list:
        return [self.__controls.dem.dem[i[0], i[1]] for i in self.neighbour_coords]

    def __on_boundary(self) -> bool:
        b = False if self.__controls.dem.boundary[self.coords[0], self.coords[1]] == 0 else True
        return b

    def __current_cell_value(self) -> float:
        return self.__controls.dem.dem[self.coords[0], self.coords[1]]

    def __is_sink(self) -> bool:
        if self.__controls.horizontal_flow:
            s = True if all(self.value < i for i in self.neighbour_values) else False
        else:
            s = True if all(self.value <= i for i in self.neighbour_values) else False
        return s

    def __neighbour_tan_slopes(self) -> list:
        neighbour_values_calc = [i * 0.9
            if i == self.value
            and self.__controls.horizontal_flow
            else i
            for i in self.neighbour_values]
        tan_slopes = [((self.value - neighbour_value) / self.__controls.dem.resolution[0])
            if neighbour_value < self.value
            else None
            for neighbour_value in neighbour_values_calc]
        return tan_slopes
        
    def __neighbour_yis(self) -> list:
        neighbour_yis = [i / np.tan(self.__controls.slope_threshold * _RAD_TO_DEG)
            if i is not None
            else 0
            for i in self.neighbour_tan_slopes]
        self.max_yis: float = max(neighbour_yis)
        return neighbour_yis