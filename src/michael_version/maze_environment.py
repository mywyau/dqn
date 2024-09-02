import random
import pygame

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class MazeEnvironment:
    def __init__(self, screen_width, screen_height, cell_size=80):
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

        # Set an open starting position for the car
        self.start_x, self.start_y = self.find_open_start()

    def generate_maze(self):
        # Initialize starting point
        current_cell = (0, 0)
        self.visited.append(current_cell)
        self.stack.append(current_cell)
        self.grid[current_cell[1]][current_cell[0]] = 0  # Mark the start as an open path

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

        print(f"Maze grid generated: {self.grid}")

    def get_neighbors(self, cell):
        neighbors = []
        x, y = cell
        if x > 1 and (x - 2, y) not in self.visited:  # Left (skipping 1 cell to ensure proper wall between cells)
            neighbors.append((x - 2, y))
        if x < self.columns - 2 and (x + 2, y) not in self.visited:  # Right
            neighbors.append((x + 2, y))
        if y > 1 and (x, y - 2) not in self.visited:  # Up
            neighbors.append((x, y - 2))
        if y < self.rows - 2 and (x, y + 2) not in self.visited:  # Down
            neighbors.append((x, y + 2))
        return neighbors

    def remove_wall(self, current, next):
        x1, y1 = current
        x2, y2 = next

        self.grid[y2][x2] = 0  # Mark next cell as a path

        # Remove the wall between cells (modify the cell in between to be part of the path)
        if x1 == x2:  # Moving vertically
            self.grid[min(y1, y2) + 1][x1] = 0
        elif y1 == y2:  # Moving horizontally
            self.grid[y1][min(x1, x2) + 1] = 0

    def draw(self, screen):
        screen.fill(WHITE)
        for y in range(self.rows):
            for x in range(self.columns):
                if self.grid[y][x] == 1:  # 1 means wall
                    pygame.draw.rect(screen, BLACK,
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def is_position_obstacle(self, x, y):
        """Check if the given (x, y) position is occupied by a maze wall."""
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        if grid_x >= self.columns or grid_y >= self.rows or grid_x < 0 or grid_y < 0:
            return True  # Treat out-of-bounds as obstacles
        return self.grid[grid_y][grid_x] == 1  # Return True if it's a wall (1)

    def find_open_start(self):
        """Find an open position in the middle of a path to start."""
        for y in range(1, self.rows - 1):
            for x in range(1, self.columns - 1):
                if self.grid[y][x] == 0 and self.grid[y - 1][x] == 0 and self.grid[y + 1][x] == 0 and self.grid[y][x - 1] == 0 and self.grid[y][x + 1] == 0:
                    return x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2
        return 30, 30  # Default to (30, 30) if no open path is found
