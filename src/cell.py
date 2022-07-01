from typing import Tuple
import numpy as np
from src.controls import Controls

class Cell:
    def __init__(
        self,
        controls: Controls,
        coords: Tuple[int, int]
        ) -> None:

        self.__controls = controls
        self.coords = coords
        self.on_boundary = self.__on_boundary()
        self.value = self.__current_cell_value()
        self.neighbour_values = self.__neighbour_values()
        self.is_sink = self.__is_sink()

    def __neighbour_values(self) -> list:
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
        
        dem_values = self.__controls.dem.dem[r_min:r_max, c_min:c_max]
        dem_list_list = dem_values.tolist()
        dem_list = [x for xs in dem_list_list for x in xs]
        dem_list.remove(self.value)
        return dem_list

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


