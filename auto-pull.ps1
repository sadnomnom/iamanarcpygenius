# Create auto-pull.ps1
New-Item -ItemType File -Path "auto-pull.ps1" -Value @'
while ($true) {
    Write-Host "Checking for updates..."
    
    # Fetch and pull changes
    git fetch
    $status = git pull
    
    if ($status -match "Already up to date") {
        Write-Host "No new changes."
    } else {
        Write-Host "Updated with new changes!"
    }
    
    # Wait 30 seconds before checking again
    Start-Sleep -Seconds 30
}
'@