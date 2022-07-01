from typing import Any, Tuple
import numpy as np
from src.results import PathResults
from src.controls import Controls

class Path:
    def __init__(
        self,
        controls: Controls,
        start_coords: Tuple[int, int]
        ) -> None:

        self.__controls = controls
        self.affected = [start_coords]

