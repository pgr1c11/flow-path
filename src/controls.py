from src.dem import Dem

class Controls:
    def __init__(
        self,
        dem: Dem,
        slope_threshold: float,
        divergent_flow: float,
        persistence: float,
        horizontal_flow: bool,
        fahrboschung_angle: float,
        max_n_steps: int,
        max_length: float,
        paths_per_flow: int
        ) -> None:
        
        self.dem = dem
        self.slope_threshold = slope_threshold
        self.divergent_flow = divergent_flow
        self.persistence = persistence
        self.horizontal_flow = horizontal_flow
        self.fahrboschung_angle = fahrboschung_angle
        self.max_n_steps = max_n_steps
        self.max_length = max_length
        self.paths_per_flow = paths_per_flow
