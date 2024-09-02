# TODO: Fix or delete, hard to mock and test
# import unittest
# from unittest.mock import patch, MagicMock
# import torch
# import pygame
#
# from michael_version.car import Car
# from michael_version.car_environment import CarEnvironment
# from michael_version.dqn_agent import DQNAgent
# from michael_version.environment import Environment
# from michael_version.test_dqn import test_dqn
#
#
# # from car_environment import CarEnvironment
# # from car import Car
# # from dqn_agent import DQNAgent
# # from environment import Environment
#
#
# class TestDQN(unittest.TestCase):
#     @patch('pygame.init')
#     @patch('pygame.display.set_mode')
#     @patch('pygame.display.set_caption')
#     @patch('pygame.time.wait')
#     @patch('pygame.event.get')
#     @patch('torch.load')
#     @patch('dqn_agent.DQNAgent.act')
#     def test_dqn(self, mock_act, mock_torch_load, mock_event_get, mock_time_wait,
#                  mock_set_caption, mock_set_mode, mock_pygame_init):
#         # Mock Pygame event to simulate quitting after one loop iteration
#         mock_event_get.side_effect = [[pygame.event.Event(pygame.QUIT)]]
#
#         # Mock the model loading
#         mock_torch_load.return_value = MagicMock()
#
#         # Mock the agent's act method to return a fixed action
#         mock_act.return_value = 0
#
#         # Create the environment and car
#         environment = Environment(1200, 800, obstacle_count=10)
#         car = Car(100, 100, environment)
#         env = CarEnvironment(car, environment)
#
#         state_size = len(env.get_state())
#         action_size = 7
#         agent = DQNAgent(state_size, action_size)
#
#         # Mock the state dict loading
#         agent.model.load_state_dict = MagicMock()
#
#         # Call the function to test
#         with patch('builtins.print') as mocked_print:
#             # from your_module_name import test_dqn  # Import the function from your module
#             test_dqn()
#
#             # Ensure model was loaded
#             agent.model.load_state_dict.assert_called_once()
#
#             # Check that we printed the success message
#             mocked_print.assert_any_call("Model loaded successfully.")
#
#             # Ensure the environment was reset
#             self.assertEqual(env.get_state(), car.get_state())
#
#             # Ensure we completed the loop and quit properly
#             mocked_print.assert_any_call(f"Test completed at timestep 0 with total reward 0.")
#             mocked_print.assert_any_call(f"Final reward after 2000 timesteps: 0")
#
#         # Check Pygame quit was called
#         self.assertTrue(pygame.quit.called)
#
#
# if __name__ == "__main__":
#     unittest.main()
