import torch
import pygame
from car_environment import CarEnvironment
from car import Car
from dqn_agent import DQNAgent
from environment import Environment  # Assuming Environment is defined in a separate file

def test_dqn():
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 1200, 800

    # Initialize the environment and the car
    environment = Environment(screen_width, screen_height, obstacle_count=10)
    car = Car(100, 100, environment)
    env = CarEnvironment(car, environment)  # Pass the environment to CarEnvironment

    state_size = len(env.get_state())
    action_size = 7  # Number of actions
    agent = DQNAgent(state_size, action_size)

    # Load the trained model
    agent.model.load_state_dict(torch.load("generated_models/dqn_model.pth"))
    print("Model loaded successfully.")

    state = env.reset()
    total_reward = 0

    # Run the game loop for testing
    for time in range(10000):
        # Handle events (including quitting)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Let the agent select an action
        action = agent.act(state)

        # Step through the environment
        next_state, reward, done = env.step(action)

        # Accumulate reward
        total_reward += reward

        # Render the environment
        env.render()

        # Update the state
        state = next_state

        # Exit the loop if the car is done
        if done:
            break

        # Add a delay to slow down the visualization
        pygame.time.wait(2)  # Wait 10 milliseconds between each step

    print(f"Test completed at timestep {time} with total reward {total_reward}.")
    print(f"Final reward after 2000 timesteps: {total_reward}")

    # Quit Pygame properly
    pygame.quit()

if __name__ == "__main__":
    test_dqn()
