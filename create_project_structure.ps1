# Create base directories
$directories = @(
    "config",
    "data/input/mxd",
    "data/input/aprx",
    "data/output/pdf",
    "data/output/logs",
    "scripts/helpers",
    "tests"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir -Force
}

# Set environment variables to disable SSL verification
$env:PIP_DISABLE_PIP_VERSION_CHECK = 1
$env:PYTHONHTTPSVERIFY = 0

# Verify ArcGIS Pro environment
Write-Host "`nVerifying ArcGIS Pro environment...`n"
$arcpyVersion = python -c "import arcpy; print(arcpy.GetInstallInfo()['Version'])"
Write-Host "ArcGIS Pro version: $arcpyVersion"

# Upgrade pip and install requirements with SSL verification disabled
Write-Host "`nUpgrading pip and installing requirements...`n"
python -m pip install --upgrade pip --no-warn-script-location --disable-pip-version-check --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Install each package individually with SSL verification disabled
$packages = @(
    "click>=8.0.0",
    "pandas>=1.3.0",
    "PyYAML>=5.4.1",
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..."
    python -m pip install --no-deps --no-cache-dir --disable-pip-version-check --trusted-host pypi.org --trusted-host files.pythonhosted.org $package
}

# Create .gitkeep files
Write-Host "`nCreating .gitkeep files...`n"
New-Item "data/input/mxd/.gitkeep" -ItemType File -Force
New-Item "data/input/aprx/.gitkeep" -ItemType File -Force
New-Item "data/output/pdf/.gitkeep" -ItemType File -Force
New-Item "data/output/logs/.gitkeep" -ItemType File -Force

# Verify pytest installation
Write-Host "`nVerifying pytest installation...`n"
python -m pip list | findstr "pytest"

# Verify the structure was created
Write-Host "`nProject structure created successfully!`n"
Get-ChildItem -Recurse -Directory | Select-Object FullName

Write-Host "`nEnvironment setup complete!`n"
Write-Host "Note: Make sure you have ArcGIS installed for arcpy functionality"
Write-Host "Using ArcGIS Pro Python environment: $arcpyVersion"
