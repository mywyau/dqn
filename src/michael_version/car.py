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

        # Check radar distances at various angles (front and sides only)
        for d in range(-90, 91, 15):  # Angles from -90 to 90 degrees (front and sides)
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
            self.speed = min(self.speed + 1.5, 11)
        elif action == 5:  # Decelerate
            self.speed = max(self.speed - 1, 3)
        elif action == 6:  # Reverse
            self.speed = -min(abs(self.speed) + 1, 2)

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
        for d in range(-90, 91, 30):  # Adjusted radar angles to match the front and sides
            self.radars.append([(self.x, self.y), 100])

    def get_state(self):
        state = [self.speed, self.angle]

        fixed_radar_count = 12  # Adjusted radar count to match the reduced number of beams

        while len(self.radars) < fixed_radar_count:
            self.radars.append([(self.x, self.y), 100])

        for radar in self.radars:
            state.append(radar[1])

        fixed_state_size = 15  # Speed + Angle + 12 radar distances
        while len(state) < fixed_state_size:
            state.append(0)

        return state

    def get_reward(self):
        reward = 0

        # Distance-based reward for moving away from the start
        start_distance = math.hypot(self.x - self.environment.start_x, self.y - self.environment.start_y)
        reward += start_distance * 0.01  # Encourage moving away from the start

        # Penalize the car for getting too close to obstacles
        min_distance_to_obstacle = min(radar[1] for radar in self.radars)
        if min_distance_to_obstacle < 35:
            reward -= (35 - min_distance_to_obstacle) * 2

        # Reward for moving forward with a higher reward for higher speed
        if self.speed > 0:
            reward += 0.1 * self.speed  # Scale the reward by the speed

        # Heavy reward for exploring new areas
        current_position = (int(self.rect.centerx), int(self.rect.centery))
        radar_range = max(radar[1] for radar in self.radars)  # Use the radar range as the size of the visited area
        if not self.is_position_visited(current_position, radar_range):
            reward += 100
            self.mark_area_as_visited(current_position, radar_range)  # Mark the area within radar range as visited
        else:
            reward -= 0.5  # Increase the penalty for revisiting an area

        # Incremental penalty for staying in the same area
        if len(self.path) > 20:  # After 10 steps, check for stagnation
            recent_positions = self.path[-20:]
            mean_x = sum(p[0] for p in recent_positions) / 10
            mean_y = sum(p[1] for p in recent_positions) / 10
            variance = sum((math.hypot(p[0] - mean_x, p[1] - mean_y)) for p in recent_positions)
            if variance < 10:  # Adjust this threshold as needed
                reward -= 2  # Increase the penalty for lack of movement

        # # Penalize large angle changes to encourage smooth turning
        # if hasattr(self, 'prev_angle'):
        #     angle_change_penalty = abs(self.angle - self.prev_angle) * 0.2  # Reduce the penalty factor
        #     reward -= angle_change_penalty
        # self.prev_angle = self.angle

        # Penalty for high speed in sharp corners, scaled to speed
        if self.is_approaching_corner():
            reward -= self.speed * 0.1  # Reduce the penalty for high speed in corners

        # Reward for maintaining a safe distance from obstacles
        if min_distance_to_obstacle > 50:
            reward += 5

        # Bonus for moving towards the most open direction, scaled for stronger guidance
        left_value = sum(radar[1] for radar in self.radars[:len(self.radars) // 3])
        right_value = sum(radar[1] for radar in self.radars[-len(self.radars) // 3:])
        forward_value = sum(radar[1] for radar in self.radars[len(self.radars) // 3:-len(self.radars) // 3])

        if forward_value >= max(left_value, right_value):
            reward += 3  # Increase reward for moving forward
        elif left_value > right_value:
            reward += 1.5  # Adjusted to encourage smoother left turns
        else:
            reward += 1.5  # Adjusted to encourage smoother right turns

        # Heavy penalty if the car collides with an obstacle or goes out of bounds
        if not self.is_alive:
            reward -= 100

        return reward

    def is_position_visited(self, position, radius):
        """Check if the given position or its surrounding area has been visited based on radar range."""
        x, y = position
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx ** 2 + dy ** 2 <= radius ** 2:  # Check if within the radar range
                    if (x + dx, y + dy) in self.visited_positions:
                        return True
        return False

    def mark_area_as_visited(self, position, radius):
        """Mark a circular area around the position as visited based on radar range."""
        x, y = position
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx ** 2 + dy ** 2 <= radius:  # Check if within the radar range
                    self.visited_positions.add((x + dx, y + dy))

    def is_approaching_corner(self):
        # A simple heuristic to determine if a corner is ahead
        angle_changes = [abs(self.angle - prev_angle) for prev_angle in [self.angle - 15, self.angle + 15]]
        return max(angle_changes) > 30  # Example threshold, tune as necessary

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
