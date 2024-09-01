import logging
import os
import sys

import pygame

from config import screen_width


def load_map_image(script_dir):
    """Loads the map image from the specified directory."""
    map_path = os.path.join(script_dir, '..', 'resources', 'car_door.png')
    try:
        map_image = pygame.image.load(map_path)
        logging.info(f"Map loaded from {map_path}")
        return map_image
    except pygame.error as e:
        logging.error(f"Unable to load map image: {e}")
        sys.exit(1)


def draw_screen(screen, map_image, cars, generation, remain_cars):
    """Draws the game screen including cars and generation info."""
    screen.blit(map_image, (0, 0))
    for car in cars:
        if car.get_alive():
            car.draw(screen)

    generation_font = pygame.font.SysFont("Arial", 70)
    font = pygame.font.SysFont("Arial", 30)

    generation_text = generation_font.render(f"Generation : {generation}", True, (255, 255, 0))
    generation_text_rect = generation_text.get_rect(center=(screen_width / 2, 100))
    screen.blit(generation_text, generation_text_rect)

    cars_text = font.render(f"Remain cars : {remain_cars}", True, (0, 0, 0))
    cars_text_rect = cars_text.get_rect(center=(screen_width / 2, 200))
    screen.blit(cars_text, cars_text_rect)

    pygame.display.flip()
