# train_dqn.py
import logging
import torch
import pygame
from car import Car
from car_environment import CarEnvironment
from dqn_agent import DQNAgent
from environment import Environment  # Assuming Environment is defined in a separate file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_dqn(episodes, visualize=False):
    # Initialize Pygame if visualizing
    if visualize:
        pygame.init()

    # Initialize environment and car
    environment = Environment(1200, 800, obstacle_count=10)
    car = Car(100, 100, environment)
    env = CarEnvironment(car, environment)

    state_size = len(env.get_state())
    print(f"State size: {state_size}")  # This should match the input size of the first layer in DQN
    action_size = 7
    agent = DQNAgent(state_size, action_size)

    logging.info("Starting DQN training")

    for e in range(episodes):
        state = env.reset()
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
                logging.info(f"Episode {e + 1}/{episodes} ended with score: {total_reward}, Epsilon: {agent.epsilon:.2f}")
                break

            agent.replay()

            if time % 100 == 0:
                logging.info(f"Episode {e + 1}/{episodes} at timestep {time} - Current Epsilon: {agent.epsilon:.2f}")

            # Render the environment if visualizing
            if visualize:
                env.render()
                pygame.time.wait(10)  # Adjust the delay to control the visualization speed

        if e % 10 == 0 or e == episodes - 1:
            torch.save(agent.model.state_dict(), "generated_models/dqn_model.pth")
            logging.info(f"Model saved after episode {e + 1}")

    logging.info("DQN training completed")

    # Quit Pygame if visualizing
    if visualize:
        pygame.quit()

if __name__ == "__main__":
    train_dqn(20, visualize=True)  # Train for 20 episodes with visualization enabled
