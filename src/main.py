import os
import math
import yaml
import matplotlib.pyplot as plt

from occupancy_grid import OccupancyGrid
from lidar_simulator import LidarSimulator
from utils import bresenham_raytrace


def load_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    config_path = os.path.join(project_root, "config", "default.yaml")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    map_cfg = config["map"]
    lidar_cfg = config["lidar"]
    sim_cfg = config["simulation"]
    robot_cfg = config["robot"]

    grid = OccupancyGrid(
        width=map_cfg["width"],
        height=map_cfg["height"],
        resolution=map_cfg["resolution"],
        occ_prob=map_cfg["occ_prob"],
        free_prob=map_cfg["free_prob"],
        l_min=map_cfg["l_min"],
        l_max=map_cfg["l_max"],
    )

    lidar = LidarSimulator(
        num_rays=lidar_cfg["num_rays"],
        max_range=lidar_cfg["max_range"],
        noise_std=lidar_cfg["noise_std"],
    )

    obstacles = sim_cfg["obstacles"]
    num_iterations = sim_cfg["num_iterations"]

    robot_x = robot_cfg["x"]
    robot_y = robot_cfg["y"]

    gx0, gy0 = grid.world_to_grid(robot_x, robot_y)

    os.makedirs("results", exist_ok=True)

    for i in range(num_iterations):
        ranges = lidar.simulate_scan(obstacles)

        for angle, r in zip(lidar.angles, ranges):
            x_end = robot_x + r * math.cos(angle)
            y_end = robot_y + r * math.sin(angle)

            gx1, gy1 = grid.world_to_grid(x_end, y_end)
            cells = bresenham_raytrace(gx0, gy0, gx1, gy1)

            if not cells:
                continue

            for gx, gy in cells[:-1]:
                grid.update_cell(gx, gy, grid.l_free)

            end_x, end_y = cells[-1]
            grid.update_cell(end_x, end_y, grid.l_occ)

        if i % 10 == 0:
            plt.imshow(grid.get_probability_map(), cmap="gray", origin="lower")
            plt.title(f"Iteration {i}")
            plt.savefig(f"results/map_frame_{i:03d}.png")
            plt.clf()

    prob_map = grid.get_probability_map()

    plt.figure(figsize=(8, 8))
    plt.imshow(prob_map, cmap="gray", origin="lower", vmin=0, vmax=1)
    plt.title("Occupancy Grid Map")
    plt.colorbar(label="Occupancy Probability")

    gx0, gy0 = grid.world_to_grid(robot_x, robot_y)
    plt.scatter(gx0, gy0, c="red", s=50, label="Robot")
    plt.legend()

    plt.savefig("results/final_map.png")
    plt.show()


if __name__ == "__main__":
    main()