from pathlib import Path
from typing import List, Union
from scripts.helpers.logging_utils import get_logger
from scripts.process_mxd import MXDProcessor
from scripts.process_aprx import APRXProcessor

logger = get_logger(__name__)

class FileHandler:
    """Handles file operations for both MXD and APRX files."""
    
    def __init__(self):
        self.supported_extensions = {'.mxd', '.aprx'}
    
    def validate_file(self, file_path: Path) -> bool:
        """Validates if the file exists and has a supported extension."""
        return file_path.exists() and file_path.suffix.lower() in self.supported_extensions
    
    def process_file(self, input_path: Path, output_path: Path, resolution: int = 300) -> bool:
        """Processes a single file (MXD or APRX) and exports to PDF."""
        if not self.validate_file(input_path):
            logger.error(f"Invalid file: {input_path}")
            return False
        
        try:
            if input_path.suffix.lower() == '.mxd':
                processor = MXDProcessor(input_path)
                processor.open_mxd()
            else:
                processor = APRXProcessor(input_path)
                processor.open_aprx()
            
            result = processor.export_to_pdf(output_path, resolution)
            processor.close()
            return result is not None
            
        except Exception as e:
            logger.error(f"Error processing file {input_path}: {e}")
            return False
