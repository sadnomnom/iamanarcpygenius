while ($true) {
    # Check for changes
    $status = git status --porcelain
    if ($status) {
        Write-Host "Changes detected. Committing and pushing..."
        
        # Add all changes
        git add .
        
        # Create commit with timestamp
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "Auto-sync: $timestamp"
        
        # Push changes
        git push
        
        Write-Host "Changes pushed successfully!"
    }
    
    # Wait 30 seconds before checking again
    Start-Sleep -Seconds 30
}