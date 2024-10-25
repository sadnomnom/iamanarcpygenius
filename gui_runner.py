import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from scripts.tkinter_gui import MapProcessorGUI
from scripts.helpers.logging_utils import setup_file_logger
from config.fixed_paths import LOGS_DIR, ensure_directories

def main():
    """Main entry point for the GUI application."""
    # Ensure directories exist
    ensure_directories()
    
    # Setup logging
    logger = setup_file_logger("gui_runner", LOGS_DIR)
    logger.info("Starting GUI application")
    
    # Create and run GUI
    app = MapProcessorGUI()
    app.run()

if __name__ == "__main__":
    main()
