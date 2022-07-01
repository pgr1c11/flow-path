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
        max_n_walks: int,
        max_length: float
        ) -> None:
        
        self.dem = dem
        self.slope_threshold = slope_threshold
        self.divergent_flow = divergent_flow
        self.persistence = persistence
        self.horizontal_flow = horizontal_flow
        self.fahrboschung_angle = fahrboschung_angle
        self.max_n_walks = max_n_walks
        self.max_length = max_length
