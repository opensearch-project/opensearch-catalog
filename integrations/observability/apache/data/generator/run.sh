#!/bin/bash

# Define the Python script and requirements file
PYTHON_SCRIPT="generator.py"
REQUIREMENTS_FILE="requirements.txt"

# Check if the Python script and requirements file exist
if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    echo "Python script '$PYTHON_SCRIPT' does not exist."
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

# Run the Python script
echo "Running script '$PYTHON_SCRIPT'..."
python "$PYTHON_SCRIPT" "$@"

# Check if the Python script ran successfully
if [[ $? -ne 0 ]]; then
    echo "Script '$PYTHON_SCRIPT' failed to run."
    exit 1
else
    echo "Script '$PYTHON_SCRIPT' ran successfully."
fi
