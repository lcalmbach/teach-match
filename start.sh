#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Change directory to src
cd src

# Run the Django development server
python3 manage.py runserver