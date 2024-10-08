#!/bin/bash

# Set the base directory to the script's location
BASE_DIR=$(dirname "$0")

# Activate Python virtual environment if necessary
# Uncomment and modify the following line if you're using a virtual environment
# source "$BASE_DIR/../.venv/bin/activate"

# Navigate to the directory containing the script
cd "$BASE_DIR/src/michael_version/"

# Run the simulation
python3 test_dqn.py

# Optionally, deactivate the virtual environment after running the script
# deactivate
