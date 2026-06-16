#!/bin/bash

# Define the Python scripts
GENERATOR_SCRIPT="generator.py"
ETL_SCRIPT="run-etl.py"

# Function to kill a script given its name
kill_script() {
    SCRIPT_NAME=$1
    echo "Killing all processes matching $SCRIPT_NAME"
    pkill -f $SCRIPT_NAME
    if [ $? -eq 0 ]; then
        echo "Successfully killed $SCRIPT_NAME"
    else
        echo "Failed to kill $SCRIPT_NAME or no process found"
    fi
}

# Kill the generator and ETL scripts
kill_script "$GENERATOR_SCRIPT"
kill_script "$ETL_SCRIPT"
