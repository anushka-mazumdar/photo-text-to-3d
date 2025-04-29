#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the file_utils module.
"""

import os
import unittest
import tempfile
from pathlib import Path

from utils.file_utils import validate_file, ensure_dir, get_file_size, list_files_by_extension


class TestFileUtils(unittest.TestCase):
    """Test cases for file_utils module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
        
        # Create a test file
        self.test_file = self.test_dir / "test.txt"
        with open(self.test_file, "w") as f:
            f.write("Test content")
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up the temporary directory
        self.temp_dir.cleanup()
    
    def test_validate_file(self):
        """Test validate_file function."""
        # Test with existing file
        self.assertTrue(validate_file(self.test_file))
        
        # Test with non-existent file
        non_existent_file = self.test_dir / "non_existent.txt"
        self.assertFalse(validate_file(non_existent_file))
        
        # Test with allowed extensions
        self.assertTrue(validate_file(self.test_file, [".txt"]))
        self.assertFalse(validate_file(self.test_file, [".jpg", ".png"]))
    
    def test_ensure_dir(self):
        """Test ensure_dir function."""
        # Test with existing directory
        self.assertTrue(ensure_dir(self.test_dir))
        
        # Test with new directory
        new_dir = self.test_dir / "new_dir"
        self.assertTrue(ensure_dir(new_dir))
        self.assertTrue(new_dir.exists())
        
        # Test with nested directory
        nested_dir = self.test_dir / "nested" / "dir"
        self.assertTrue(ensure_dir(nested_dir))
        self.assertTrue(nested_dir.exists())
    
    def test_get_file_size(self):
        """Test get_file_size function."""
        # Test with existing file
        self.assertEqual(get_file_size(self.test_file), len("Test content"))
        
        # Test with non-existent file
        non_existent_file = self.test_dir / "non_existent.txt"
        self.assertEqual(get_file_size(non_existent_file), -1)
    
    def test_list_files_by_extension(self):
        """Test list_files_by_extension function."""
        # Create test files with different extensions
        txt_file1 = self.test_dir / "file1.txt"
        txt_file2 = self.test_dir / "file2.txt"
        jpg_file = self.test_dir / "image.jpg"
        
        for file_path in [txt_file1, txt_file2, jpg_file]:
            with open(file_path, "w") as f:
                f.write("Test content")
        
        # Test listing .txt files
        txt_files = list_files_by_extension(self.test_dir, ".txt")
        self.assertEqual(len(txt_files), 3)  # Including the test.txt from setUp
        
        # Test listing .jpg files
        jpg_files = list_files_by_extension(self.test_dir, ".jpg")
        self.assertEqual(len(jpg_files), 1)
        
        # Test listing .png files (none should exist)
        png_files = list_files_by_extension(self.test_dir, ".png")
        self.assertEqual(len(png_files), 0)


if __name__ == "__main__":
    unittest.main()
