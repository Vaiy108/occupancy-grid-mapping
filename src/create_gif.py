import os
import imageio.v2 as imageio

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
OUTPUT_PATH = os.path.join(RESULTS_DIR, "map_animation.gif")

images = []

for file_name in sorted(os.listdir(RESULTS_DIR)):
    if file_name.startswith("map_frame_") and file_name.endswith(".png"):
        file_path = os.path.join(RESULTS_DIR, file_name)
        try:
            images.append(imageio.imread(file_path))
        except Exception as e:
            print(f"Skipping unreadable file: {file_name} ({e})")

if not images:
    raise ValueError("No readable map_frame_*.png files found in the results folder.")

imageio.mimsave(OUTPUT_PATH, images, duration=0.3)
print("GIF created:", OUTPUT_PATH)