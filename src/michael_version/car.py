import math
import pygame
from colours import BLACK, GREEN

class Car:
    def __init__(self, x, y, environment, visualize=False):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.environment = environment
        self.is_alive = True
        self.visited_positions = set()
        self.path = []
        self.radars = []
        self.visualize = visualize
        self.map = {}

        # Car dimensions
        self.width = 10
        self.height = 10
        self.color = GREEN
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        if not self.visualize:
            return

        # Draw the path taken by the car
        for i in range(1, len(self.path)):
            pygame.draw.line(screen, BLACK, self.path[i - 1], self.path[i], 2)

        # Draw the car on the screen as a rectangle
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw radar lines and values
        self.draw_radar(screen)

    def update(self, environment):
        # Update the car's position
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.rect.topleft = (self.x, self.y)

        # Store the position in the path and mark the current position as visited
        self.path.append((self.x, self.y))
        self.visited_positions.add((int(self.x), int(self.y)))
        self.map[(int(self.x), int(self.y))] = 'visited'

        # Clear radar data
        self.radars.clear()

        # Check radar distances at various angles (360 degrees)
        for d in range(0, 360, 15):  # Increased resolution of radar beams
            self.check_radar(d, environment)

        # Mark obstacles on the map
        for radar in self.radars:
            position, distance = radar
            if environment.is_position_obstacle(position[0], position[1]):
                self.map[(int(position[0]), int(position[1]))] = 'obstacle'

        # Check collision with obstacles or out of bounds
        if self.detect_collision(environment):
            self.is_alive = False

    def check_radar(self, degree, environment):
        radar_length = 0
        x = int(self.rect.centerx)
        y = int(self.rect.centery)

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

        dist = int(math.sqrt(math.pow(x - self.rect.centerx, 2) + math.pow(y - self.rect.centery, 2)))
        self.radars.append([(x, y), dist])

    def draw_radar(self, screen):
        if not self.visualize:
            return

        # Draw radar lines on the screen
        for radar in self.radars:
            position, distance = radar
            pygame.draw.line(screen, GREEN, self.rect.center, position, 1)
            pygame.draw.circle(screen, GREEN, position, 3)

            font = pygame.font.Font(None, 24)
            text = font.render(str(distance), True, BLACK)
            screen.blit(text, position)

    def perform_action(self, action):
        if action == 0:  # Small left turn
            self.angle += 3
        elif action == 1:  # Large left turn
            self.angle += 6
        elif action == 2:  # Small right turn
            self.angle -= 3
        elif action == 3:  # Large right turn
            self.angle -= 6
        elif action == 4:  # Accelerate
            self.speed = min(self.speed + 0.5, 10)
        elif action == 5:  # Decelerate
            self.speed = max(self.speed - 0.5, 2)
        elif action == 6:  # Reverse
            self.speed = -min(abs(self.speed) + 0.5, 2)

        # Check for collisions
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
        self.path.clear()
        self.map.clear()
        self.rect.topleft = (self.x, self.y)

        # Initialize radars to some default values (e.g., max distance)
        for d in range(0, 360, 30):
            self.radars.append([(self.x, self.y), 100])

    def get_state(self):
        state = [self.speed, self.angle]

        fixed_radar_count = 24  # Increased radar count for better sensing

        while len(self.radars) < fixed_radar_count:
            self.radars.append([(self.x, self.y), 100])

        for radar in self.radars:
            state.append(radar[1])

        fixed_state_size = 26  # Speed + Angle + 24 radar distances
        while len(state) < fixed_state_size:
            state.append(0)

        return state

    def get_reward(self):
        reward = 0

        min_distance_to_obstacle = min(radar[1] for radar in self.radars)
        if min_distance_to_obstacle < 35:
            reward -= (35 - min_distance_to_obstacle) * 2

        if self.speed > 0:
            reward += 0.1

        current_position = (int(self.rect.centerx), int(self.rect.centery))
        if current_position not in self.visited_positions:
            reward += 50  # Heavily reward for exploring a new area
            self.visited_positions.add(current_position)
        else:
            reward -= 0.1  # Small penalty for revisiting an area

        if min_distance_to_obstacle > 50:
            reward += 5

        left_value = sum(radar[1] for radar in self.radars[:len(self.radars) // 3])
        right_value = sum(radar[1] for radar in self.radars[-len(self.radars) // 3:])
        forward_value = sum(radar[1] for radar in self.radars[len(self.radars) // 3:-len(self.radars) // 3])

        if forward_value >= max(left_value, right_value):
            reward += 2
        elif left_value > right_value:
            reward += 1
        else:
            reward += 1

        if not self.is_alive:
            reward -= 100

        return reward

    def is_car_alive(self):
        return self.is_alive

    def detect_collision(self, environment):
        if (self.rect.left < 0 or self.rect.right > environment.screen_width or
                self.rect.top < 0 or self.rect.bottom > environment.screen_height):
            return True

        car_center = self.rect.center
        if environment.is_position_obstacle(car_center[0], car_center[1]):
            return True

        return False

    def find_frontiers(self):
        frontiers = []
        for (x, y) in self.visited_positions:
            neighbors = [(x + self.width, y), (x - self.width, y), (x, y + self.height), (x, y - self.height)]
            for nx, ny in neighbors:
                if (nx, ny) not in self.visited_positions and (nx, ny) not in self.map:
                    frontiers.append((nx, ny))
        return frontiers

    def choose_frontier(self, frontiers):
        min_distance = float('inf')
        target_frontier = None
        for frontier in frontiers:
            distance = math.hypot(frontier[0] - self.x, frontier[1] - self.y)
            if distance < min_distance:
                min_distance = distance
                target_frontier = frontier
        return target_frontier

    def move_to_frontier(self, frontier):
        dx = frontier[0] - self.x
        dy = frontier[1] - self.y
        if abs(dx) > abs(dy):
            if dx > 0:
                self.angle = 0  # Move right
            else:
                self.angle = 180  # Move left
        else:
            if dy > 0:
                self.angle = 90  # Move down
            else:
                self.angle = 270  # Move up
        self.speed = min(2, math.hypot(dx, dy))

    def explore(self):
        frontiers = self.find_frontiers()
        if frontiers:
            target_frontier = self.choose_frontier(frontiers)
            if target_frontier:
                self.move_to_frontier(target_frontier)
        else:
            self.speed = 0

    def visualize_map(self):
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')

        for (x, y) in self.map:
            if self.map[(x, y)] in ['visited', 'obstacle']:
                if x < min_x: min_x = x
                if y < min_y: min_y = y
                if x > max_x: max_x = x
                if y > max_y: max_y = y

        for y in range(min_y, max_y + 1):
            row = ""
            for x in range(min_x, max_x + 1):
                if (x, y) in self.map:
                    if self.map[(x, y)] == 'visited':
                        row += '.'
                    elif self.map[(x, y)] == 'obstacle':
                        row += '#'
                else:
                    row += ' '
            if row.strip():
                print(row)

    def visualize_map_to_string(self):
        map_str = ""
        for y in range(self.environment.screen_height):
            for x in range(self.environment.screen_width):
                if (x, y) in self.map:
                    if self.map[(x, y)] == 'visited':
                        map_str += '.'
                    elif self.map[(x, y)] == 'obstacle':
                        map_str += '#'
                else:
                    map_str += ' '
            map_str += '\n'
        return map_str
