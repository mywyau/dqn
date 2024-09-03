# import pygame
# from car import Car
# from environment import Environment  # Your existing environment class
# from maze_environment import MazeEnvironment  # The new maze environment class
# from car_environment import CarEnvironment
#
#
# def run_simulation(env_type='default'):
#     pygame.init()
#     screen_width, screen_height = 1200, 800
#
#     if env_type == 'maze':
#         environment = MazeEnvironment(screen_width, screen_height)
#     else:
#         environment = Environment(screen_width, screen_height, obstacle_count=10)
#
#     car = Car(100, 100, environment)
#     car_env = CarEnvironment(car, environment)
#
#     state = car_env.reset()
#
#     running = True
#     clock = pygame.time.Clock()
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#         action = 4  # Example action to move the car forward
#         next_state, reward, done = car_env.step(action)
#
#         if done:
#             car_env.reset()
#
#         clock.tick(30)  # Control the frame rate
#
#     pygame.quit()
#
# if __name__ == "__main__":
#     run_simulation('maze')  # To run the maze environment
#     # run_simulation('obstacle')  # To run the obstacle environment
