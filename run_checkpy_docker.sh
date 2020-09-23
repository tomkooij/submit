#!/bin/bash

# add locally installed checkpy (in container) to PATH
export PATH=$PATH:/home/checkpy/.local/bin

while true
do
    echo "Running Checkpy. Inifite loop. Press [CTRL+C] to stop.."
    python run_checkpy.py 
    echo "Sleep 60."
    sleep 60
done
