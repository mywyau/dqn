import math
import pygame
from colours import BLACK
from geometry_helper import GeometryHelper  # Import the GeometryHelper class

class Car:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.environment = environment
        self.is_alive = True
        self.visited_positions = set()
        self.radars = []
        self.path = []  # Store the path the car has taken

        # Car dimensions
        self.width = 30
        self.height = 15

        # Color and Rect for the car
        self.color = (0, 255, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        # Draw the path the car has taken
        if len(self.path) > 1:
            pygame.draw.lines(screen, (255, 255, 0), False, self.path, 2)

        # Draw the car on the screen
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw the radar lines
        self.draw_radar(screen)

    def update(self):
        # Update the car's position
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.rect.topleft = (self.x, self.y)

        # Add current position to path
        self.path.append((self.rect.centerx, self.rect.centery))

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
        while radar_length < 100:
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
            # Display the distance of the radar hit
            font = pygame.font.Font(None, 24)
            text = font.render(str(distance), True, BLACK)
            screen.blit(text, position)

    def perform_action(self, action):
        # Rule to prevent moving toward an obstacle if radar detects something too close
        radar_index = None
        if action in [0, 1] and len(self.radars) > 0:  # Turning left actions
            radar_index = 0  # Index for the leftmost radar (-90 degrees)
        elif action in [2, 3] and len(self.radars) > 0:  # Turning right actions
            radar_index = -1  # Index for the rightmost radar (150 degrees)

        if radar_index is not None and len(self.radars) > abs(radar_index) and self.radars[radar_index][1] < 20:
            # Skip the action if the obstacle is too close
            return

        if action == 0:  # Small left turn
            self.angle += 2
        elif action == 1:  # Large left turn
            self.angle += 5
        elif action == 2:  # Small right turn
            self.angle -= 2
        elif action == 3:  # Large right turn
            self.angle -= 5
        elif action == 4:  # Accelerate
            self.speed = min(self.speed + 3, 10)
        elif action == 5:  # Decelerate
            self.speed = max(self.speed - 1, 2)
        elif action == 6:  # Reverse
            self.speed = -min(self.speed, 4)

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

        # Ensure the state vector is a fixed size by padding with zeros if necessary
        fixed_state_size = 10
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

        # Penalty for getting closer to obstacles
        min_distance_to_obstacle = GeometryHelper.get_min_distance_to_obstacle(self.rect, self.environment.obstacles)
        if min_distance_to_obstacle is not None:
            # Increase penalty as the car gets closer to an obstacle
            if min_distance_to_obstacle < 30:  # Threshold distance (can be adjusted)
                reward -= 10  # High penalty for being too close
            elif min_distance_to_obstacle < 50:
                reward -= 5  # Medium penalty
            elif min_distance_to_obstacle < 100:
                reward -= 2  # Low penalty

        # Penalty for getting closer to the borders of the environment
        min_distance_to_border = GeometryHelper.get_min_distance_to_border(self.rect, self.environment.screen_width, self.environment.screen_height)
        if min_distance_to_border < 30:
            reward -= 10  # High penalty for being too close to the border
        elif min_distance_to_border < 50:
            reward -= 5  # Medium penalty
        elif min_distance_to_border < 100:
            reward -= 2  # Low penalty

        # Bonus for moving
        if self.speed > 0:
            reward += 0.1  # Small reward for continuous movement

        return reward

    def is_car_alive(self):
        return self.is_alive

    def detect_collision(self):
        # Check for collisions with obstacles or out of bounds
        if self.rect.left < 0 or self.rect.right > self.environment.screen_width or self.rect.top < 0 or self.rect.bottom > self.environment.screen_height:
            return True

        # Check if the car is colliding with an obstacle
        return self.environment.is_position_obstacle(self.rect.centerx, self.rect.centery)
