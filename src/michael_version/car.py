import math

import pygame

from colours import BLACK, GREEN


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
        self.width = 10
        self.height = 10

        # Color and Rect for the car
        self.color = GREEN
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        # Draw the car on the screen as a rectangle
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw radar lines and values
        self.draw_radar(screen)

    def update(self, environment):
        # Update the car's position
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.rect.topleft = (self.x, self.y)

        # Clear radar data
        self.radars.clear()

        # Check radar distances at various angles (360 degrees)
        for d in range(0, 360, 30):  # Adjust step to increase or decrease the number of beams
            self.check_radar(d, environment)

        # Check collision with obstacles or out of bounds
        if self.detect_collision(environment):
            self.is_alive = False

    def check_radar(self, degree, environment):
        radar_length = 0
        x = int(self.rect.centerx)
        y = int(self.rect.centery)

        # Determine the direction of the radar
        angle_rad = math.radians(self.angle + degree)
        while radar_length < 100:  # Max radar length
            radar_length += 1
            x = int(self.rect.centerx + math.cos(angle_rad) * radar_length)
            y = int(self.rect.centery + math.sin(angle_rad) * radar_length)

            # Break if radar is out of bounds
            if x < 0 or y < 0 or x >= environment.screen_width or y >= environment.screen_height:
                break

            # Check for obstacles
            if environment.is_position_obstacle(x, y):
                break

        # Record radar data
        dist = int(math.sqrt(math.pow(x - self.rect.centerx, 2) + math.pow(y - self.rect.centery, 2)))
        self.radars.append([(x, y), dist])

    def draw_radar(self, screen):
        # Draw radar lines on the screen
        for radar in self.radars:
            position, distance = radar
            pygame.draw.line(screen, GREEN, self.rect.center, position, 1)
            pygame.draw.circle(screen, GREEN, position, 3)

            # Display the distance of the radar hit
            font = pygame.font.Font(None, 24)
            text = font.render(str(distance), True, BLACK)
            screen.blit(text, position)

    def perform_action(self, action):
        # Implement turning or movement logic based on radar or other sensors
        if action == 0:  # Small left turn
            self.angle += 1
        elif action == 1:  # Large left turn
            self.angle += 3
        elif action == 2:  # Small right turn
            self.angle -= 1
        elif action == 3:  # Large right turn
            self.angle -= 3
        elif action == 4:  # Accelerate
            self.speed = min(self.speed + 0.5, 10)  # Increase speed faster, with a higher max speed
        elif action == 5:  # Decelerate
            self.speed = max(self.speed - 0.5, 2)  # Decrease speed faster, with a higher minimum speed
        elif action == 6:  # Reverse
            self.speed = -min(self.speed, 2)

        # Ensure the car stays within bounds
        if self.detect_collision(self.environment):
            self.is_alive = False

    def reset(self):
        self.x = self.environment.start_x
        self.y = self.environment.start_y
        self.angle = 0
        self.speed = 0
        self.is_alive = True
        self.radars.clear()
        self.visited_positions.clear()
        self.rect.topleft = (self.x, self.y)

        # Initialize radars to some default values (e.g., max distance)
        for d in range(0, 360, 30):  # Assuming the same angles as in `update`
            self.radars.append([(self.x, self.y), 100])  # Initialize with max distance

    def get_state(self):
        # Return a representation of the car's state
        state = [self.speed, self.angle]

        # If radars list is empty or incomplete, add default values
        fixed_radar_count = 12  # Assuming 12 radar beams (0, 30, 60, ..., 330)

        # Ensure radars list has a fixed number of entries
        while len(self.radars) < fixed_radar_count:
            self.radars.append([(self.x, self.y), 100])  # Initialize with max distance

        for radar in self.radars:
            state.append(radar[1])  # Distance recorded by radar

        # Ensure the state vector is a fixed size by padding with zeros if necessary
        fixed_state_size = 14  # Speed + Angle + 12 radar distances
        while len(state) < fixed_state_size:
            state.append(0)

        return state

    def get_reward(self):
        reward = 0

        # Penalize the car for getting too close to obstacles
        min_distance_to_obstacle = min(radar[1] for radar in self.radars)
        if min_distance_to_obstacle < 35:  # Threshold distance (e.g., 35 units)
            reward -= (35 - min_distance_to_obstacle) * 2  # Higher penalty for closer obstacles

        # Reward for moving forward (assuming the car is moving towards open space)
        if self.speed > 0:
            reward += 0.1

        # Extra reward for exploring new areas
        current_position = (int(self.rect.centerx), int(self.rect.centery))
        if current_position not in self.visited_positions:
            reward += 10  # Reward for exploring a new area
            self.visited_positions.add(current_position)
        else:
            reward -= 1  # Small penalty for revisiting an area

        # Reward for maintaining a safe distance from obstacles
        if min_distance_to_obstacle > 50:
            reward += 5  # Bonus for keeping a safe distance

        # Bonus for moving towards the most open direction (based on radar values)
        left_value = sum(radar[1] for radar in self.radars[:len(self.radars) // 3])
        right_value = sum(radar[1] for radar in self.radars[-len(self.radars) // 3:])
        forward_value = sum(radar[1] for radar in self.radars[len(self.radars) // 3:-len(self.radars) // 3])

        if forward_value >= max(left_value, right_value):
            reward += 2  # Encourage moving forward if it's the most open path
        elif left_value > right_value:
            reward += 1  # Encourage turning left if it's more open
        else:
            reward += 1  # Encourage turning right if it's more open

        # Heavy penalty if the car collides with an obstacle or goes out of bounds
        if not self.is_alive:
            reward -= 100

        return reward

    def is_car_alive(self):
        return self.is_alive

    def detect_collision(self, environment):
        # Check for collisions with obstacles or out of bounds
        if (self.rect.left < 0 or
                self.rect.right > environment.screen_width or
                self.rect.top < 0 or
                self.rect.bottom > environment.screen_height):
            return True

        # Check if the car is colliding with an obstacle
        car_center = self.rect.center
        if environment.is_position_obstacle(car_center[0], car_center[1]):
            return True

        return False
