#!/bin/bash

# Temporarily set the PYTHONPATH to include the 'src' directory
export PYTHONPATH=$(pwd)/src

# Run the tests using unittest
python -m unittest discover -s tests

# Optionally, unset the PYTHONPATH after running tests (not strictly necessary in a script)
unset PYTHONPATH
