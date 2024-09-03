import logging
import os
import sys
import pygame
import torch
from car import Car
from car_environment import CarEnvironment
from dqn_agent import DQNAgent
from environment import Environment  # Assuming Environment is defined in a separate file
from maze_environment import MazeEnvironment  # Import the MazeEnvironment class

# Ensure directories exist
os.makedirs("generated_models", exist_ok=True)
os.makedirs("generated_maps", exist_ok=True)

# Set up logging to ensure INFO messages are shown
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_dqn(episodes, environment_type='maze', visualize=False):
    # Initialize Pygame if visualizing
    if visualize:
        pygame.init()

    # Initialize environment and car based on the selected environment type
    if environment_type == 'maze':
        environment = MazeEnvironment(1200, 800, cell_size=120)
    else:
        raise ValueError(f"Unknown environment type: {environment_type}")

    state_size = len(environment.reset())  # Reset maze to get the initial state size
    action_size = 7
    agent = DQNAgent(state_size, action_size)

    logging.info(f"Starting DQN training in {environment_type} environment")

    for e in range(episodes):
        # Reset the environment to regenerate the maze
        environment.reset()
        car = Car(environment.start_x, environment.start_y, environment, visualize=visualize)
        env = CarEnvironment(car, environment)

        state = env.reset()
        total_reward = 0

        for time in range(2000):
            # Handle events to allow quitting during training
            if visualize:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

            action = agent.act(state)
            next_state, reward, done = env.step(action)

            agent.remember(state, action, reward, next_state, done)
            state = next_state

            total_reward += reward

            if done:
                agent.update_target_model()
                break

            agent.replay()

            if visualize:
                env.render()
                pygame.time.wait(10)

        logging.info(f"Episode {e + 1}/{episodes} ended with score: {total_reward}, Epsilon: {agent.epsilon:.2f}")

        if e % 10 == 0 or e == episodes - 1:
            torch.save(agent.model.state_dict(), f"generated_models/dqn_model_{environment_type}_ep{e + 1}.pth")
            logging.info(f"Model saved after episode {e + 1}")

    logging.info("DQN training completed")

    if visualize:
        pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        environment_type = sys.argv[1]
    else:
        environment_type = 'default'

    train_dqn(10000, environment_type=environment_type, visualize=True)
