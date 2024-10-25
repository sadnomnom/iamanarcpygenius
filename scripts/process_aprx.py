import arcpy
from pathlib import Path
from typing import Optional
from scripts.helpers.logging_utils import get_logger

logger = get_logger(__name__)

class APRXProcessor:
    """Handles processing of ArcGIS Pro .aprx files."""
    
    def __init__(self, aprx_path: Path):
        self.aprx_path = Path(aprx_path)
        self.aprx = None
        self.layout = None
    
    def open_file(self):
        """Opens the APRX file."""
        try:
            self.aprx = arcpy.mp.ArcGISProject(str(self.aprx_path))
            # Get the first layout (usually the one we want)
            self.layout = self.aprx.listLayouts()[0]
            logger.info(f"Opened APRX file: {self.aprx_path}")
        except Exception as e:
            logger.error(f"Failed to open APRX file: {e}")
            raise
    
    def export_to_pdf(self, output_path: Path, resolution: int = 300) -> Optional[Path]:
        """Exports the APRX to PDF format."""
        try:
            if not self.layout:
                raise ValueError("No layout found in APRX file")
                
            self.layout.exportToPDF(str(output_path), resolution=resolution)
            logger.info(f"Exported PDF to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to export PDF: {e}")
            return None
    
    def close(self):
        """Closes the APRX file."""
        if self.aprx:
            del self.aprx
