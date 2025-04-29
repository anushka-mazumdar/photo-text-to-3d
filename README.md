# 3D Model Generator

A Python application that generates 3D models (.obj or .stl) from photos or text prompts.

## Features

- Generate 3D models from photos using depth estimation
- Generate 3D models from text prompts using procedural generation
- Support for both .obj and .stl output formats
- Configurable resolution and other parameters
- Command-line interface for easy integration into workflows

## Project Structure

```
3D model/
├── config/             # Configuration files
│   ├── __init__.py
│   └── settings.py
├── data/               # Input data and intermediate files
│   └── __init__.py
├── models/             # Output 3D models
│   └── __init__.py
├── src/                # Source code
│   ├── __init__.py
│   ├── photo_to_3d.py  # Photo to 3D model conversion
│   └── text_to_3d.py   # Text to 3D model conversion
├── tests/              # Test cases
│   ├── __init__.py
│   └── test_file_utils.py
├── utils/              # Utility functions
│   ├── __init__.py
│   └── file_utils.py
├── venv/               # Virtual environment (not tracked in git)
├── main.py             # Main entry point
├── README.md           # Project documentation
├── requirements.txt    # Dependencies
└── run.ipynb           # Jupyter notebook for interactive use
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/3d-model-generator.git
   cd 3d-model-generator
   ```

2. Create and activate a virtual environment:
   ```
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

Generate a 3D model from a photo:

```
python main.py photo path/to/image.jpg -o models/output.obj -r 256
```

Generate a 3D model from a text prompt:

```
python main.py text "A mountain landscape" -o models/mountain.obj -r 256
```

### Options

- `-o, --output`: Path to output 3D model file (.obj or .stl)
- `-r, --resolution`: Resolution of the output 3D model (default: 128)

## Advanced Usage

For more advanced usage, you can modify the configuration file at `config/config.json`. This file is automatically created with default values when you first run the application.

### Configuration Options

- `photo_to_3d`: Settings for photo to 3D model conversion
  - `depth_estimation_method`: Method for estimating depth from photos (simple, neural)
  - `smoothing`: Whether to apply smoothing to the generated model
  - `smoothing_factor`: Strength of the smoothing effect

- `text_to_3d`: Settings for text to 3D model conversion
  - `model_type`: Type of model to use (procedural, neural)
  - `complexity`: Complexity of the generated model (low, medium, high)

- `output`: Settings for output files
  - `default_format`: Default output format (obj, stl)
  - `compress_output`: Whether to compress output files

## Development

### Running Tests

```
pytest tests/
```

### Adding New Features

1. Implement new functionality in the appropriate module
2. Add tests for the new functionality
3. Update the documentation

## Dependencies

- numpy: Numerical computing
- Pillow: Image processing
- trimesh: 3D mesh processing
- scipy: Scientific computing
- opencv-python: Computer vision algorithms
- pytest: Testing framework

## Future Improvements

- Implement neural network-based depth estimation for better 3D models from photos
- Add support for text-to-3D using advanced AI models like DreamFusion or Shap-E
- Implement a web interface for easier use
- Add support for more output formats (glTF, PLY, etc.)
- Improve texture mapping for more realistic models

## License

MIT License
