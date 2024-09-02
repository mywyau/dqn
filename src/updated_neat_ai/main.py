import os
import sys
import logging
import neat
from car_simulation import run_car
from neat_config_loader import load_neat_config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config = load_neat_config(script_dir)

    # Create core evolution algorithm class
    p = neat.Population(config)

    # Add reporter for fancy statistical results
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    logging.info("Starting NEAT evolution.")
    p.run(run_car, 1000)
    logging.info("NEAT evolution finished.")
