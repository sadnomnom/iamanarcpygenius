import sys
import importlib
from pathlib import Path
from typing import List, Dict
from scripts.helpers.logging_utils import get_logger

logger = get_logger(__name__)

def check_dependencies() -> Dict[str, bool]:
    """Check if all required packages are installed."""
    required_packages = {
        'arcpy': 'ArcGIS installation',
        'click': 'CLI support',
        'pandas': 'Data processing',
        'yaml': 'Configuration',
        'pytest': 'Testing'
    }
    
    results = {}
    for package, description in required_packages.items():
        try:
            importlib.import_module(package)
            results[package] = True
            logger.info(f"✓ {package} (for {description})")
        except ImportError:
            results[package] = False
            logger.error(f"✗ {package} (for {description})")
    
    return results

def verify_arcpy_environment() -> bool:
    """Verify ArcGIS/arcpy environment setup."""
    try:
        import arcpy
        # Test basic arcpy functionality
        arcpy.env.overwriteOutput = True
        logger.info("✓ ArcPy environment configured successfully")
        return True
    except Exception as e:
        logger.error(f"✗ ArcPy environment error: {e}")
        return False

def verify_directories() -> bool:
    """Verify required directories exist."""
    from config.fixed_paths import (
        MXD_INPUT_DIR, 
        APRX_INPUT_DIR, 
        PDF_OUTPUT_DIR, 
        LOGS_DIR
    )
    
    required_dirs = [
        MXD_INPUT_DIR,
        APRX_INPUT_DIR,
        PDF_OUTPUT_DIR,
        LOGS_DIR
    ]
    
    all_exist = True
    for directory in required_dirs:
        if directory.exists():
            logger.info(f"✓ Directory exists: {directory}")
        else:
            logger.error(f"✗ Missing directory: {directory}")
            all_exist = False
    
    return all_exist

def run_verification() -> bool:
    """Run all verification checks."""
    logger.info("Starting environment verification...")
    
    # Check Python version
    python_version = sys.version_info
    logger.info(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Run all checks
    dep_results = check_dependencies()
    arcpy_ok = verify_arcpy_environment()
    dirs_ok = verify_directories()
    
    # Overall status
    all_passed = all(dep_results.values()) and arcpy_ok and dirs_ok
    
    if all_passed:
        logger.info("✓ All verification checks passed")
    else:
        logger.error("✗ Some verification checks failed")
    
    return all_passed

if __name__ == '__main__':
    success = run_verification()
    sys.exit(0 if success else 1)
