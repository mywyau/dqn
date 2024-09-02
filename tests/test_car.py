import unittest
from unittest.mock import MagicMock
import pygame

from michael_version.car import Car


class TestCar(unittest.TestCase):

    def setUp(self):
        # Mock environment with specified width and height
        self.environment = MagicMock()
        self.environment.screen_width = 1200
        self.environment.screen_height = 800
        self.environment.is_position_obstacle = MagicMock(return_value=False)

        # Initialize the car
        self.car = Car(100, 100, self.environment)

    def test_initial_state(self):
        # Test the car's initial state
        self.assertEqual(self.car.x, 100)
        self.assertEqual(self.car.y, 100)
        self.assertEqual(self.car.angle, 0)
        self.assertEqual(self.car.speed, 0)
        self.assertTrue(self.car.is_car_alive())
        self.assertEqual(len(self.car.radars), 0)

    def test_perform_action(self):
        # Test performing actions
        initial_angle = self.car.angle
        initial_speed = self.car.speed

        self.car.perform_action(0)  # Small left turn
        self.assertEqual(self.car.angle, initial_angle + 2)

        self.car.perform_action(2)  # Small right turn
        self.assertEqual(self.car.angle, initial_angle + 2 - 2)

        self.car.perform_action(4)  # Accelerate
        self.assertEqual(self.car.speed, initial_speed + 0.5)

        self.car.perform_action(5)  # Decelerate
        self.assertEqual(self.car.speed, max(1, initial_speed))  # Minimum speed should be 1

    def test_update_position(self):
        # Set angle and speed to ensure movement
        self.car.angle = 45  # Move diagonally
        self.car.speed = 5  # Set speed

        initial_x = self.car.x
        initial_y = self.car.y

        # Test updating the car's position
        self.car.update()
        self.assertNotEqual(self.car.x, initial_x)
        self.assertNotEqual(self.car.y, initial_y)

    def test_collision_detection_with_boundary(self):
        # Place the car at the boundary to ensure it detects a collision
        self.car.x = -10  # Position the car slightly off the left edge
        self.car.y = 400
        self.car.update()  # This should trigger a collision detection

        self.assertFalse(self.car.is_car_alive())  # Car should be dead after collision

        # Now test for the right boundary
        self.car.reset()
        self.car.x = self.environment.screen_width + 10  # Position the car slightly off the right edge
        self.car.update()
        self.assertFalse(self.car.is_car_alive())  # Car should be dead after collision

        # Now test for the top boundary
        self.car.reset()
        self.car.y = -10  # Position the car slightly off the top edge
        self.car.update()
        self.assertFalse(self.car.is_car_alive())  # Car should be dead after collision

        # Now test for the bottom boundary
        self.car.reset()
        self.car.y = self.environment.screen_height + 10  # Position the car slightly off the bottom edge
        self.car.update()
        self.assertFalse(self.car.is_car_alive())  # Car should be dead after collision

    def test_collision_detection_with_obstacle(self):
        # Mock the environment to return an obstacle at a specific position
        self.environment.is_position_obstacle = MagicMock(
            side_effect=lambda x, y: (x, y) == (self.car.rect.centerx, self.car.rect.centery))
        self.car.update()
        self.assertFalse(self.car.is_car_alive())  # Car should be dead after collision

    def test_reset(self):
        # Test resetting the car
        self.car.x = 200
        self.car.y = 200
        self.car.speed = 5
        self.car.angle = 45
        self.car.is_alive = False
        self.car.reset()
        self.assertEqual(self.car.x, 100)
        self.assertEqual(self.car.y, 100)
        self.assertEqual(self.car.speed, 0)
        self.assertEqual(self.car.angle, 0)
        self.assertTrue(self.car.is_car_alive())
        self.assertEqual(len(self.car.radars), 0)

    def test_get_state(self):
        # Test getting the state of the car
        self.car.perform_action(4)  # Accelerate
        self.car.update()
        state = self.car.get_state()
        self.assertEqual(len(state), 10)  # Ensure the state has a fixed size
        self.assertEqual(state[0], self.car.speed)
        self.assertEqual(state[1], self.car.angle)

    def test_get_reward(self):
        # Test the reward function
        reward = self.car.get_reward()
        self.assertEqual(reward, 10)  # Initial reward for new area

        # Test penalty for collision
        self.car.is_alive = False
        reward = self.car.get_reward()
        self.assertEqual(reward, -100)


if __name__ == '__main__':
    unittest.main()
