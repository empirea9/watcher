# 3D Projectile Motion Simulator - User Guide

## Overview

This is a comprehensive 3D physics simulation application that allows you to launch various objects in a 3D space and observe their trajectories under the influence of gravity. The simulator features a dark, minimalistic aesthetic and provides full control over camera movement and launch parameters.

## Features Checklist

### Visual & Aesthetic ✓
- ✓ Dark minimalistic theme
- ✓ Primary colors: Black, White, Gray
- ✓ Accent colors: Blue (trajectories), Yellow (highlights)
- ✓ No coordinate grid lines cluttering the view
- ✓ Clean UI with information panel

### 3D Environment ✓
- ✓ Fully 3D navigatable space
- ✓ Movable camera with mouse controls
- ✓ Zoom in/out with mouse scroll
- ✓ Pan camera with arrow keys
- ✓ Rotate view by dragging

### Physics Simulation ✓
- ✓ Realistic projectile motion
- ✓ Gravity simulation (9.81 m/s²)
- ✓ Mass-dependent acceleration (F = ma)
- ✓ Real-time trajectory path visualization
- ✓ Continuous physics updates at 60 FPS

### 3D Objects (8 Types) ✓
**Balls:**
- ✓ Football (0.43 kg)
- ✓ Basketball (0.62 kg)
- ✓ Baseball (0.145 kg)

**Cubes:**
- ✓ Small Cube (1.0 kg)
- ✓ Large Cube (5.0 kg)

**Projectiles:**
- ✓ Spear (0.8 kg)
- ✓ Arrow (0.02 kg)
- ✓ Bullet (0.008 kg)

### Launch Controls ✓
- ✓ Adjustable horizontal angle (0-360°)
- ✓ Adjustable vertical angle (-90° to 90°)
- ✓ Adjustable force (1-200 N)
- ✓ Space bar to launch
- ✓ Reset functionality

### UI Information Panel ✓
- ✓ Cursor 3D coordinates (X, Y, Z)
- ✓ Current object name and mass
- ✓ Launch settings display
- ✓ Simulation status
- ✓ Controls reference

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. Clone or download the repository:
```bash
git clone https://github.com/empirea9/watcher.git
cd watcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

This will install:
- pygame (2D/3D graphics library)
- PyOpenGL (OpenGL bindings for Python)
- numpy (numerical computations)

## Running the Simulator

To start the simulator:
```bash
python simulator.py
```

## Controls Reference

### Launch Controls
| Key | Action |
|-----|--------|
| SPACE | Launch object with current settings |
| R | Reset simulation |
| TAB | Switch to next object type |

### Angle & Force Adjustment
| Key | Action |
|-----|--------|
| Q | Increase horizontal angle |
| A | Decrease horizontal angle |
| W | Increase vertical angle |
| S | Decrease vertical angle |
| E | Increase launch force |
| D | Decrease launch force |

### Camera Controls
| Control | Action |
|---------|--------|
| Mouse Drag (Left Click) | Rotate camera view |
| Mouse Scroll Up | Zoom in |
| Mouse Scroll Down | Zoom out |
| Arrow Up | Pan camera forward |
| Arrow Down | Pan camera backward |
| Arrow Left | Pan camera left |
| Arrow Right | Pan camera right |

### System Controls
| Key | Action |
|-----|--------|
| ESC | Exit application |

## How to Use

### Basic Workflow

1. **Start the Application**
   ```bash
   python simulator.py
   ```

2. **Select an Object**
   - Press TAB to cycle through different objects
   - Current object info appears in the right panel

3. **Adjust Launch Parameters**
   - Use Q/A for horizontal angle (direction)
   - Use W/S for vertical angle (trajectory arc)
   - Use E/D for force (launch power)
   - Watch the values update in real-time in the UI panel

4. **Position Your View**
   - Drag with mouse to rotate the camera
   - Scroll to zoom in/out
   - Use arrow keys to pan the view

5. **Launch the Object**
   - Press SPACE to launch
   - Watch the blue trajectory line form
   - Object will fall when it hits the ground (y=0)

6. **Reset and Try Again**
   - Press R to reset the object
   - Adjust parameters
   - Launch again

### Tips for Best Results

1. **Understanding Angles:**
   - Horizontal angle (Q/A): 0° = East, 90° = North, 180° = West, 270° = South
   - Vertical angle (W/S): 0° = horizontal, 45° = optimal distance, 90° = straight up

2. **Force Selection:**
   - Start with 20N for medium-weight objects
   - Use higher forces (50-100N) for heavy cubes
   - Use lower forces (5-15N) for light objects like arrows

3. **Camera Tips:**
   - Start with default view for best perspective
   - Zoom out to see long trajectories
   - Use pan to follow the object

4. **Observing Physics:**
   - Heavier objects fall faster (same initial velocity)
   - All objects accelerate downward at 9.81 m/s²
   - Trajectory paths show the complete flight path

## Understanding the UI

### Right Panel Information

```
Cursor Position:          <- Your mouse position in 3D space
X: 5.23                   <- X coordinate (left-right)
Y: 2.15                   <- Y coordinate (up-down)
Z: -3.44                  <- Z coordinate (forward-back)

