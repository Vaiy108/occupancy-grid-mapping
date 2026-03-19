import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from occupancy_grid import OccupancyGrid


def test_grid_creation():
    grid = OccupancyGrid(width=50, height=60, resolution=0.2)
    assert grid.width == 50
    assert grid.height == 60
    assert grid.resolution == 0.2
    assert grid.log_odds.shape == (60, 50)


def test_world_to_grid_center():
    grid = OccupancyGrid(width=100, height=100, resolution=0.1)
    gx, gy = grid.world_to_grid(0.0, 0.0)
    assert gx == 50
    assert gy == 50


def test_update_cell():
    grid = OccupancyGrid()
    gx, gy = 10, 20
    old_value = grid.log_odds[gy, gx]
    grid.update_cell(gx, gy, grid.l_occ)
    assert grid.log_odds[gy, gx] > old_value


def test_probability_map_range():
    grid = OccupancyGrid()
    prob_map = grid.get_probability_map()
    assert prob_map.min() >= 0.0
    assert prob_map.max() <= 1.0