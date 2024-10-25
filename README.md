# Map Processing Pipeline

A Python tool for processing ArcGIS map files (.mxd and .aprx) and converting them to PDF format.

## Setup

1. Clone this repository
2. Run the setup script:
   - Windows: `.\create_project_structure.ps1`
   - Unix/Linux: `./create_project_structure.sh`

## Requirements

- Python 3.7+
- ArcGIS installation (for arcpy)
- Additional requirements listed in requirements.txt

## Usage

### GUI Mode


## Deployment

When deploying to a new environment:

1. Ensure ArcGIS is installed and arcpy is available
2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```
3. Create and activate a virtual environment:
   - Windows: 
     ```powershell
     .\create_project_structure.ps1
     ```
   - Unix/Linux:
     ```bash
     ./create_project_structure.sh
     ```
4. Verify the environment:
   ```bash
   python -m scripts.cli verify
   ```

### Troubleshooting

If verification fails:
1. Check the logs in `data/output/logs/`
2. Ensure ArcGIS is properly installed
3. Verify Python version matches requirements (3.7+)
4. Check that all required directories exist
5. Verify all dependencies are installed correctly
