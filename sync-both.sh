#!/bin/bash

while true; do
    echo "=== Git Sync Check ==="
    
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
        
        # Add all changes
        git add .
        
        # Create commit with timestamp and hostname
        hostname=$(hostname)
        timestamp=$(date "+%Y-%m-%d %H:%M:%S")
        git commit -m "Auto-sync from $hostname: $timestamp"
        
        # Push changes
        git push
        echo "Changes pushed successfully!"
    else
        echo "No local changes to push."
    fi
    
    echo "Next check in 1 seconds..."
    echo "------------------------"
    sleep 1
done
