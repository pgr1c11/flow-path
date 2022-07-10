from src.results import FlowResults
from src.controls import Controls
from src.cell import Cell 
from src.path import Path
from collections import Counter

class Flow:
    def __init__(
        self,
        controls: Controls,
        start_cell: Cell
        ) -> None:
        self.__controls = controls
        self.start_cell = start_cell
        self.results = self.__run()
    
    def __run(self) -> FlowResults:
        cell = self.start_cell
        paths = [Path(controls=self.__controls, start_cell=cell)
            for _ in range(self.__controls.paths_per_flow)]
        affected_cells_list_list = [path.results.affected_cells for path in paths]
        affected_cells_list = [x for xs in affected_cells_list_list for x in xs]
        affected_cells_counter = Counter(elem for elem in affected_cells_list)
        affected_cells = list(affected_cells_counter.keys())
        cell_values = list(affected_cells_counter.values())
        return FlowResults(
            controls=self.__controls,
            affected_cells=affected_cells,
            cell_values=cell_values)