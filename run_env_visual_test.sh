#!/bin/bash

# Set the PYTHONPATH to include the src directory
export PYTHONPATH=$(pwd)/src

# Set the environment variable to enable visualization
export VISUALIZE_TEST=1

# Run the specific unittest module
python3 -m unittest tests.test_environment_visualization

# Unset the environment variable after the test is complete
unset VISUALIZE_TEST

# Unset the PYTHONPATH after the test is complete
unset PYTHONPATH
