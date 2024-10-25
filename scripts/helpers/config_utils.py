import yaml
from pathlib import Path
from typing import Dict, List, Optional
from scripts.helpers.logging_utils import get_logger

logger = get_logger(__name__)

class ConfigurationError(Exception):
    """Custom exception for configuration errors."""
    pass

def load_config() -> Dict:
    """Load and validate configuration from YAML file."""
    try:
        config_path = Path("config/settings.yaml")
        if not config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")
            
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Validate configuration
        validate_config(config)
        return config
        
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        raise ConfigurationError(f"Invalid YAML format: {e}")
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise ConfigurationError(f"Configuration error: {e}")

def validate_config(config: Dict) -> None:
    """Validate configuration structure and required fields."""
    required_sections = ['paths', 'options', 'substations']
    required_paths = ['workspace', 'mxd_input', 'aprx_input', 'pdf_output', 'logs']
    
    # Check required sections
    for section in required_sections:
        if section not in config:
            raise ConfigurationError(f"Missing required section: {section}")
    
    # Validate paths section
    for path_key in required_paths:
        if path_key not in config['paths']:
            raise ConfigurationError(f"Missing required path: {path_key}")
        path = Path(config['paths'][path_key])
        if not path.exists():
            logger.warning(f"Path does not exist: {path}")
    
    # Validate options
    if 'default_year' not in config['options']:
        raise ConfigurationError("Missing default_year in options")
    if not isinstance(config['options'].get('resolution', 300), int):
        raise ConfigurationError("Resolution must be an integer")
    
    # Validate substations
    if not isinstance(config['substations'], list):
        raise ConfigurationError("Substations must be a list")
    if not config['substations']:
        raise ConfigurationError("Substations list is empty")

def validate_substation(substation: str, config: Optional[Dict] = None) -> bool:
    """Validate if a substation exists in configuration."""
    if config is None:
        config = load_config()
    
    try:
        valid_substations = set(sub.upper() for sub in config['substations'])
        substation = substation.upper()
        
        if substation not in valid_substations:
            logger.error(f"Invalid substation: {substation}")
            logger.info(f"Valid substations: {', '.join(sorted(valid_substations))}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Error validating substation: {e}")
        return False
