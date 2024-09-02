import unittest
import torch
import numpy as np

from michael_version.dqn_agent import DQN, DQNAgent


class TestDQNAgent(unittest.TestCase):

    def setUp(self):
        # Set up the DQNAgent with a simple state and action size
        self.state_size = 4
        self.action_size = 2
        self.agent = DQNAgent(self.state_size, self.action_size)
        self.sample_state = np.random.rand(self.state_size)
        self.sample_next_state = np.random.rand(self.state_size)

    def test_initialization(self):
        # Ensure the DQNAgent initializes correctly
        self.assertEqual(self.agent.state_size, self.state_size)
        self.assertEqual(self.agent.action_size, self.action_size)
        self.assertEqual(len(self.agent.memory), 0)
        self.assertEqual(self.agent.epsilon, 1.0)

    def test_remember(self):
        # Test the remember function
        self.agent.remember(self.sample_state, 0, 1.0, self.sample_next_state, False)
        self.assertEqual(len(self.agent.memory), 1)
        self.assertEqual(self.agent.memory[0][0].all(), self.sample_state.all())

    def test_act_random(self):
        # Test the action selection (exploration mode)
        action = self.agent.act(self.sample_state)
        self.assertIn(action, range(self.action_size))

    def test_act_greedy(self):
        # Test the action selection (exploitation mode)
        self.agent.epsilon = 0  # Force greedy action
        action = self.agent.act(self.sample_state)
        self.assertIn(action, range(self.action_size))

    def test_replay_insufficient_memory(self):
        # Test that replay doesn't run if there's not enough memory
        self.agent.replay()  # Nothing should happen
        self.assertEqual(len(self.agent.memory), 0)

    def test_replay(self):
        # Populate memory and test replay
        for _ in range(self.agent.batch_size + 1):
            self.agent.remember(self.sample_state, 0, 1.0, self.sample_next_state, False)
        self.agent.replay()  # Should update the model without error

    def test_update_target_model(self):
        # Test that the target model updates
        original_weights = self.agent.target_model.state_dict()
        self.agent.update_target_model()
        updated_weights = self.agent.target_model.state_dict()
        for key in original_weights:
            self.assertTrue(torch.equal(original_weights[key], updated_weights[key]))


if __name__ == "__main__":
    unittest.main()
