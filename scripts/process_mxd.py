import arcpy
from pathlib import Path
from typing import Optional
from scripts.helpers.logging_utils import get_logger
from scripts.helpers.arcpy_helpers import setup_arcpy_env

logger = get_logger(__name__)

class MXDProcessor:
    """Handles processing of ArcMap .mxd files."""
    
    def __init__(self, mxd_path: Path):
        self.mxd_path = mxd_path
        self.mxd = None
    
    def open_mxd(self):
        """Opens the MXD file."""
        try:
            self.mxd = arcpy.mapping.MapDocument(str(self.mxd_path))
            logger.info(f"Opened MXD file: {self.mxd_path}")
        except Exception as e:
            logger.error(f"Failed to open MXD file: {e}")
            raise
    
    def export_to_pdf(self, output_path: Path, resolution: int = 300) -> Optional[Path]:
        """Exports the MXD to PDF format."""
        try:
            arcpy.mapping.ExportToPDF(self.mxd, str(output_path), resolution=resolution)
            logger.info(f"Exported PDF to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to export PDF: {e}")
            return None
    
    def close(self):
        """Closes the MXD file."""
        if self.mxd:
            del self.mxd
