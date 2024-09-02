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
        self.path = []  # Track the car's previous path

        # Car dimensions
        self.width = 30
        self.height = 15

        # Color and Rect for the car (a simple rectangle for now)
        self.color = (0, 255, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        # Draw the car's path (previous positions)
        if len(self.path) > 1:
            pygame.draw.lines(screen, (173, 216, 230), False, self.path, 2)  # Light blue path

        # Draw the car on the screen as a rectangle
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw the radar lines
        self.draw_radar(screen)

    def update(self):
        # Update the car's position
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.rect.topleft = (self.x, self.y)

        # Mark the current position in the path
        self.path.append((self.rect.centerx, self.rect.centery))

        # Clear radar data
        self.radars.clear()

        # Check radar distances at various angles
        for d in range(-90, 150, 30):  # Cover angles from -90 to 150 degrees
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
        while radar_length < 100:  # Radar length up to 100 units
            radar_length += 1
            x = int(self.rect.centerx + math.cos(angle_rad) * radar_length)
            y = int(self.rect.centery + math.sin(angle_rad) * radar_length)

            # Break if radar is out of bounds
            if x < 0 or y < 0 or x >= self.environment.screen_width or y >= self.environment.screen_height:
                break

            # Check for obstacles
            if self.environment.is_position_obstacle(x, y):
                break

        # Record radar data
        dist = int(math.sqrt(math.pow(x - self.rect.centerx, 2) + math.pow(y - self.rect.centery, 2)))
        self.radars.append([(x, y), dist])

    def draw_radar(self, screen):
        # Draw radar lines on the screen
        for radar in self.radars:
            position, distance = radar
            pygame.draw.line(screen, (0, 255, 0), self.rect.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 3)

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
        if self.detect_collision():
            self.is_alive = False

    def reset(self):
        self.x = 100
        self.y = 100
        self.angle = 0
        self.speed = 0
        self.is_alive = True
        self.radars.clear()
        self.visited_positions.clear()
        self.path.clear()
        self.rect.topleft = (self.x, self.y)

    def get_state(self):
        # Return a representation of the car's state
        state = [self.speed, self.angle]
        for radar in self.radars:
            state.append(radar[1])  # Distance recorded by radar
        return state

    def get_reward(self):
        reward = 0
        current_position = (int(self.rect.centerx), int(self.rect.centery))

        # Penalty for revisiting the same area
        if current_position in self.visited_positions:
            reward -= 1
        else:
            self.visited_positions.add(current_position)

        # Penalty for getting too close to obstacles
        min_distance_to_obstacle = min(radar[1] for radar in self.radars)
        if min_distance_to_obstacle < 35:
            reward -= (35 - min_distance_to_obstacle) * 2

        # Bonus for moving
        if self.speed > 0:
            reward += 0.1

        return reward

    def detect_collision(self):
        if self.rect.left < 0 or self.rect.right > self.environment.screen_width or self.rect.top < 0 or self.rect.bottom > self.environment.screen_height:
            return True

        # Check if the car is colliding with an obstacle
        return self.environment.is_position_obstacle(self.rect.centerx, self.rect.centery)
