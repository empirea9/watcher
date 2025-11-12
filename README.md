# 3D Projectile Motion Simulator

A physics simulation project featuring a 3D navigatable space with projectile motion. Built with a dark, minimalistic aesthetic using black, white, gray, blue, and yellow as primary colors.

**🎉 NEW in Version 2.0:** Object dragging, GUI controls, infinite grid, and enhanced camera!

## Features

- **3D Navigatable Space**: Fully interactive 3D environment with movable camera
- **Object Dragging**: Right-click to drag objects anywhere in 3D space ✨ NEW
- **GUI Controls**: Professional UI with dropdowns, text inputs, and sliders ✨ NEW
- **Infinite Grid**: Dynamically generated grid that extends infinitely ✨ NEW
- **Enhanced Camera**: Adjustable speed (0.1-2.0x) with fixed arrow key panning ✨ NEW
- **Multiple Objects**: Various 3D objects with predefined masses including:
  - Balls: Football, Basketball, Baseball
  - Cubes: Small and Large
  - Projectiles: Spears, Arrows, Bullets
- **Physics Simulation**: Realistic projectile motion with gravity
- **Trajectory Visualization**: Real-time trajectory path display
- **Customizable Launch**: Adjust angle (horizontal and vertical) and force via GUI
- **Dark Aesthetic Theme**: Minimalistic design with carefully chosen color scheme

## Quick Start

### Installation

**IMPORTANT:** Version 2.0 requires pygame-gui. Make sure to install ALL dependencies!

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pygame==2.5.2 PyOpenGL==3.1.7 numpy==1.26.3 pygame-gui==0.6.9
```

### Run the Simulator

**Option 1: Using quick start script** (recommended - auto-checks dependencies)
```bash
python start.py
```

**Option 2: Direct run**
```bash
python simulator.py
```

## Controls

### Mouse
- **Left Click + Drag**: Rotate camera view
- **Right Click + Drag**: Move object to any position ✨ NEW
- **Scroll Wheel**: Zoom in/out

### Keyboard
- **Arrow Keys**: Pan camera (UP=forward, DOWN=back, LEFT=left, RIGHT=right) ✨ FIXED
- **ESC**: Exit application

### GUI Controls ✨ NEW
- **Object Dropdown**: Select from 8 different objects
- **Angle Inputs**: Enter horizontal (0-360°) and vertical (-90 to 90°) angles
- **Force Input**: Enter launch force (1-200 N)
- **Camera Speed Slider**: Adjust camera movement speed
- **LAUNCH Button**: Fire the projectile
- **RESET Button**: Reset simulation

## Documentation

- **[CHANGELOG.md](CHANGELOG.md)** - Version 2.0 changes and improvements ✨ NEW
- **[USER_GUIDE.md](USER_GUIDE.md)** - Comprehensive user manual with examples
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture and design details
- **[FEATURES.md](FEATURES.md)** - Complete features showcase
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solutions to common issues

## Project Structure

```
watcher/
├── simulator.py              # Main application (581 lines)
├── start.py                  # Quick start script (95 lines)
├── test_physics_logic.py     # Unit tests (231 lines)
├── test_simulator.py         # Integration tests (146 lines)
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── USER_GUIDE.md            # User manual (324 lines)
├── ARCHITECTURE.md          # Technical docs (295 lines)
├── FEATURES.md              # Features list (279 lines)
└── TROUBLESHOOTING.md       # Troubleshooting guide (359 lines)
```

## Technical Details

- **Graphics**: OpenGL via PyOpenGL and Pygame
- **Physics**: Custom physics engine with gravity simulation
- **Camera**: 3D camera with yaw, pitch, and zoom controls
- **Objects**: Different shapes (spheres, cubes, cylinders) with realistic masses
- **Testing**: 10 unit tests, all passing

## Requirements

- Python 3.8+
- pygame 2.5.2
- PyOpenGL 3.1.7
- numpy 1.26.3
- pygame-gui 0.6.9 ✨ NEW

## Testing

Run the unit tests:
```bash
python test_physics_logic.py
```

All tests should pass:
- ✓ Color scheme validation
- ✓ Object types verification
- ✓ Physics simulation
- ✓ Camera controls
- ✓ Trajectory tracking

## UI Information

The right panel displays:
- Current cursor 3D position coordinates (X, Y, Z)
- Selected object name and mass
- Launch settings (angles and force)
- Simulation status
- All available controls

## Color Scheme

The application uses a carefully designed dark theme:
- **Background**: Almost black (RGB: 13, 13, 13)
- **Grid**: Dark gray (RGB: 51, 51, 51)
- **Trajectory**: Blue (RGB: 77, 153, 255)
- **Objects**: Light gray (RGB: 230, 230, 230)
- **Text**: White (RGB: 255, 255, 255)
- **Highlights**: Yellow (RGB: 255, 230, 51)

## Development

**Code Quality:**
- Clean, readable code structure
- Well-documented functions
- Modular class design
- Comprehensive comments
- Security scanned (0 vulnerabilities)

**Total Project:**
- ~2,400 lines of code and documentation
- 8 different 3D objects
- 10 passing unit tests
- 5 documentation files

## License

This physics simulator was created as a demonstration of 3D graphics and physics simulation in Python.

## Getting Help

1. Check [USER_GUIDE.md](USER_GUIDE.md) for detailed usage instructions
2. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
3. Review [FEATURES.md](FEATURES.md) for complete feature list
4. Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details 
