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
    def get_min_distance_to_border(car_rect, screen_width, screen_height):
        """Calculate the minimum distance from the car to the borders of the environment."""
        distances = [
            car_rect.left,  # Distance to left border
            screen_width - car_rect.right,  # Distance to right border
            car_rect.top,  # Distance to top border
            screen_height - car_rect.bottom  # Distance to bottom border
        ]
        return min(distances)
