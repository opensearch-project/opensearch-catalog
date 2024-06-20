#!/bin/bash

# Define the Python scripts and requirements file
GENERATOR_SCRIPT="generator.py"
ETL_SCRIPT="run-etl.py"
REQUIREMENTS_FILE="requirements.txt"

# Check if the Python scripts and requirements file exist
if [[ ! -f "$GENERATOR_SCRIPT" ]]; then
    echo "Python script '$GENERATOR_SCRIPT' does not exist."
    exit 1
fi

if [[ ! -f "$ETL_SCRIPT" ]]; then
    echo "Python ETL script '$ETL_SCRIPT' does not exist."
    exit 1
fi

if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
    echo "Requirements file '$REQUIREMENTS_FILE' does not exist."
    exit 1
fi

# Install the required Python packages
echo "Installing requirements from '$REQUIREMENTS_FILE'..."
pip install -r "$REQUIREMENTS_FILE"

# Check if pip install succeeded
if [[ $? -ne 0 ]]; then
    echo "Failed to install required packages."
    exit 1
fi

# Run the generator Python script in the background
echo "Running script '$GENERATOR_SCRIPT' in the background..."
nohup python "$GENERATOR_SCRIPT" "$@" &

# Run the ETL Python script in the background
echo "Running ETL script '$ETL_SCRIPT' in the background..."
nohup python "$ETL_SCRIPT" "$@" &

# Wait for all background jobs to finish
wait

echo "Both scripts are now running in the background."

echo "redirect the stdout and stderr of the generator script to generator.log and the ETL script to etl.log"
nohup python "$GENERATOR_SCRIPT" "$@" > generator.log 2>&1 &
nohup python "$ETL_SCRIPT" "$@" > etl.log 2>&1 &