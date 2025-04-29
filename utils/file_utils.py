#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions for file operations.
"""

import os
import logging
from pathlib import Path

# Set up logging
logger = logging.getLogger(__name__)


def validate_file(file_path, allowed_extensions=None):
    """
    Validate if a file exists and has an allowed extension.
    
    Args:
        file_path (str): Path to the file to validate.
        allowed_extensions (list): List of allowed file extensions.
    
    Returns:
        bool: True if the file is valid, False otherwise.
    """
    if not os.path.isfile(file_path):
        logger.error(f"File not found: {file_path}")
        return False
    
    if allowed_extensions:
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in allowed_extensions:
            logger.error(f"Invalid file extension: {ext}. Allowed: {allowed_extensions}")
            return False
    
    return True


def ensure_dir(directory):
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory (str or Path): Directory path to ensure exists.
    
    Returns:
        bool: True if the directory exists or was created, False otherwise.
    """
    try:
        directory = Path(directory)
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {str(e)}")
        return False


def get_file_size(file_path):
    """
    Get the size of a file in bytes.
    
    Args:
        file_path (str): Path to the file.
    
    Returns:
        int: Size of the file in bytes, or -1 if the file doesn't exist.
    """
    try:
        return os.path.getsize(file_path)
    except (OSError, FileNotFoundError):
        logger.error(f"Error getting file size for {file_path}")
        return -1


def list_files_by_extension(directory, extension):
    """
    List all files in a directory with a specific extension.
    
    Args:
        directory (str): Directory to search in.
        extension (str): File extension to filter by (e.g., '.obj').
    
    Returns:
        list: List of file paths matching the extension.
    """
    try:
        directory = Path(directory)
        return [str(f) for f in directory.glob(f"*{extension}")]
    except Exception as e:
        logger.error(f"Error listing files in {directory}: {str(e)}")
        return []
