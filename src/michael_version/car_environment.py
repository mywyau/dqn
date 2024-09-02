import pygame

from colours import WHITE, BLUE


class CarEnvironment:
    def __init__(self, car, environment):
        self.car = car
        self.environment = environment
        self.screen = pygame.display.set_mode((self.environment.screen_width, self.environment.screen_height))
        pygame.display.set_caption("Car Environment")

    def is_position_obstacle(self, x, y):
        """Check if the position collides with any obstacle."""
        return self.environment.is_position_obstacle(x, y)

    def reset(self):
        """Reset the environment to the initial state."""
        self.car.reset()
        self.render()  # Render the initial state
        return self.car.get_state()

    def step(self, action):
        """Perform an action and return the new state, reward, and done flag."""
        self.car.perform_action(action)
        self.car.update()  # No need to pass the environment here, the car already has access
        reward = self.car.get_reward()
        done = not self.car.is_car_alive()  # Correctly access is_alive attribute
        state = self.car.get_state()
        self.render()  # Render the environment after the step
        return state, reward, done

    def get_state(self):
        """Get the current state from the car."""
        return self.car.get_state()

    def render(self):
        """Render the environment."""
        self.screen.fill(WHITE)  # Clear the screen with black

        # Draw the trail of the car
        trail_color = BLUE  # blue for the trail
        for pos in self.car.visited_positions:
            pygame.draw.circle(self.screen, trail_color, (int(pos[0]), int(pos[1])), 2)

        # Draw the environment obstacles
        self.environment.draw(self.screen)

        # Draw the car on top of the trail
        self.car.draw(self.screen)

        pygame.display.flip()  # Update the display
