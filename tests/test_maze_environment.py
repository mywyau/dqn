import unittest

import pygame

from michael_version.maze_environment import MazeEnvironment


class TestMazeEnvironment(unittest.TestCase):

    def setUp(self):
        # Initialize a MazeEnvironment with a known configuration
        self.screen_width = 120
        self.screen_height = 80
        self.cell_size = 40
        self.env = MazeEnvironment(self.screen_width, self.screen_height, self.cell_size)

    def test_maze_dimensions(self):
        # Ensure the grid dimensions match the calculated columns and rows
        self.assertEqual(len(self.env.grid), self.env.rows)
        self.assertEqual(len(self.env.grid[0]), self.env.columns)

    def test_generate_maze(self):
        # Ensure the maze was generated with at least one open path from the start
        open_cells = sum(row.count(0) for row in self.env.grid)
        print(f"Open cells: {open_cells}")
        self.assertGreater(open_cells, 1)  # More than one cell should be open

    def test_get_neighbors(self):
        # Test getting neighbors for a corner cell
        neighbors = self.env.get_neighbors((0, 0))
        print(f"Neighbors of (0, 0): {neighbors}")
        self.assertIn((1, 0), neighbors)
        self.assertIn((0, 1), neighbors)
        self.assertNotIn((0, 0), neighbors)  # The cell itself should not be a neighbor

    def test_remove_wall(self):
        # Test that removing a wall updates the grid correctly
        current_cell = (0, 0)
        next_cell = (0, 1)
        self.env.remove_wall(current_cell, next_cell)
        print(f"Grid after removing wall: {self.env.grid}")
        self.assertEqual(self.env.grid[0][0], 0)
        self.assertEqual(self.env.grid[1][0], 0)
        self.assertEqual(self.env.grid[1][0], 0)  # Wall between the cells should be removed

    def test_is_position_obstacle(self):
        # Check that a position inside a wall is recognized as an obstacle
        x, y = 10, 10  # Inside the first cell, which is initially a wall
        self.assertTrue(self.env.is_position_obstacle(x, y))

        # Check that a position inside a path is not recognized as an obstacle
        self.env.grid[0][0] = 0  # Set the first cell as a path
        x, y = 5, 5  # Inside the first cell, which is now a path
        self.assertFalse(self.env.is_position_obstacle(x, y))

    def test_draw(self):
        # Test the drawing method
        screen = pygame.Surface((self.screen_width, self.screen_height))
        self.env.draw(screen)

        # Ensure that walls are drawn
        self.assertEqual(screen.get_at((0, 0)), pygame.Color(255, 255, 255))  # Check that the top-left corner is white

        # Ensure that paths are not drawn
        self.env.grid[0][0] = 0  # Set the first cell as a path
        self.env.draw(screen)
        self.assertEqual(screen.get_at((1, 1)), pygame.Color(0, 0, 0))  # Check that the top-left corner is black


if __name__ == "__main__":
    unittest.main()
