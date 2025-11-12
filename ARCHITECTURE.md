# Project Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  3D Projectile Motion Simulator              │
│                                                              │
│  ┌────────────────┐        ┌───────────────────┐           │
│  │  User Input    │───────▶│  Physics Engine   │           │
│  │  - Keyboard    │        │  - Gravity        │           │
│  │  - Mouse       │        │  - Trajectory     │           │
│  └────────────────┘        │  - Collisions     │           │
│         │                  └───────────────────┘           │
│         │                           │                       │
│         ▼                           ▼                       │
│  ┌────────────────┐        ┌───────────────────┐           │
│  │  Camera System │◀──────▶│  3D Scene         │           │
│  │  - Position    │        │  - Objects        │           │
│  │  - Rotation    │        │  - Grid           │           │
│  │  - Zoom        │        │  - Axes           │           │
│  └────────────────┘        │  - Trajectory     │           │
│         │                  └───────────────────┘           │
│         │                           │                       │
│         └───────────┬───────────────┘                       │
│                     ▼                                       │
│            ┌─────────────────┐                             │
│            │  OpenGL Renderer │                             │
│            └─────────────────┘                             │
│                     │                                       │
│                     ▼                                       │
│            ┌─────────────────┐                             │
│            │   UI Overlay     │                             │
│            │  - Coordinates   │                             │
│            │  - Object Info   │                             │
│            │  - Controls      │                             │
│            └─────────────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

## Class Hierarchy

```
PhysicsSimulator (Main Application)
│
├─── Camera
│    ├── position: Vector3
│    ├── target: Vector3
│    ├── yaw: float
│    ├── pitch: float
│    └── distance: float
│
├─── Object3D (Multiple Instances)
│    ├── mass: float
│    ├── size: float
│    ├── shape: string
│    ├── position: Vector3
│    ├── velocity: Vector3
│    ├── rotation: Vector3
│    └── trajectory: List[Vector3]
│
└─── UI System
     ├── draw_grid()
     ├── draw_axes()
     ├── draw_ui()
     └── draw_ui_text()
```

## Coordinate System

```
        Y (Up)
        │
        │
        │
        └──────────── X (East)
       ╱
      ╱
     ╱
    Z (North)

Grid plane is at Y = 0 (ground level)
Objects start at Y = 2
Objects stop when Y < 0
```

## Data Flow

```
Input Event
    │
    ▼
┌──────────────┐
│ Event Handler│
└──────────────┘
    │
    ├─── Keyboard ──▶ Launch Parameters (angle, force)
    │                 Object Selection (TAB)
    │                 Launch (SPACE)
    │                 Reset (R)
    │
    └─── Mouse ────▶ Camera Rotation (drag)
                     Camera Zoom (scroll)
    │
    ▼
┌──────────────┐
│ Physics Loop │ (60 FPS)
└──────────────┘
    │
    ├─── If Simulating:
    │    └─── Update velocity (apply gravity)
    │         Update position (integrate)
    │         Record trajectory
    │         Check ground collision
    │
    └─── Update camera position
    │
    ▼
┌──────────────┐
│ Render Loop  │
└──────────────┘
    │
    ├─── Clear buffers
    ├─── Apply camera transform
    ├─── Draw grid
    ├─── Draw axes
    ├─── Draw object
    ├─── Draw trajectory
    ├─── Draw UI overlay
    └─── Swap buffers
```

## Object State Machine

```
┌─────────┐
│  READY  │ ◀──────────────┐
└─────────┘                 │
    │                       │
    │ SPACE pressed         │ R pressed or
    │                       │ hit ground
    ▼                       │
┌─────────┐                 │
│SIMULATING│ ───────────────┘
└─────────┘
    │
    │ Physics update each frame:
    │ 1. Apply gravity: v.y += g * dt
    │ 2. Update position: pos += v * dt
    │ 3. Record trajectory point
    │ 4. Check if pos.y < 0 (ground)
    │
    └─── Loop until ground hit
```

## Physics Formulas

### Force to Velocity Conversion
```
Given: Force F, Mass m, Angles (horizontal θ, vertical φ)

Velocity components:
vx = (F/m) × cos(φ) × cos(θ)
vy = (F/m) × sin(φ)
vz = (F/m) × cos(φ) × sin(θ)
```

### Gravity Integration
```
Each timestep dt:
vy = vy + g × dt    (where g = -9.81 m/s²)
position = position + velocity × dt
```

### Camera Position
```
Given: Target position, yaw α, pitch β, distance d

Camera position:
x = target.x + d × cos(β) × cos(α)
y = target.y + d × sin(β)
z = target.z + d × cos(β) × sin(α)
```

## File Structure Details

### simulator.py (Main Application)
```python
# Constants
COLORS = {...}                    # Color scheme

# Classes
class Object3D:                   # Physics object
    OBJECTS = {...}               # Object definitions
    def __init__(...)
    def reset(...)
    def apply_force(...)
    def update(...)               # Physics step
    def draw(...)                 # Render object
    def draw_trajectory(...)      # Render path

class Camera:                     # 3D camera
    def __init__(...)
    def update_position(...)
    def apply(...)                # Set view matrix
    def rotate(...)
    def zoom(...)
    def pan(...)

class PhysicsSimulator:          # Main app
    def __init__(...)
    def draw_grid(...)
    def draw_axes(...)
    def draw_ui(...)
    def draw_ui_text(...)
    def handle_input(...)
    def run(...)                  # Main loop

def main():                       # Entry point
```

### Color Palette
```
Background:    RGB(13, 13, 13)    # Very dark gray
Grid:          RGB(51, 51, 51)    # Dark gray
Trajectory:    RGB(77, 153, 255)  # Blue
Object:        RGB(230, 230, 230) # Light gray
Text:          RGB(255, 255, 255) # White
Highlight:     RGB(255, 230, 51)  # Yellow
```

## Performance Characteristics

```
Target Frame Rate: 60 FPS
Physics Updates:   60 Hz
Trajectory Points: ~10 per second of flight
Max Objects:       1 (current design)
Memory Usage:      ~50 MB
CPU Usage:         ~5-10% (single core)
GPU Usage:         Minimal (simple geometry)
```

## Extension Points

Future enhancements could include:

1. **Multiple simultaneous objects**
   - Track array of Object3D instances
   - Render all in draw loop

2. **Air resistance**
   - Add drag force: F_drag = -k × v²
   - Update physics in Object3D.update()

3. **Collision detection**
   - Check distance between objects
   - Apply collision response

4. **Save/Load trajectories**
   - Export trajectory data to file
   - Replay saved simulations

5. **Different environments**
   - Moon gravity: -1.62 m/s²
   - Mars gravity: -3.71 m/s²
   - Custom gravity setting

6. **Better graphics**
   - Shadows
   - Textures
   - Lighting effects
   - Particle effects on launch

## Testing Strategy

```
Unit Tests (test_physics_logic.py)
├── Color scheme validation
├── Object type verification
├── Object initialization
├── Object reset
├── Force application
├── Physics simulation
├── Mass differences
├── Camera controls
├── Angle configurations
└── Trajectory tracking

Integration Tests (test_simulator.py)
├── Module imports
├── Class instantiation
├── Method functionality
└── Error handling
```
