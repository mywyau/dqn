import unittest
import pygame
from michael_version.environment import Environment
from michael_version.car import Car
from michael_version.car_environment import CarEnvironment

class TestEnvironmentVisualization(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 800
        self.obstacle_count = 5
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.env = Environment(self.screen_width, self.screen_height, self.obstacle_count)
        self.car = Car(100, 100, self.env)
        self.car_env = CarEnvironment(self.car, self.env)

    def test_visualization(self):
        running = True
        clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()  # Get the start time

        display_duration = 10000  # Display for 10000 milliseconds (10 seconds)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Check if the desired time has passed
            elapsed_time = pygame.time.get_ticks() - start_ticks
            if elapsed_time > display_duration:
                running = False

            # Clear the screen
            self.screen.fill((0, 0, 0))

            # Draw the environment and the car
            self.env.draw(self.screen)
            self.car_env.render()

            # Update the display
            pygame.display.flip()

            # Slow down the loop to make it visible
            clock.tick(60)  # 60 frames per second

        pygame.quit()

if __name__ == "__main__":
    unittest.main()
