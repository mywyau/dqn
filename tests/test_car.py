import unittest

import pygame

from michael_version.car import Car
from michael_version.environment import Environment


class TestCar(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.environment = Environment(1200, 800, 0)  # No obstacles for now
        self.car = Car(100, 100, self.environment)

    def test_initial_state(self):
        self.assertTrue(self.car.is_car_alive())
        self.assertEqual(self.car.speed, 0)
        self.assertEqual(self.car.angle, 0)

    def test_collision_with_obstacle(self):
        # Simulate an obstacle at the car's position
        self.environment.obstacles.append(pygame.Rect(100, 100, 30, 30))
        self.car.update(self.environment)
        self.assertFalse(self.car.is_car_alive())  # Car should be dead after collision

    def test_no_collision(self):
        self.car.update(self.environment)
        self.assertTrue(self.car.is_car_alive())  # Car should be alive


if __name__ == "__main__":
    unittest.main()
