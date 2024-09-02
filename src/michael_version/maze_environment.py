import pygame
import random

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class MazeEnvironment:
    def __init__(self, screen_width, screen_height, cell_size=40):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.columns = screen_width // cell_size
        self.rows = screen_height // cell_size
        self.grid = [[1 for _ in range(self.columns)] for _ in range(self.rows)]
        self.visited = []
        self.stack = []

        # Generate the maze
        self.generate_maze()

    def generate_maze(self):
        # Initialize starting point
        current_cell = (0, 0)
        self.visited.append(current_cell)
        self.stack.append(current_cell)

        while len(self.stack) > 0:
            current_cell = self.stack[-1]
            neighbors = self.get_neighbors(current_cell)

            if neighbors:
                next_cell = random.choice(neighbors)
                self.remove_wall(current_cell, next_cell)
                self.stack.append(next_cell)
                self.visited.append(next_cell)
            else:
                self.stack.pop()

    def get_neighbors(self, cell):
        neighbors = []
        x, y = cell
        if x > 0 and (x - 1, y) not in self.visited:  # Left
            neighbors.append((x - 1, y))
        if x < self.columns - 1 and (x + 1, y) not in self.visited:  # Right
            neighbors.append((x + 1, y))
        if y > 0 and (x, y - 1) not in self.visited:  # Up
            neighbors.append((x, y - 1))
        if y < self.rows - 1 and (x, y + 1) not in self.visited:  # Down
            neighbors.append((x, y + 1))
        return neighbors

    def remove_wall(self, current, next):
        x1, y1 = current
        x2, y2 = next

        self.grid[y1][x1] = 0
        self.grid[y2][x2] = 0

        # Remove the wall between cells
        if x1 == x2:
            self.grid[min(y1, y2) + 1][x1] = 0
        elif y1 == y2:
            self.grid[y1][min(x1, x2) + 1] = 0

    def draw(self, screen):
        screen.fill(BLACK)
        for y in range(self.rows):
            for x in range(self.columns):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, WHITE, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def is_position_obstacle(self, x, y):
        """Check if the given (x, y) position is occupied by a maze wall."""
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        if grid_x >= self.columns or grid_y >= self.rows or grid_x < 0 or grid_y < 0:
            return True  # Treat out-of-bounds as obstacles
        return self.grid[grid_y][grid_x] == 1
