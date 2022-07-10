import numpy as np
from osgeo import gdal, osr
from abc import ABC
from typing import Tuple
import os
from matplotlib import pyplot as plt
from src.controls import Controls

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

class Results(ABC):
    def __init__(self) -> None:
        self.controls: Controls
        self.affected_cells: list
        self.cell_values: list
        self.array_shape: list
    
    def _get_array_shape(self) -> list:
        r_vals = [i[0] for i in self.affected_cells]
        c_vals = [i[1] for i in self.affected_cells]
        r_min, r_max = min(r_vals), max(r_vals)
        c_min, c_max = min(c_vals), max(c_vals)
        cols = (c_max - c_min) + 1
        rows = (r_max - r_min) + 1
        return [r_min, r_max, c_min, c_max, rows, cols]

    def __get_origin(self, r_min: float, c_min: float) -> Tuple[float, float]:
        dem_origin = self.controls.dem.origin
        dem_origin_x, dem_origin_y = dem_origin[0], dem_origin[1]
        origin_x = dem_origin_x + self.controls.dem.resolution[0] * c_min
        origin_y = dem_origin_y + self.controls.dem.resolution[1] * r_min
        return (origin_x, origin_y)

    def __get_epsg_code(self) -> int:
        if self.controls.dem.crs == "None":
            return 27700
        else:
            proj = osr.SpatialReference(self.controls.dem.crs)
            return int(proj.GetAttrValue('AUTHORITY',1))

    def create_array(self) -> np.ndarray:
        r_min, c_min, rows, cols = self.array_shape[0], self.array_shape[2], self.array_shape[4], self.array_shape[5]
        arr = np.zeros(shape=(rows, cols))
        affected_cells_floor = [(i[0] - r_min, i[1] - c_min) for i in self.affected_cells]
        affected_cells_array = np.array(affected_cells_floor)
        arr[(affected_cells_array[:,0], affected_cells_array[:,1])] = self.cell_values
        return arr

    def create_raster(self) -> None:
        r_min, c_min, rows, cols = self.array_shape[0], self.array_shape[2], self.array_shape[4], self.array_shape[5]
        arr = self.create_array()
        origin = self.__get_origin(r_min=r_min, c_min=c_min)
        origin_x, origin_y = origin[0], origin[1]
        pixel_size = self.controls.dem.resolution
        pixel_size_x, pixel_size_y = pixel_size[0], pixel_size[1]
        temp_filename = os.path.join(ROOT_DIR, 'data', 'temp.tif')
        epsg_code = self.__get_epsg_code()
        driver = gdal.GetDriverByName('GTiff')
        outRaster = driver.Create(temp_filename, cols, rows, 1, gdal.GDT_Byte)
        outRaster.SetGeoTransform((origin_x, pixel_size_x, 0, origin_y, 0, pixel_size_y))
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(arr)
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromEPSG(epsg_code)
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        outband.FlushCache()

    def plot(self) -> None:
        plt.imshow(self.create_array(), cmap='pink')
        plt.colorbar()
        plt.show()

class PathResults(Results):
    def __init__(self, controls: Controls, affected_cells: list) -> None:
        self.controls = controls
        self.affected_cells = affected_cells
        self.cell_values = [1 for _ in self.affected_cells]
        self.array_shape = self._get_array_shape()

class FlowResults(Results):
    def __init__(self, controls: Controls, affected_cells: list, cell_values: list) -> None:
        self.controls = controls
        self.affected_cells = affected_cells
        self.cell_values = cell_values
        self.array_shape = self._get_array_shape()

class MapResults:
    pass