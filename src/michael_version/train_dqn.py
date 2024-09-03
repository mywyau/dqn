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


def train_dqn(episodes, environment_type='default', visualize=False):
    # Initialize Pygame if visualizing
    if visualize:
        pygame.init()

    # Initialize environment and car based on the selected environment type
    if environment_type == 'default':
        environment = Environment(1200, 800, obstacle_count=10)
    elif environment_type == 'maze':
        environment = MazeEnvironment(1200, 800, cell_size=120)
    else:
        raise ValueError(f"Unknown environment type: {environment_type}")

    car = Car(environment.start_x, environment.start_y, environment)
    env = CarEnvironment(car, environment)

    state = env.get_state()
    print(f"State: {state}, Shape: {len(state)}")

    state_size = len(env.get_state())
    print(f"State size: {state_size}")  # This should match the input size of the first layer in DQN
    action_size = 7
    agent = DQNAgent(state_size, action_size)

    logging.info(f"Starting DQN training in {environment_type} environment")

    for e in range(episodes):
        state = env.reset()
        car.reset()  # Reset the car, which includes clearing the map
        logging.info(f"Episode {e + 1}/{episodes} started with initial state of size: {len(state)}")

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

            if time % 100 == 0:
                logging.info(f"Timestep {time}: State size: {len(state)}, Next state size: {len(next_state)}")

            agent.remember(state, action, reward, next_state, done)
            state = next_state

            total_reward += reward

            if done:
                agent.update_target_model()
                logging.info(
                    f"Episode {e + 1}/{episodes} ended with score: {total_reward}, Epsilon: {agent.epsilon:.2f}")
                break

            agent.replay()

            if time % 100 == 0:
                logging.info(f"Episode {e + 1}/{episodes} at timestep {time} - Current Epsilon: {agent.epsilon:.2f}")

            # Render the environment if visualizing
            if visualize:
                env.render()
                pygame.time.wait(10)  # Adjust the delay to control the visualization speed

        # Output the map at the end of each episode
        # logging.info(f"Map after episode {e + 1}:")

        # car.visualize_map()  # Display the map in the console

        # Optionally, save the map to a file
        # with open(f"generated_maps/map_ep{e + 1}.txt", "w") as map_file:
        #     map_output = car.visualize_map_to_string()
        #     map_file.write(map_output)

        if e % 10 == 0 or e == episodes - 1:
            torch.save(agent.model.state_dict(), f"generated_models/dqn_model_{environment_type}_ep{e + 1}.pth")
            logging.info(f"Model saved after episode {e + 1}")

    logging.info("DQN training completed")

    # Optionally, save the map to a file when training finishes
    with open(f"generated_maps/map_ep{e + 1}.txt", "w") as map_file:
        map_output = car.visualize_map_to_string()
        map_file.write(map_output)

    # Quit Pygame if visualizing
    if visualize:
        pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        environment_type = sys.argv[1]
    else:
        environment_type = 'default'

    train_dqn(10000,
              environment_type=environment_type,
              visualize=True)  # Train for 10000 episodes with visualization enabled
