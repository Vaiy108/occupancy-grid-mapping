import numpy as np


class LidarSimulator:
    def __init__(
        self,
        num_rays: int = 181,
        max_range: float = 10.0,
        noise_std: float = 0.05,
    ):
        self.num_rays = num_rays
        self.max_range = max_range
        self.noise_std = noise_std

        # Field of view: -90° to +90°
        self.angles = np.linspace(-np.pi / 2, np.pi / 2, num_rays)

    def simulate_scan(self, obstacles):
        """
        Simulate a 2D Lidar scan.

        obstacles: list of dicts with {'x', 'y'}
        returns: numpy array of ranges (size = num_rays)
        """

        ranges = np.ones(self.num_rays) * self.max_range

        for i, theta in enumerate(self.angles):
            for obs in obstacles:
                dx = obs['x']
                dy = obs['y']

                r = np.sqrt(dx**2 + dy**2)
                angle = np.arctan2(dy, dx)

                # Check if obstacle lies along this ray
                if abs(angle - theta) < (np.pi / self.num_rays):
                    if r < ranges[i]:
                        ranges[i] = r

        # Add Gaussian noise
        noise = np.random.normal(0, self.noise_std, size=self.num_rays)
        ranges = ranges + noise

        # Clamp values
        ranges = np.clip(ranges, 0.01, self.max_range)

        return ranges