"""Watch a glider walk across the grid in your terminal."""

import os
import time

from life.engine import GLIDER, empty_grid, place, step, to_text

grid = place(empty_grid(12, 24), GLIDER, 1, 1)

for generation in range(60):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Generation {generation}  (Ctrl+C to quit)\n")
    print(to_text(grid))
    grid = step(grid)
    time.sleep(0.15)
