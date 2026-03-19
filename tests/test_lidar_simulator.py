import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from lidar_simulator import LidarSimulator


def test_lidar_output_shape():
    lidar = LidarSimulator(num_rays=100)
    obstacles = [{'x': 2, 'y': 2}]
    ranges = lidar.simulate_scan(obstacles)

    assert len(ranges) == 100


def test_lidar_range_limits():
    lidar = LidarSimulator(max_range=5.0)
    obstacles = [{'x': 2, 'y': 1}]
    ranges = lidar.simulate_scan(obstacles)

    assert np.all(ranges >= 0.01)
    assert np.all(ranges <= 5.0)