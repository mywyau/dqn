import os
import logging

import neat
import pygame
from Car import Car
from config import screen_width, screen_height
from event_handler import handle_events
from graphics import draw_screen, load_map_image

def initialize_neural_networks(genomes, config):
    """Initializes neural networks and cars for the given genomes."""
    nets, cars = [], []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
        cars.append(Car())
    return nets, cars

def update_car_fitness(cars, nets, genomes, map_image):
    """Updates the fitness of the cars and checks if any are alive."""
    remain_cars = 0
    all_stuck = True

    for i, car in enumerate(cars):
        if car.get_alive():
            remain_cars += 1
            car.update(map_image)
            genomes[i][1].fitness += car.get_reward()

            if not car.is_stuck():
                all_stuck = False

            output = nets[i].activate(car.get_data())
            car.perform_action(output)

    return remain_cars, all_stuck

from config import generation, TIME_LIMIT_PER_GENERATION

def run_car(genomes, config):
    """Runs the simulation for a generation of cars."""
    global generation
    generation += 1  # Increment generation count

    nets, cars = initialize_neural_networks(genomes, config)

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    map_image = load_map_image(script_dir)

    current_time_step = 0

    while current_time_step < TIME_LIMIT_PER_GENERATION:
        handle_events()

        remain_cars, all_stuck = update_car_fitness(cars, nets, genomes, map_image)

        if remain_cars == 0 or all_stuck:
            logging.info("All cars have been terminated or are stuck. Ending generation.")
            break

        draw_screen(screen, map_image, cars, generation, remain_cars)

        clock.tick(5)
        current_time_step += 1

    if current_time_step >= TIME_LIMIT_PER_GENERATION:
        logging.info(f"Generation time limit of {TIME_LIMIT_PER_GENERATION} frames reached. Ending generation.")
