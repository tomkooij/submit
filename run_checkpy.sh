#!/bin/bash
while true
do
    echo "Running Checkpy. Inifite loop. Press [CTRL+C] to stop.."
    python run_checkpy.py >> checkpy.log
    sleep 60
done
