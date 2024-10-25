from pathlib import Path
from typing import List, Optional
import shutil
from scripts.helpers.logging_utils import get_logger

logger = get_logger(__name__)

def ensure_directory(directory: Path) -> bool:
    """Ensures a directory exists, creates it if it doesn't."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        return False

def get_files_by_extension(directory: Path, extensions: List[str]) -> List[Path]:
    """Returns a list of files with specified extensions in the directory."""
    files = []
    for ext in extensions:
        files.extend(directory.glob(f"*.{ext}"))
    return files

def safe_copy_file(source: Path, destination: Path) -> bool:
    """Safely copies a file to the destination."""
    try:
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        logger.error(f"Failed to copy {source} to {destination}: {e}")
        return False
