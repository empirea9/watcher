# 3D Projectile Motion Simulator

A physics simulation project featuring a 3D navigatable space with projectile motion. Built with a dark, minimalistic aesthetic using black, white, gray, blue, and yellow as primary colors.

## Features

- **3D Navigatable Space**: Fully interactive 3D environment with movable camera
- **Multiple Objects**: Various 3D objects with predefined masses including:
  - Balls: Football, Basketball, Baseball
  - Cubes: Small and Large
  - Projectiles: Spears, Arrows, Bullets
- **Physics Simulation**: Realistic projectile motion with gravity
- **Trajectory Visualization**: Real-time trajectory path display
- **Customizable Launch**: Adjust angle (horizontal and vertical) and force
- **Cursor Tracking**: 3D coordinates displayed in the UI panel
- **Dark Aesthetic Theme**: Minimalistic design with carefully chosen color scheme

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the simulator:
```bash
python simulator.py
```

### Controls

- **SPACE**: Launch the object with current settings
- **R**: Reset the simulation
- **TAB**: Switch to next object type
- **Q/A**: Adjust horizontal angle (+/-)
- **W/S**: Adjust vertical angle (+/-)
- **E/D**: Adjust launch force (+/-)
- **Mouse Drag**: Rotate camera view
- **Mouse Scroll**: Zoom in/out
- **Arrow Keys**: Pan camera target

### UI Information

The right panel displays:
- Current cursor 3D position coordinates
- Selected object name and mass
- Launch settings (angles and force)
- Simulation status
- All available controls

## Technical Details

- **Graphics**: OpenGL via PyOpenGL and Pygame
- **Physics**: Custom physics engine with gravity simulation
- **Camera**: 3D camera with yaw, pitch, and zoom controls
- **Objects**: Different shapes (spheres, cubes, cylinders) with realistic masses 
