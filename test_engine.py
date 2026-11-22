import unittest

import numpy as np

from life.engine import (BLINKER, BLOCK, GLIDER, count_neighbors, empty_grid,
                         place, step)


class TestEngine(unittest.TestCase):
    def test_block_is_still_life(self):
        g = place(empty_grid(6, 6), BLOCK, 2, 2)
        self.assertTrue(np.array_equal(step(g), g))

    def test_blinker_has_period_two(self):
        g0 = place(empty_grid(5, 5), BLINKER, 2, 1)
        g1 = step(g0)
        g2 = step(g1)
        self.assertFalse(np.array_equal(g0, g1))
        self.assertTrue(np.array_equal(g0, g2))
        # Horizontal bar becomes a vertical bar.
        self.assertEqual(g1[1:4, 2].tolist(), [1, 1, 1])

    def test_glider_moves_diagonally(self):
        g = place(empty_grid(10, 10), GLIDER, 1, 1)
        for _ in range(4):
            g = step(g)
        expected = place(empty_grid(10, 10), GLIDER, 2, 2)
        self.assertTrue(np.array_equal(g, expected))

    def test_glider_wraps_around_torus(self):
        n = 8
        g = place(empty_grid(n, n), GLIDER, 1, 1)
        start = g.copy()
        for _ in range(4 * n):  # moves 1 cell per 4 generations
            g = step(g, wrap=True)
        self.assertTrue(np.array_equal(g, start))

    def test_corner_neighbors_without_wrap(self):
        g = empty_grid(4, 4)
        g[0, 1] = g[1, 0] = g[1, 1] = 1
        self.assertEqual(count_neighbors(g, wrap=False)[0, 0], 3)

    def test_corner_neighbors_with_wrap(self):
        g = empty_grid(4, 4)
        g[3, 3] = 1  # diagonal neighbor of (0, 0) on a torus
        self.assertEqual(count_neighbors(g, wrap=True)[0, 0], 1)

    def test_step_does_not_modify_input(self):
        g = place(empty_grid(5, 5), BLINKER, 2, 1)
        before = g.copy()
        step(g)
        self.assertTrue(np.array_equal(g, before))

    def test_lonely_cell_dies_and_crowded_cell_dies(self):
        g = empty_grid(5, 5)
        g[2, 2] = 1
        self.assertEqual(step(g).sum(), 0)  # underpopulation
        g = empty_grid(5, 5)
        g[1:4, 1:4] = 1  # center has 8 neighbors
        self.assertEqual(step(g)[2, 2], 0)  # overpopulation


if __name__ == "__main__":
    unittest.main()
