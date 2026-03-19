import numpy as np


class OccupancyGrid:
    def __init__(
        self,
        width: int = 100,
        height: int = 100,
        resolution: float = 0.1,
        occ_prob: float = 0.9,
        free_prob: float = 0.3,
        l_min: float = -5.0,
        l_max: float = 5.0,
    ):
        self.width = width
        self.height = height
        self.resolution = resolution

        self.occ_prob = occ_prob
        self.free_prob = free_prob
        self.l_min = l_min
        self.l_max = l_max

        # log-odds grid initialized as unknown (0 => p = 0.5)
        self.log_odds = np.zeros((self.height, self.width), dtype=np.float32)

        # precompute log-odds increments
        self.l_occ = np.log(self.occ_prob / (1.0 - self.occ_prob))
        self.l_free = np.log(self.free_prob / (1.0 - self.free_prob))

    def world_to_grid(self, x: float, y: float):
        """
        Convert world coordinates in meters to grid indices.
        World origin (0,0) is placed at the center of the grid.
        """
        gx = int(round(x / self.resolution + self.width / 2))
        gy = int(round(y / self.resolution + self.height / 2))
        return gx, gy

    def grid_to_world(self, gx: int, gy: int):
        """
        Convert grid indices back to world coordinates.
        """
        x = (gx - self.width / 2) * self.resolution
        y = (gy - self.height / 2) * self.resolution
        return x, y

    def is_inside(self, gx: int, gy: int) -> bool:
        return 0 <= gx < self.width and 0 <= gy < self.height

    def update_cell(self, gx: int, gy: int, delta_log_odds: float):
        """
        Add a log-odds increment to a cell and clamp it.
        """
        if self.is_inside(gx, gy):
            self.log_odds[gy, gx] += delta_log_odds
            self.log_odds[gy, gx] = np.clip(
                self.log_odds[gy, gx], self.l_min, self.l_max
            )

    def get_probability_map(self):
        """
        Convert log-odds map into occupancy probabilities.
        """
        return 1.0 - 1.0 / (1.0 + np.exp(self.log_odds))

    def reset(self):
        """
        Reset the map to unknown state.
        """
        self.log_odds.fill(0.0)