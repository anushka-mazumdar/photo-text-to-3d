#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration settings for the 3D model generation application.
"""

import os
import json
import logging
from pathlib import Path

# Set up logging
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/app.log"
    },
    "photo_to_3d": {
        "default_resolution": 128,
        "max_resolution": 512,
        "depth_estimation_method": "simple",  # Options: simple, neural
        "smoothing": True,
        "smoothing_factor": 0.5
    },
    "text_to_3d": {
        "default_resolution": 128,
        "max_resolution": 512,
        "model_type": "procedural",  # Options: procedural, neural
        "complexity": "medium"  # Options: low, medium, high
    },
    "output": {
        "default_format": "obj",  # Options: obj, stl
        "default_directory": "models",
        "auto_clean": False,  # Whether to clean up temporary files
        "compress_output": False  # Whether to compress output files
    }
}

# Path to the user configuration file
CONFIG_FILE = Path("config/config.json")


def load_config():
    """
    Load configuration from the config file, or create a default one if it doesn't exist.
    
    Returns:
        dict: Configuration dictionary.
    """
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                logger.info(f"Loaded configuration from {CONFIG_FILE}")
                
                # Merge with default config to ensure all keys exist
                config = DEFAULT_CONFIG.copy()
                update_nested_dict(config, user_config)
                return config
        else:
            # Create default config file
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
                logger.info(f"Created default configuration at {CONFIG_FILE}")
            return DEFAULT_CONFIG.copy()
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        return DEFAULT_CONFIG.copy()


def update_nested_dict(d, u):
    """
    Update a nested dictionary with another dictionary.
    
    Args:
        d (dict): Dictionary to update.
        u (dict): Dictionary with updates.
    
    Returns:
        dict: Updated dictionary.
    """
    for k, v in u.items():
        if isinstance(v, dict) and k in d and isinstance(d[k], dict):
            update_nested_dict(d[k], v)
        else:
            d[k] = v
    return d


def save_config(config):
    """
    Save configuration to the config file.
    
    Args:
        config (dict): Configuration dictionary.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
            logger.info(f"Saved configuration to {CONFIG_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error saving configuration: {str(e)}")
        return False


def setup_logging(config=None):
    """
    Set up logging based on configuration.
    
    Args:
        config (dict): Configuration dictionary.
    """
    if config is None:
        config = load_config()
    
    log_config = config.get("logging", DEFAULT_CONFIG["logging"])
    
    # Create logs directory if it doesn't exist
    log_file = Path(log_config.get("file", "logs/app.log"))
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_config.get("level", "INFO")),
        format=log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
