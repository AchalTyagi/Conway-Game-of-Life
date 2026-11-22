"""Watch a glider walk across the grid in your terminal."""

import os
import subprocess
import time

from life.engine import GLIDER, empty_grid, place, step, to_text


def clear_screen():
    # "cls" is a shell built-in on Windows, so it needs shell=True there.
    if os.name == "nt":
        subprocess.run("cls", shell=True, check=False)
    else:
        subprocess.run(["clear"], check=False)


grid = place(empty_grid(12, 24), GLIDER, 1, 1)

for generation in range(60):
    clear_screen()
    print(f"Generation {generation}  (Ctrl+C to quit)\n")
    print(to_text(grid))
    grid = step(grid)
    time.sleep(0.15)