Object: Football          <- Currently selected object
Mass: 0.430 kg           <- Object's mass in kilograms

Launch Settings:          <- Current launch parameters
H-Angle: 45.0°           <- Horizontal angle
V-Angle: 45.0°           <- Vertical angle
Force: 20.0 N            <- Launch force in Newtons

Status: READY             <- Simulation state
```

### Visual Elements

- **Ground Grid:** Dark gray grid lines showing the ground plane (y=0)
- **Coordinate Axes:** 
  - Red line: X-axis (East-West)
  - Green line: Y-axis (Up-Down)
  - Blue line: Z-axis (North-South)
- **Blue Trajectory Line:** Path the object has traveled
- **White/Gray Object:** The current object being simulated

## Technical Details

### Physics Engine
- **Gravity:** -9.81 m/s² (Earth standard)
- **Integration Method:** Euler integration
- **Time Step:** Variable (60 FPS target)
- **Force Application:** F = ma (Newton's second law)
- **Trajectory Sampling:** Every 0.1 meters

### Graphics
- **Renderer:** OpenGL 3D
- **Window Size:** 1280x720 pixels
- **Field of View:** 45°
- **Camera Type:** Free-look orbital camera
- **Anti-aliasing:** Enabled via blending

### Objects
All objects have realistic masses and appropriate sizes:
- Spheres for balls and bullets
- Cubes for boxes
- Cylinders for spears and arrows

## Troubleshooting

### Application Won't Start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.8+)
- Verify OpenGL support on your system

### Graphics Issues
- Update graphics drivers
- Try running on a different display
- Check if OpenGL is supported: `python -c "from OpenGL.GL import *"`

### Performance Issues
- Close other applications
- Reduce window size (modify `width` and `height` in code)
- Ensure GPU acceleration is enabled

## Examples & Experiments

### Long Distance Shot
1. Select Football (TAB until you see it)
2. Set H-Angle: 0° (press A until 0)
3. Set V-Angle: 45° (optimal angle)
4. Set Force: 50N (press E multiple times)
5. Press SPACE and watch!

### Vertical Launch
1. Select Basketball
2. Set V-Angle: 90° (straight up)
3. Set Force: 30N
4. Launch and observe the up-down motion

### Comparing Masses
1. Launch a Bullet with 10N force at 45°/45°
2. Press R to reset
3. Press TAB to switch to Large Cube
4. Launch with same 10N force at 45°/45°
5. Compare the trajectories!

### Artillery Simulation
1. Select Spear
2. Position camera from side view
3. Launch at various angles to find optimal range

## Color Scheme Details

The application uses a carefully designed dark theme:

| Element | Color | RGB | Purpose |
|---------|-------|-----|---------|
| Background | Almost Black | (0.05, 0.05, 0.05) | Main background |
| Grid | Dark Gray | (0.2, 0.2, 0.2) | Ground reference |
| Trajectory | Blue | (0.3, 0.6, 1.0) | Path visualization |
| Object | Light Gray | (0.9, 0.9, 0.9) | Main objects |
| UI Background | Dark | (0.1, 0.1, 0.1) | UI panel |
| UI Text | White | (1.0, 1.0, 1.0) | Readable text |
| Highlights | Yellow | (1.0, 0.9, 0.2) | Important info |
| X-Axis | Red | (0.8, 0.2, 0.2) | Coordinate reference |
| Y-Axis | Green | (0.2, 0.8, 0.2) | Coordinate reference |
| Z-Axis | Blue | (0.2, 0.2, 0.8) | Coordinate reference |

## Project Structure

```
watcher/
├── simulator.py              # Main application
├── requirements.txt          # Python dependencies
├── test_physics_logic.py     # Unit tests for physics
├── test_simulator.py         # Integration tests
├── README.md                 # Project overview
├── USER_GUIDE.md            # This file
└── .gitignore               # Git ignore rules
```

## Credits & License

This physics simulator was created as a demonstration of 3D graphics and physics simulation in Python.

Technologies used:
- Pygame: Game development framework
- PyOpenGL: Python bindings for OpenGL
- NumPy: Numerical computing library

## Support & Feedback

For issues, questions, or suggestions:
1. Check this user guide
2. Review the README.md
3. Open an issue on the repository
4. Check the test files for usage examples

Enjoy exploring projectile motion in 3D!
