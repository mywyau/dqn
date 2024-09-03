import torch
import pygame
from car_environment import CarEnvironment
from car import Car
from dqn_agent import DQNAgent
from maze_environment import MazeEnvironment  # Ensure this import is correct

def test_dqn():
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 1200, 800

    # Initialize the maze environment and the car
    environment = MazeEnvironment(screen_width, screen_height, cell_size=120)  # Adjust cell_size if needed
    car = Car(environment.start_x, environment.start_y, environment, visualize=True)  # Enable visualization
    env = CarEnvironment(car, environment)

    state_size = len(env.get_state())
    action_size = 7  # Number of actions
    agent = DQNAgent(state_size, action_size)

    # Load the trained model
    agent.model.load_state_dict(torch.load("generated_models/dqn_model_maze_ep701.pth", map_location=torch.device('cpu')))
    agent.epsilon = 0  # Disable exploration during testing
    print("Maze model loaded successfully.")

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

        # Render the environment (if visualize is enabled)
        env.render()

        # Update the state
        state = next_state

        # Exit the loop if the car is done
        if done:
            break

        # Add a delay to slow down the visualization
        pygame.time.wait(2)  # Adjust delay as needed for visualization

    print(f"Test completed at timestep {time} with total reward {total_reward}.")

    # Quit Pygame properly
    pygame.quit()

if __name__ == "__main__":
    test_dqn()
