#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for converting text prompts to 3D models.
"""

import os
import numpy as np
import trimesh
import logging
import hashlib
import re

# Set up logging
logger = logging.getLogger(__name__)


def text_to_model(prompt, output_path, resolution=128, config=None):
    """
    Convert a text prompt to a 3D model.
    
    Args:
        prompt (str): Text prompt describing the 3D model.
        output_path (str): Path to save the output 3D model.
        resolution (int): Resolution of the output 3D model.
        config (dict): Configuration parameters.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        logger.info(f"Processing text prompt: {prompt}")
        
        # In a real implementation, this would use a text-to-3D model like:
        # - DreamFusion
        # - Point-E
        # - Shap-E
        # - Text2Mesh
        # - GET3D
        # or similar models
        
        # For this example, we'll create a simple procedural shape based on the prompt
        # This is just a placeholder for demonstration purposes
        
        # Use the prompt to seed a random generator
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
        seed = int(prompt_hash, 16) % (2**32)
        np.random.seed(seed)
        
        # Simple shape generation based on keywords in the prompt
        prompt_lower = prompt.lower()
        
        # Determine shape type based on keywords
        if any(word in prompt_lower for word in ['sphere', 'ball', 'round']):
            mesh = create_sphere(resolution)
        elif any(word in prompt_lower for word in ['cube', 'box', 'square']):
            mesh = create_cube(resolution)
        elif any(word in prompt_lower for word in ['cylinder', 'tube']):
            mesh = create_cylinder(resolution)
        elif any(word in prompt_lower for word in ['cone', 'pyramid']):
            mesh = create_cone(resolution)
        else:
            # Default to a simple terrain-like surface
            mesh = create_terrain(resolution, prompt)
        
        # Determine the output format
        if output_path.lower().endswith('.stl'):
            mesh.export(output_path, file_type='stl')
        else:  # Default to OBJ
            mesh.export(output_path, file_type='obj')
        
        logger.info(f"3D model saved to: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error converting text to 3D model: {str(e)}")
        return False


def create_sphere(resolution):
    """Create a sphere mesh."""
    # Create a UV sphere
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    
    # Create vertices
    vertices = []
    for i in range(resolution):
        for j in range(resolution):
            x = 0.5 * np.sin(v[j]) * np.cos(u[i])
            y = 0.5 * np.sin(v[j]) * np.sin(u[i])
            z = 0.5 * np.cos(v[j])
            vertices.append([x, y, z])
    
    vertices = np.array(vertices)
    
    # Create faces
    faces = []
    for i in range(resolution-1):
        for j in range(resolution-1):
            v0 = i * resolution + j
            v1 = i * resolution + j + 1
            v2 = (i + 1) * resolution + j
            v3 = (i + 1) * resolution + j + 1
            
            # Add two triangles for each grid cell
            faces.append([v0, v1, v2])
            faces.append([v1, v3, v2])
    
    faces = np.array(faces)
    
    # Create a mesh
    return trimesh.Trimesh(vertices=vertices, faces=faces)


def create_cube(resolution):
    """Create a cube mesh."""
    # Create a cube with subdivision
    mesh = trimesh.creation.box(extents=[1, 1, 1])
    
    # Subdivide the mesh to increase resolution
    for _ in range(int(np.log2(resolution/12))):
        mesh = mesh.subdivide()
    
    return mesh


def create_cylinder(resolution):
    """Create a cylinder mesh."""
    # Create a cylinder
    return trimesh.creation.cylinder(
        radius=0.5, 
        height=1.0, 
        sections=resolution
    )


def create_cone(resolution):
    """Create a cone mesh."""
    # Create a cone
    return trimesh.creation.cone(
        radius=0.5, 
        height=1.0, 
        sections=resolution
    )


def create_terrain(resolution, prompt):
    """Create a terrain-like mesh based on the prompt."""
    # Create a grid of vertices
    x = np.linspace(-0.5, 0.5, resolution)
    y = np.linspace(-0.5, 0.5, resolution)
    xv, yv = np.meshgrid(x, y)
    
    # Use the prompt to generate terrain features
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    
    # Extract numbers from the hash to use as parameters
    params = [int(prompt_hash[i:i+2], 16) / 255.0 for i in range(0, 32, 2)]
    
    # Create height map using perlin-like noise
    z = np.zeros((resolution, resolution))
    for i, param in enumerate(params[:8]):
        freq = 1 + i * 2
        z += param * np.sin(freq * xv) * np.cos(freq * yv) / freq
    
    # Normalize height
    z = (z - z.min()) / (z.max() - z.min()) * 0.5
    
    # Create vertices
    vertices = np.zeros((resolution * resolution, 3))
    vertices[:, 0] = xv.flatten()
    vertices[:, 1] = yv.flatten()
    vertices[:, 2] = z.flatten()
    
    # Create faces
    faces = []
    for i in range(resolution-1):
        for j in range(resolution-1):
            v0 = i * resolution + j
            v1 = i * resolution + j + 1
            v2 = (i + 1) * resolution + j
            v3 = (i + 1) * resolution + j + 1
            
            # Add two triangles for each grid cell
            faces.append([v0, v1, v2])
            faces.append([v1, v3, v2])
    
    faces = np.array(faces)
    
    # Create a mesh
    return trimesh.Trimesh(vertices=vertices, faces=faces)
