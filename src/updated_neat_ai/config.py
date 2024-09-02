# config.py

# Screen settings
screen_width = 1200
screen_height = 800

# Car settings
MAX_LIFETIME = 50  # Maximum lifetime of a car in the simulation

# NEAT configuration
NEAT_CONFIG_PATH = "config-feedforward.txt"  # Path to the NEAT configuration file

# Logging settings
LOGGING_LEVEL = "INFO"

# Other settings (if needed)
INITIAL_CAR_POSITION = [200, 480]  # Default starting position of the car
CAR_SIZE = (30, 30)  # Size of the car image after scaling
MAX_SPEED = 6.0  # Maximum speed a car can achieve
MIN_SPEED = 1.0  # Minimum speed a car can have
REVERSE_SPEED = 2.0  # Speed when the car is reversing

# Radar settings
RADAR_ANGLES = [-90, -60, -30, 0, 30, 60, 90]  # Angles at which radars are positioned
RADAR_MAX_DISTANCE = 500  # Maximum distance for radar to detect

# Rewards and penalties
REWARD_NEW_POSITION = 2000  # Reward for exploring a new position
PENALTY_REPEAT_POSITION = 100  # Penalty for revisiting the same position
PENALTY_TIME_SPENT = 0.01  # Penalty per time unit spent in the simulation
PENALTY_STUCK = 500  # Penalty if the car revisits the same position after 50 time units

# Generation settings
generation = 0  # Initialize generation counter
TIME_LIMIT_PER_GENERATION = 2000  # Time limit for each generation in frames

# Example: Random exploration settings (optional)
EXPLORATION_RATE_DECAY = 1000  # The generation count after which exploration rate starts decaying
MIN_EXPLORATION_RATE = 0.1  # Minimum exploration rate

# Example: Map settings (if needed)
MAP_IMAGE_PATH = "resources/car_door.png"  # Path to the map image
