#!/bin/bash

while true; do
    echo "Checking for updates..."
    
    # Fetch and pull changes
    git fetch
    status=$(git pull)
    
    if [[ $status == "Already up to date" ]]; then
        echo "No new changes."
    else
        echo "Updated with new changes!"
    fi
    
    # Wait 30 seconds
    sleep 30
done
