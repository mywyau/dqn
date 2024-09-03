import math


class GeometryHelper:
    @staticmethod
    def calculate_distance(point1, point2):
        """Calculate the Euclidean distance between two points."""
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    @staticmethod
    def get_min_distance_to_obstacle(car_rect, obstacles):
        """Calculate the minimum distance from the car to any obstacle."""
        min_distance = None
        for obstacle in obstacles:
            distance = GeometryHelper.calculate_distance(car_rect.center, obstacle.center)
            if min_distance is None or distance < min_distance:
                min_distance = distance
        return min_distance

    @staticmethod
    def get_min_distance_to_border(rect, environment):
        """Calculate the minimum distance from the car to the border of the environment."""
        car_left = rect.left
        car_right = rect.right
        car_top = rect.top
        car_bottom = rect.bottom

        distance_to_left_border = car_left
        distance_to_right_border = environment.screen_width - car_right
        distance_to_top_border = car_top
        distance_to_bottom_border = environment.screen_height - car_bottom

        # Return the smallest distance to any border
        return min(distance_to_left_border, distance_to_right_border, distance_to_top_border, distance_to_bottom_border)

    @staticmethod
    def get_min_distance_to_maze_obstacle(rect, grid, cell_size):
        min_distance = None
        car_center_x, car_center_y = rect.centerx, rect.centery

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == 1:  # This is an obstacle
                    obstacle_center_x = (x * cell_size) + (cell_size // 2)
                    obstacle_center_y = (y * cell_size) + (cell_size // 2)
                    distance = math.sqrt((obstacle_center_x - car_center_x) ** 2 +
                                         (obstacle_center_y - car_center_y) ** 2)
                    if min_distance is None or distance < min_distance:
                        min_distance = distance

        return min_distance
