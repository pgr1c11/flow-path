from osgeo import gdal, osr
import numpy as np
from abc import ABC, abstractmethod
from matplotlib import pyplot as plt
from typing import Tuple

class Dem(ABC):
    def __init__(self) -> None:
        self.dem: np.ndarray
        self.boundary: np.ndarray
        self.resolution: Tuple[float, float]
        self.origin: Tuple[float, float]
        self.crs: str

    @abstractmethod
    def _load() -> np.ndarray:
        pass

    def plot(self) -> None:
        plt.imshow(self.dem, cmap='pink')
        plt.colorbar()
        plt.show()

    def _boundary(self) -> np.ndarray:
        dem_size = np.shape(self.dem)
        dem_boundary = np.zeros(dem_size, dtype=int)
        change_index = (0, -1)
        dem_boundary[change_index,:] = 1
        dem_boundary[:,change_index] = 1
        return dem_boundary

class DemTif(Dem):
    def __init__(self, path: str) -> None:
        self.__path = path
        self.dem = self._load()
        self.boundary = self._boundary()

    def __get_resolution(self, dataset) -> Tuple[float, float]:
        _, xres, _, _, _, yres  = dataset.GetGeoTransform()
        return (abs(xres), abs(yres))

    def __get_origin(self, dataset) -> Tuple[float, float]:
        x_or, _, _, y_or, _, _ = dataset.GetGeoTransform()
        return (x_or, y_or)

    def __get_crs(self, dataset) -> str:
        wkt_crs = dataset.GetProjection()
        srs=osr.SpatialReference(wkt=wkt_crs)
        if not srs.IsProjected:
            raise Exception("DEM CRS must be projected.")
        return wkt_crs

    def _load(self) -> np.ndarray:
        dataset = gdal.Open(self.__path)
        self.resolution = self.__get_resolution(dataset)
        self.origin = self.__get_origin(dataset)
        self.crs = self.__get_crs(dataset)
        return np.array(dataset.GetRasterBand(1).ReadAsArray())

class DemDummy(Dem):
    def __init__(
        self,
        dimensions: Tuple[int, int] = (100, 100),
        relief: float = 50,
        noise: float = 0.1) -> None:

        self.__dimensions = dimensions
        self.__relief = relief
        self.__noise = noise
        self.dem = self._load()
        self.boundary = self._boundary()
        self.resolution = (1, 1)
        self.origin = (0, 0)
        self.crs = "None"
    
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