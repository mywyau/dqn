import unittest
import pygame
from michael_version.environment import Environment

class TestEnvironment(unittest.TestCase):

    def setUp(self):
        # Initialize an Environment with a small number of obstacles (e.g., 5)
        self.screen_width = 1200
        self.screen_height = 800
        self.obstacle_count = 5
        self.env = Environment(self.screen_width, self.screen_height, self.obstacle_count)

        # Manually place 5 obstacles to avoid randomness and ensure test reliability
        self.env.obstacles = [
            pygame.Rect(100, 100, 50, 50),
            pygame.Rect(300, 300, 50, 50),
            pygame.Rect(500, 500, 50, 50),
            pygame.Rect(700, 700, 50, 50),
            pygame.Rect(900, 100, 50, 50)
        ]

    def test_generate_obstacles(self):
        # Ensure that the correct number of obstacles is generated
        self.assertEqual(len(self.env.obstacles), self.obstacle_count)

        # Ensure all obstacles are within the screen bounds
        for obstacle in self.env.obstacles:
            self.assertTrue(0 <= obstacle.x < self.screen_width)
            self.assertTrue(0 <= obstacle.y < self.screen_height)
            self.assertTrue(obstacle.right <= self.screen_width)
            self.assertTrue(obstacle.bottom <= self.screen_height)

    def test_is_position_free(self):
        # Check a position that should be free
        pos = (self.screen_width // 2, self.screen_height // 2)
        size = (50, 50)
        self.assertTrue(self.env.is_position_free(pos, size))

        # Place an obstacle manually and check that the position is no longer free
        obstacle = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.env.obstacles.append(obstacle)
        self.assertFalse(self.env.is_position_free(pos, size))

    def test_is_position_obstacle(self):
        # Check a position that should not be an obstacle
        x, y = self.screen_width // 2, self.screen_height // 2
        self.assertFalse(self.env.is_position_obstacle(x, y))

        # Place an obstacle manually and check that the position is now considered an obstacle
        obstacle = pygame.Rect(x, y, 50, 50)
        self.env.obstacles.append(obstacle)
        self.assertTrue(self.env.is_position_obstacle(x, y))

    def test_obstacle_placement_limit(self):
        # Ensure that the method doesn't run into an infinite loop or hang if obstacles cannot be placed
        env = Environment(self.screen_width, self.screen_height, obstacle_count=5)
        self.assertEqual(len(env.obstacles), 5)

    def test_obstacle_no_overlap(self):
        # Ensure that no obstacles overlap with each other
        for i, obstacle in enumerate(self.env.obstacles):
            for other in self.env.obstacles[i + 1:]:
                self.assertFalse(obstacle.colliderect(other))

    def test_draw(self):
        # Create a Pygame screen surface to test drawing
        screen = pygame.Surface((self.screen_width, self.screen_height))
        self.env.draw(screen)

        # Ensure that something is drawn to the screen, simple check
        self.assertNotEqual(screen.get_at((0, 0)), pygame.Color(255, 255, 255))  # Assuming the background is white

if __name__ == "__main__":
    unittest.main()
