"""Configuration module for Lead Generation Bot."""

import json
import os
from pathlib import Path
from typing import Any


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


def load_config(config_path: str = "config/settings.json") -> dict[str, Any]:
    """
    Load configuration from JSON file and environment variables.
    
    Args:
        config_path: Path to the configuration JSON file
        
    Returns:
        Dictionary containing all configuration values
        
    Raises:
        ConfigurationError: If configuration file is missing, invalid, or incomplete
    """
    # Check if config file exists
    if not os.path.exists(config_path):
        raise ConfigurationError(
            f"Configuration file not found: {config_path}\n"
            f"Please create it from the example: cp config/settings.example.json {config_path}"
        )
    
    # Load JSON file
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigurationError(
            f"Invalid JSON syntax in configuration file: {config_path}\n"
            f"Error: {str(e)}"
        )
    except Exception as e:
        raise ConfigurationError(
            f"Failed to read configuration file: {config_path}\n"
            f"Error: {str(e)}"
        )
    
    # Define required fields with their types
    required_fields = {
        "GOOGLE_SHEET_ID": str,
        "GOOGLE_SERVICE_ACCOUNT_JSON": str,
        "MIN_RATING": (int, float),
        "MIN_REVIEWS": int,
        "MAX_LEADS_PER_RUN": int
    }
    
    # Optional fields (for FREE version)
    optional_fields = {
        "SERPAPI_KEY": str,
        "GEMINI_API_KEY": str,
        "GMAIL_ADDRESS": str,
        "GMAIL_APP_PASSWORD": str
    }
    
    # Validate required fields
    for field, expected_type in required_fields.items():
        # Check environment variable first
        env_value = os.getenv(field)
        if env_value is not None:
            # Try to convert env value to appropriate type
            if expected_type == int or expected_type == (int, float):
                try:
                    config[field] = int(env_value) if '.' not in env_value else float(env_value)
                except ValueError:
                    raise ConfigurationError(
                        f"Invalid value for {field} in environment variable: {env_value}"
                    )
            else:
                config[field] = env_value
        
        # Check if field exists in config
        if field not in config:
            raise ConfigurationError(
                f"Missing required configuration field: {field}\n"
                f"Please add it to {config_path} or set it as an environment variable"
            )
        
        value = config[field]
        
        # Type validation
        if not isinstance(value, expected_type):
            raise ConfigurationError(
                f"Invalid type for configuration field: {field}\n"
                f"Expected {expected_type}, got {type(value).__name__}"
            )
    
    # Load optional fields
    for field, expected_type in optional_fields.items():
        # Check environment variable first
        env_value = os.getenv(field)
        if env_value is not None:
            config[field] = env_value
        # If not in config, set to None
        if field not in config:
            config[field] = None
    
    # Additional validation
    if config["MIN_RATING"] < 0 or config["MIN_RATING"] > 5:
        raise ConfigurationError(
            f"MIN_RATING must be between 0 and 5, got {config['MIN_RATING']}"
        )
    
    if config["MIN_REVIEWS"] < 0:
        raise ConfigurationError(
            f"MIN_REVIEWS must be non-negative, got {config['MIN_REVIEWS']}"
        )
    
    if config["MAX_LEADS_PER_RUN"] < 1:
        raise ConfigurationError(
            f"MAX_LEADS_PER_RUN must be at least 1, got {config['MAX_LEADS_PER_RUN']}"
        )
    
    return config


# Global configuration (loaded on import)
_config = None


def get_config() -> dict[str, Any]:
    """Get the loaded configuration."""
    global _config
    if _config is None:
        _config = load_config()
    return _config


# Export configuration constants
def init_config():
    """Initialize configuration constants."""
    global SERPAPI_KEY, GOOGLE_SHEET_ID, GOOGLE_SERVICE_ACCOUNT_JSON
    global MIN_RATING, MIN_REVIEWS, MAX_LEADS_PER_RUN
    
    config = get_config()
    SERPAPI_KEY = config["SERPAPI_KEY"]
    GOOGLE_SHEET_ID = config["GOOGLE_SHEET_ID"]
    GOOGLE_SERVICE_ACCOUNT_JSON = config["GOOGLE_SERVICE_ACCOUNT_JSON"]
    MIN_RATING = config["MIN_RATING"]
    MIN_REVIEWS = config["MIN_REVIEWS"]
    MAX_LEADS_PER_RUN = config["MAX_LEADS_PER_RUN"]
