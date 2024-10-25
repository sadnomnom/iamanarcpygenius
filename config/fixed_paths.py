import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Input directories
MXD_INPUT_DIR = PROJECT_ROOT / "data" / "input" / "mxd"
APRX_INPUT_DIR = PROJECT_ROOT / "data" / "input" / "aprx"

# Output directories
PDF_OUTPUT_DIR = PROJECT_ROOT / "data" / "output" / "pdf"
LOGS_DIR = PROJECT_ROOT / "data" / "output" / "logs"

# Config file path
SETTINGS_PATH = PROJECT_ROOT / "config" / "settings.yaml"

def ensure_directories():
    """Ensure all required directories exist."""
    for directory in [MXD_INPUT_DIR, APRX_INPUT_DIR, PDF_OUTPUT_DIR, LOGS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
