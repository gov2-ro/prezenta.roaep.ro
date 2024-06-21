#!/bin/bash

# Define the path to merge-pvs.py
MERGE_PVS_SCRIPT="./merge-pvs.py"

# List of commands to run
commands=(
    "$MERGE_PVS_SCRIPT --functie p --pv-type final"
    "$MERGE_PVS_SCRIPT --functie pcj --pv-type final"
    "$MERGE_PVS_SCRIPT --functie cj --pv-type final"
    "$MERGE_PVS_SCRIPT --functie cl --pv-type final"

    "$MERGE_PVS_SCRIPT --functie p --pv-type part"
    "$MERGE_PVS_SCRIPT --functie pcj --pv-type part"
    "$MERGE_PVS_SCRIPT --functie cj --pv-type part"
    "$MERGE_PVS_SCRIPT --functie cl --pv-type part"
)

# Run each command
for command in "${commands[@]}"
do
    echo "Running: $command"
    python3 $command
    if [ $? -ne 0 ]; then
        echo "Command failed: $command"
    else
        echo "Command succeeded: $command"
    fi
done
