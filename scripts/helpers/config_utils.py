import yaml
from pathlib import Path
from typing import Dict, Any
from scripts.helpers.logging_utils import get_logger

logger = get_logger(__name__)

def load_config(config_path: Path = Path("config/settings.yaml")) -> Dict[str, Any]:
    """Loads configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"Failed to load config from {config_path}: {e}")
        return {}

def save_config(config: Dict[str, Any], config_path: Path = Path("config/settings.yaml")):
    """Saves configuration to YAML file."""
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        logger.info(f"Saved config to {config_path}")
    except Exception as e:
        logger.error(f"Failed to save config to {config_path}: {e}")
