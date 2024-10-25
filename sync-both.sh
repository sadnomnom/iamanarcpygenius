#!/bin/bash

while true; do
    echo "=== Git Sync Check ==="
    
    # Run log cleanup
    ./log-cleanup.sh
    
    # First pull any remote changes
    echo "Checking for remote changes..."
    git fetch
    pull_status=$(git pull)
    
    if [[ $pull_status == *"Already up to date"* ]]; then
        echo "No new changes to pull."
    else
        echo "Pulled new changes!"
    fi
    
    # Then check for local changes
    if [[ $(git status --porcelain) ]]; then
        echo "Local changes detected. Committing and pushing..."
        git add .
        hostname=$(hostname)
        timestamp=$(date "+%Y-%m-%d %H:%M:%S")
        git commit -m "Auto-sync from $hostname: $timestamp"
        git push
        echo "Changes pushed successfully!"
    else
        echo "No local changes to push."
    fi
    
    echo "Next check in 1 seconds..."
    echo "------------------------"
    sleep 1
done
