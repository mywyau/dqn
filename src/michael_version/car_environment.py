import pygame

from colours import WHITE

class CarEnvironment:
    def __init__(self, car, environment, visualize=True):
        self.car = car
        self.environment = environment
        self.visualize = visualize
        if visualize:
            self.screen = pygame.display.set_mode((environment.screen_width, environment.screen_height))

    def reset(self):
        self.environment.reset()  # Reset the environment (i.e., regenerate the maze)
        self.car.reset()  # Reset the car
        if self.visualize:
            self.render()  # Only render if visualize is True
        return self.get_state()

    def render(self):
        if self.visualize:
            self.screen.fill((255, 255, 255))  # Clear screen
            self.environment.draw(self.screen)  # Draw environment
            self.car.draw(self.screen)  # Draw the car
            pygame.display.flip()  # Update the display

    def step(self, action):
        """Perform an action and return the new state, reward, and done flag."""
        self.car.perform_action(action)
        self.car.update(self.environment)  # Pass the environment to the update method
        reward = self.car.get_reward()
        done = not self.car.is_alive
        state = self.car.get_state()
        self.render()  # Render the environment after the step
        return state, reward, done

    def get_state(self):
        """Get the current state from the car."""
        return self.car.get_state()
