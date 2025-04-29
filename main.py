#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the 3D model generation application.
This script handles command-line arguments and orchestrates the workflow.
"""

import argparse
import os
import sys
from pathlib import Path

from src.photo_to_3d import photo_to_model
from src.text_to_3d import text_to_model
from utils.file_utils import validate_file, ensure_dir
from config.settings import load_config


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate 3D models from photos or text prompts"
    )
    
    # Create subparsers for different modes
    subparsers = parser.add_subparsers(dest="mode", help="Mode of operation")
    
    # Photo mode parser
    photo_parser = subparsers.add_parser("photo", help="Generate 3D model from photo")
    photo_parser.add_argument("input_path", help="Path to input photo")
    photo_parser.add_argument(
        "-o", "--output", default="models/output.obj", 
        help="Path to output 3D model file (.obj or .stl)"
    )
    photo_parser.add_argument(
        "-r", "--resolution", type=int, default=128,
        help="Resolution of the output 3D model"
    )
    
    # Text mode parser
    text_parser = subparsers.add_parser("text", help="Generate 3D model from text prompt")
    text_parser.add_argument("prompt", help="Text prompt describing the 3D model")
    text_parser.add_argument(
        "-o", "--output", default="models/output.obj",
        help="Path to output 3D model file (.obj or .stl)"
    )
    text_parser.add_argument(
        "-r", "--resolution", type=int, default=128,
        help="Resolution of the output 3D model"
    )
    
    return parser.parse_args()


def main():
    """Main function to run the application."""
    # Load configuration
    config = load_config()
    
    # Parse arguments
    args = parse_arguments()
    
    if not args.mode:
        print("Error: You must specify a mode (photo or text)")
        sys.exit(1)
    
    # Ensure output directory exists
    output_path = Path(args.output)
    ensure_dir(output_path.parent)
    
    if args.mode == "photo":
        # Validate input file
        if not validate_file(args.input_path, [".jpg", ".jpeg", ".png"]):
            print(f"Error: Input file {args.input_path} is not a valid image file")
            sys.exit(1)
        
        # Generate 3D model from photo
        print(f"Generating 3D model from photo: {args.input_path}")
        photo_to_model(
            input_path=args.input_path,
            output_path=args.output,
            resolution=args.resolution,
            config=config
        )
    
    elif args.mode == "text":
        # Generate 3D model from text prompt
        print(f"Generating 3D model from text prompt: {args.prompt}")
        text_to_model(
            prompt=args.prompt,
            output_path=args.output,
            resolution=args.resolution,
            config=config
        )
    
    print(f"3D model generated successfully: {args.output}")


if __name__ == "__main__":
    main()
