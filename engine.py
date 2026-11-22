"""Core Game of Life engine: no graphics, just grids and rules.

A grid is a 2D NumPy array of uint8: 1 = alive, 0 = dead.
"""

import numpy as np

# Patterns are written as text: "O" is a live cell, "." is a dead cell.
BLOCK = ["OO",
         "OO"]

BLINKER = ["OOO"]

GLIDER = [".O.",
          "..O",
          "OOO"]


def empty_grid(rows, cols):
    """Return a grid of the given size with every cell dead."""
    return np.zeros((rows, cols), dtype=np.uint8)


def place(grid, pattern, top=0, left=0):
    """Stamp a text pattern onto the grid (in place) with its corner at (top, left)."""
    for r, line in enumerate(pattern):
        for c, ch in enumerate(line):
            if ch == "O":
                grid[top + r, left + c] = 1
    return grid


def count_neighbors(grid, wrap=True):
    """Return an array with the number of live neighbors of every cell.

    wrap=True  -> the grid is a torus (edges connect to the opposite side).
    wrap=False -> cells outside the grid are treated as dead.

    Note: with wrap=True the grid should be at least 3x3, otherwise the
    same neighbor gets counted more than once.
    """
    offsets = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0)]

    if wrap:
        return sum(np.roll(grid, shift=(dr, dc), axis=(0, 1)) for dr, dc in offsets)

    rows, cols = grid.shape
    padded = np.pad(grid, 1)  # one ring of dead cells around the grid
    return sum(padded[1 + dr:1 + dr + rows, 1 + dc:1 + dc + cols] for dr, dc in offsets)


def step(grid, wrap=True):
    """Return the next generation as a NEW grid (the input is not modified)."""
    n = count_neighbors(grid, wrap=wrap)
    alive = grid == 1
    survives = alive & ((n == 2) | (n == 3))
    born = ~alive & (n == 3)
    return (survives | born).astype(np.uint8)


def to_text(grid, alive="#", dead="."):
    """Render the grid as a multi-line string for terminal output."""
    return "\n".join("".join(alive if cell else dead for cell in row) for row in grid)
