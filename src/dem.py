from osgeo import gdal
import numpy as np
from abc import ABC, abstractmethod
from matplotlib import pyplot as plt
from typing import Tuple

class dem(ABC):
    def __init__(self) -> None:
        self.dem: np.ndarray

    @abstractmethod
    def _load() -> np.ndarray:
        pass

    def plot(self) -> None:
        plt.imshow(self.dem, cmap='pink')
        plt.colorbar()
        plt.show()

class dem_tif(dem):
    def __init__(self, path: str) -> None:
        self.__path = path
        self.dem = self._load()

    def _load(self) -> np.ndarray:
        dataset = gdal.Open(self.__path)
        return np.array(dataset.GetRasterBand(1).ReadAsArray())

class dem_dummy(dem):
    def __init__(self, dimensions: Tuple[int, int] = (100, 100), relief: float = 50, noise: float = 0.1) -> None:
        self.__dimensions = dimensions
        self.__relief = relief
        self.__noise = noise
        self.dem = self._load()
    
    def _load(self) -> np.ndarray:
        start = 0
        stop = self.__relief
        width = self.__dimensions[0]
        height = self.__dimensions[1]
        row = np.linspace(start, stop, width)
        dem = np.tile(row, (height, 1))
        dem_size = np.shape(dem)
        noise_dem = np.random.normal(loc=1, scale=self.__noise, size=dem_size)
        return dem * noise_dem