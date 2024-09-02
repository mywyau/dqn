import logging
import os
import sys

import neat


def load_neat_config(script_dir):
    config_path = os.path.join(script_dir, 'config-feedforward.txt')
    try:
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )
        return config
    except Exception as e:
        logging.error(f"Error loading NEAT configuration: {e}")
        sys.exit(1)
