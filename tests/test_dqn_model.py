import unittest

import torch

from michael_version.dqn_agent import DQN


class TestDQN(unittest.TestCase):

    def setUp(self):
        # Set up a common state and action size for the tests
        self.state_size = 4
        self.action_size = 2
        self.dqn = DQN(self.state_size, self.action_size)

    def test_model_initialization(self):
        # Check if the model initializes with correct layer sizes
        self.assertEqual(self.dqn.fc1.in_features, self.state_size)
        self.assertEqual(self.dqn.fc3.out_features, self.action_size)

    def test_forward_pass(self):
        # Test a forward pass with a random input tensor
        input_tensor = torch.rand(1, self.state_size)
        output = self.dqn(input_tensor)
        self.assertEqual(output.shape, (1, self.action_size))


if __name__ == "__main__":
    unittest.main()
