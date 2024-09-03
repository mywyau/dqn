import random
import pygame

from colours import RED


class Environment:
    def __init__(self, screen_width, screen_height, obstacle_count=10):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.obstacle_count = obstacle_count
        self.obstacles = []

        # Generate random obstacles
        self.generate_obstacles()

        # Set an open starting position for the car
        self.start_x, self.start_y = self.find_open_start()

    def find_open_start(self):
        """Find an open position in the environment to start."""
        attempt_limit = 1000  # Limit the number of attempts to find an open position
        car_width, car_height = 30, 15  # Assuming these are the dimensions of the car

        for _ in range(attempt_limit):
            # Generate a random position
            x = random.randint(0, self.screen_width - car_width)
            y = random.randint(0, self.screen_height - car_height)
            if self.is_position_free((x, y), (car_width, car_height)):
                return x, y

        # If no free position is found after many attempts, return (0, 0) as a fallback
        print("Failed to find an open start position after multiple attempts.")
        return 0, 0

    def generate_obstacles(self):
        attempt_limit = 1000  # Limit the number of attempts to place an obstacle
        min_gap = 10  # Minimum gap between obstacles
        for _ in range(self.obstacle_count):
            for attempt in range(attempt_limit):
                # Randomize position and size of the obstacle
                width = random.randint(30, 100)
                height = random.randint(30, 100)
                x = random.randint(0, self.screen_width - width)
                y = random.randint(0, self.screen_height - height)
                new_obstacle = pygame.Rect(x, y, width, height)

                # Check if the new obstacle overlaps any existing ones
                if all(not new_obstacle.colliderect(existing.inflate(min_gap, min_gap)) for existing in self.obstacles):
                    self.obstacles.append(new_obstacle)
                    break
            else:
                print("Failed to place an obstacle after multiple attempts.")

        # If too many obstacles failed to be placed, log the issue
        if len(self.obstacles) < self.obstacle_count:
            print(f"Only {len(self.obstacles)} out of {self.obstacle_count} obstacles were placed.")

    def draw(self, screen):
        # Draw the obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, RED, obstacle)

    def is_position_free(self, pos, size):
        """Check if a given position is free from obstacles."""
        new_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        for obstacle in self.obstacles:
            if new_rect.colliderect(obstacle):
                return False
        return True

    def is_position_obstacle(self, x, y):
        """Check if the given (x, y) position is occupied by an obstacle."""
        for obstacle in self.obstacles:
            if obstacle.collidepoint(x, y):
                return True
        return False
