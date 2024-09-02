import pygame

from colours import WHITE


class CarEnvironment:
    def __init__(self, car, environment):
        self.car = car
        self.environment = environment
        self.screen = pygame.display.set_mode((self.environment.screen_width, self.environment.screen_height))
        pygame.display.set_caption("Car Environment")
        self.clock = pygame.time.Clock()  # Create a clock object to control frame rate

    def reset(self):
        """Reset the environment to the initial state."""
        self.car.reset()
        self.render()  # Render the initial state
        return self.car.get_state()

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

    def render(self):
        """Render the environment."""
        self.screen.fill(WHITE)  # Clear the screen with white
        self.environment.draw(self.screen)  # Draw the current environment
        self.car.draw(self.screen)  # Draw the car
        pygame.display.flip()  # Update the display
        self.clock.tick(60)  # Cap the frame rate to 60 FPS
