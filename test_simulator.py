"""
Test script for physics simulator
"""

import sys
import os

# Test imports
print("Testing imports...")
try:
    import pygame
    print("✓ pygame imported successfully")
except ImportError as e:
    print(f"✗ pygame import failed: {e}")
    sys.exit(1)

try:
    import numpy as np
    print("✓ numpy imported successfully")
except ImportError as e:
    print(f"✗ numpy import failed: {e}")
    sys.exit(1)

# Try OpenGL import (may fail in headless environment)
try:
    # Set environment variable for headless mode
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    from OpenGL.GL import *
    from OpenGL.GLU import *
    print("✓ PyOpenGL imported successfully")
    opengl_available = True
except Exception as e:
    print(f"⚠ PyOpenGL not available in this environment (expected in headless mode): {type(e).__name__}")
    opengl_available = False

# Test basic simulator module structure
print("\nTesting simulator module structure...")
try:
    # Import without initializing OpenGL context
    import simulator
    print("✓ simulator module imported successfully")
except Exception as e:
    print(f"✗ simulator module import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test Object3D class (doesn't require OpenGL context)
print("\nTesting Object3D class...")
try:
    obj = simulator.Object3D('football')
    assert obj.name == 'Football'
    assert obj.mass == 0.43
    assert obj.size == 0.11
    assert obj.shape == 'sphere'
    print(f"✓ Object3D class works - Created {obj.name} with mass {obj.mass}kg")
    
    # Test reset
    obj.reset([1, 2, 3])
    assert obj.position[0] == 1.0
    assert obj.position[1] == 2.0
    assert obj.position[2] == 3.0
    print(f"✓ Object reset works")
    
    # Test force application
    obj.apply_force(10.0, 45.0, 30.0)
    assert obj.velocity[0] != 0
    print(f"✓ Force application works")
    
except Exception as e:
    print(f"✗ Object3D test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test Camera class
try:
    camera = simulator.Camera()
    assert camera.distance == 15.0
    print(f"✓ Camera class works - Initial distance: {camera.distance}")
    
    # Test camera controls
    camera.zoom(5)
    assert camera.distance == 20.0
    print(f"✓ Camera zoom works")
    
    camera.rotate(10, 5)
    print(f"✓ Camera rotation works")
    
except Exception as e:
    print(f"✗ Camera test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test object types
print("\nTesting object types...")
object_types = list(simulator.Object3D.OBJECTS.keys())
print(f"Available objects ({len(object_types)}):")
for obj_type in object_types:
    obj = simulator.Object3D(obj_type)
    print(f"  - {obj.name}: {obj.mass}kg, size: {obj.size}m, shape: {obj.shape}")

# Test physics update
print("\nTesting physics simulation...")
try:
    obj = simulator.Object3D('baseball')
    obj.reset([0, 10, 0])
    obj.apply_force(5.0, 45.0, 45.0)
    
    # Simulate for a few steps
    for i in range(10):
        still_moving = obj.update(0.1)
        
    assert len(obj.trajectory) > 1
    assert obj.position[1] < 10  # Should have fallen due to gravity
    print(f"✓ Physics simulation works - trajectory has {len(obj.trajectory)} points")
    
except Exception as e:
    print(f"✗ Physics simulation test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test color scheme
print("\nTesting color scheme...")
try:
    colors = simulator.COLORS
    assert 'background' in colors
    assert 'trajectory' in colors
    assert 'highlight' in colors
    # Verify dark aesthetic
    bg = colors['background']
    assert all(c <= 0.1 for c in bg), "Background should be very dark"
    print(f"✓ Color scheme defined correctly (dark aesthetic)")
except Exception as e:
    print(f"✗ Color scheme test failed: {e}")
    sys.exit(1)

print("\n✓ All logic tests passed!")
if not opengl_available:
    print("\nNote: OpenGL context could not be created (headless environment).")
    print("The graphical interface requires a display to run.")
else:
    print("\nNote: OpenGL is available. The simulator should work with a display.")

