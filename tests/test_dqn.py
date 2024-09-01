import unittest

import torch

from michael_version.dqn_agent import DQN


class TestDQNModel(unittest.TestCase):

    def test_forward_pass(self):
        state_size = 10  # This should match the input size expected by the model
        action_size = 7  # Number of actions
        model = DQN(state_size, action_size)

        # Create a dummy input
        dummy_input = torch.rand(1, state_size)

        # Pass through the model
        output = model(dummy_input)

        # Check if output has the correct shape
        self.assertEqual(output.shape, (1, action_size))


if __name__ == '__main__':
    unittest.main()
