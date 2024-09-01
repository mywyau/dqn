# import pygame
# import sys
# from environment import Environment, WHITE
# from car_environment import Car
#
# # Initialize Pygame
# pygame.init()
#
# # Set up display
# screen_width, screen_height = 800, 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Randomized Environment with Car")
#
# # Set up the clock for managing the frame rate
# clock = pygame.time.Clock()
#
# # Initialize Environment and Car
# environment = Environment(screen_width, screen_height, obstacle_count=15)
# car = Car(100, 100, environment)
#
# # Main loop
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#     # Update the car's position
#     car.update()
#
#     # Fill the screen with a color (e.g., white)
#     screen.fill(WHITE)
#
#     # Draw the environment and car
#     environment.draw(screen)
#     car.draw(screen)
#
#     # Update the display
#     pygame.display.flip()
#
#     # Cap the frame rate at 60 FPS
#     clock.tick(60)

# main.py
import sys
from train_dqn import train_dqn
from test_dqn import test_dqn

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [train|test]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "train":
        train_dqn(1000)  # Train for 1000 episodes
    elif mode == "test":
        test_dqn()  # Test the trained model
    else:
        print("Invalid mode. Choose 'train' or 'test'.")
        sys.exit(1)
