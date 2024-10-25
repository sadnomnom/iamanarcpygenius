import arcpy
from pathlib import Path
from typing import Optional
from scripts.helpers.logging_utils import get_logger

logger = get_logger(__name__)

def setup_arcpy_env():
    """Sets up the ArcPy environment with common settings."""
    arcpy.env.overwriteOutput = True
    arcpy.env.addOutputsToMap = False

def check_arcpy_license(extension: Optional[str] = None) -> bool:
    """Checks if required ArcGIS license/extension is available."""
    try:
        if extension:
            if arcpy.CheckExtension(extension) == "Available":
                arcpy.CheckOutExtension(extension)
                return True
            return False
        return True
    except Exception as e:
        logger.error(f"License check failed: {e}")
        return False

def release_arcpy_license(extension: Optional[str] = None):
    """Releases checked out ArcGIS extension license."""
    if extension:
        try:
            arcpy.CheckInExtension(extension)
        except Exception as e:
            logger.error(f"Failed to release license: {e}")
