import math

import pygame

from colours import GREEN


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

        # Color and Rect for the car (a simple green rectangle for now)
        self.color = GREEN
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        # Draw the car on the screen as a rectangle
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        # Update the car's position
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.rect.topleft = (self.x, self.y)

        # Clear radar data
        self.radars.clear()

        # Check radar distances at various angles
        for d in range(-90, 150, 30):
            self.check_radar(d)

        # Check collision with obstacles or out of bounds
        if self.detect_collision():
            self.is_alive = False

    def check_radar(self, degree):
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
            if x < 0 or y < 0 or x >= self.environment.screen_width or y >= self.environment.screen_height:
                break

            # Check for obstacles using the new method
            if self.environment.is_position_obstacle(x, y):
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
            self.speed = min(self.speed + 0.5, 10)  # Increased acceleration and maximum speed
        elif action == 5:  # Decelerate
            self.speed = max(self.speed - 0.5, 1)  # Increased deceleration
        elif action == 6:  # Reverse
            self.speed = -min(self.speed, 4)  # Increased reverse speed

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

        # Ensure the state vector is a fixed size by padding with zeros if necessary
        fixed_state_size = 10  # Example fixed size, adjust as needed
        while len(state) < fixed_state_size:
            state.append(0)

        return state

    def get_reward(self):
        reward = 0

        # Check if the car is still alive
        if not self.is_alive:
            return -100  # Heavy penalty for dying

        # Reward for exploring new areas
        current_position = (int(self.rect.centerx), int(self.rect.centery))
        if current_position not in self.visited_positions:
            reward += 10  # Reward for exploring a new area
            self.visited_positions.add(current_position)
        else:
            reward -= 1  # Small penalty for revisiting an area

        # Penalty for hitting an obstacle (already handled in is_alive check)
        if not self.is_alive:
            return -100  # Heavy penalty for collision

        # Bonus for moving
        if self.speed > 0:
            reward += 0.1  # Small reward for continuous movement

        # Penalty for stagnation (e.g., staying in the same place)
        if len(self.visited_positions) > 10:
            if list(self.visited_positions)[-10:] == [current_position] * 10:
                reward -= 5  # Penalty for being stuck in the same place

        return reward

    def is_car_alive(self):
        return self.is_alive

    def detect_collision(self):
        # Check for collisions with obstacles or out of bounds using the environment
        if self.rect.left < 0 or self.rect.right > self.environment.screen_width or self.rect.top < 0 or self.rect.bottom > self.environment.screen_height:
            return True

        # Check if the car is colliding with an obstacle
        return self.environment.is_position_obstacle(self.rect.centerx, self.rect.centery)
