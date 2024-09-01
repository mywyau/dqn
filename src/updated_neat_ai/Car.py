import math
import pygame

class Car:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.environment = environment  # Environment in which the car operates
        self.is_alive = True
        self.visited_positions = set()
        self.radars = []

        # Car dimensions
        self.width = 30
        self.height = 15

        # Color and Rect for the car (a simple rectangle for now)
        self.color = (0, 255, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        # Draw the car on the screen as a rectangle
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, map):
        # Update the car's position
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.rect.topleft = (self.x, self.y)

        # Clear radar data
        self.radars.clear()

        # Check radar distances at various angles
        for d in range(-90, 150, 30):
            self.check_radar(d, map)

        # Check collision with obstacles or out of bounds
        if self.detect_collision(map):
            self.is_alive = False

    def check_radar(self, degree, map):
        radar_length = 0
        x = int(self.rect.centerx)
        y = int(self.rect.centery)

        # Determine the direction of the radar
        angle_rad = math.radians(self.angle + degree)
        while radar_length < 100:  # Set a max radar length to avoid infinite loops
            radar_length += 1
            x = int(self.rect.centerx + math.cos(angle_rad) * radar_length)
            y = int(self.rect.centery + math.sin(angle_rad) * radar_length)

            # Break if radar is out of bounds
            if x < 0 or y < 0 or x >= map.get_width() or y >= map.get_height():
                break

            # Check for obstacles
            color = map.get_at((x, y))
            if color == (255, 255, 255):  # Assuming white is an obstacle
                break

        # Record radar data
        dist = int(math.sqrt(math.pow(x - self.rect.centerx, 2) + math.pow(y - self.rect.centery, 2)))
        self.radars.append([(x, y), dist])

    def perform_action(self, action):
        if action == 0:  # Small left turn
            self.angle += 2
        elif action == 1:  # Large left turn
            self.angle += 5
        elif action == 2:  # Small right turn
            self.angle -= 2
        elif action == 3:  # Large right turn
            self.angle -= 5
        elif action == 4:  # Accelerate
            self.speed = min(self.speed + 0.1, 6)
        elif action == 5:  # Decelerate
            self.speed = max(self.speed - 0.1, 1)
        elif action == 6:  # Reverse
            self.speed = -min(self.speed, 2)

        # Ensure the car stays within bounds
        if self.detect_collision(self.environment):
            self.is_alive = False

    def reset(self):
        self.x = 100
        self.y = 100
        self.angle = 0
        self.speed = 0
        self.is_alive = True
        self.radars.clear()
        self.visited_positions.clear()
        self.rect.topleft = (self.x, self.y)

    def get_state(self):
        # Return a representation of the car's state
        state = [self.speed, self.angle]
        for radar in self.radars:
            state.append(radar[1])  # Distance recorded by radar
        return state

    def get_reward(self):
        # Implement a reward function based on the car's performance
        reward = 0
        # Example: reward for exploring new areas or getting closer to a target
        return reward

    def is_car_alive(self):
        return self.is_alive

    def detect_collision(self, map):
        # Check for collisions with obstacles or out of bounds
        if self.rect.left < 0 or self.rect.right > map.get_width() or self.rect.top < 0 or self.rect.bottom > map.get_height():
            return True

        # Check if the car is colliding with an obstacle
        car_center = self.rect.center
        color_at_center = map.get_at(car_center)

        if color_at_center == (255, 255, 255):  # White as obstacle color
            return True

        return False
