# Changelog - Enhanced 3D Projectile Motion Simulator

## Version 2.0 - Major Update

### New Features

#### 1. Object Dragging
- **Right-click drag**: Can now drag objects to any position in 3D space
- Objects turn yellow when being dragged
- Drag functionality disabled during simulation
- Position updates in real-time

#### 2. GUI Controls (replaced keyboard controls)
- **Object Selection**: Dropdown menu to select from 8 objects
- **Angle Inputs**: Text entry fields for horizontal (0-360°) and vertical (-90 to 90°) angles
- **Force Input**: Text entry field for launch force (1-200 N)
- **Camera Speed Slider**: Adjustable camera movement speed (0.1-2.0x)
- **Launch Button**: GUI button to launch projectile
- **Reset Button**: GUI button to reset simulation
- **Info Panel**: Instructions for controls

#### 3. Fixed Arrow Key Panning
- **UP Arrow**: Move forward (in camera direction)
- **DOWN Arrow**: Move backward  
- **LEFT Arrow**: Move left (perpendicular to camera)
- **RIGHT Arrow**: Move right (perpendicular to camera)
- Panning now follows camera orientation correctly

#### 4. Infinite Grid
- Grid now extends infinitely in all directions
- Dynamically generates based on camera position
- Grid follows camera movement seamlessly
- Extended far clipping plane (500 units)
- Grid size: 100 units from camera center

#### 5. Enhanced Camera Speed
- Default speed increased from 0.1 to 0.3
- Adjustable via slider (0.1 to 2.0x)
- Real-time speed adjustment
- Smoother, faster navigation

### Technical Changes

#### Dependencies
- Added `pygame-gui==0.6.9` for GUI controls
- Updated requirements.txt

#### Code Structure
- Refactored mouse handling for object dragging vs camera rotation
- Improved 3D position calculation from mouse coordinates
- Added `is_being_dragged` state to Object3D
- Enhanced Camera.pan() to use proper forward/right vectors
- Implemented dynamic grid generation in draw_infinite_grid()

#### UI Improvements
- Larger window size (1400x800)
- GUI panel on right side (300px width)
- Professional control layout
- Real-time input validation
- Color-coded object state (yellow when dragging)

### Controls Summary

**Mouse:**
- Left Click + Drag: Rotate camera view
- Right Click + Drag: Move object position (when not simulating)
- Scroll Wheel: Zoom in/out

**Keyboard:**
- Arrow Keys: Pan camera (UP=forward, DOWN=back, LEFT=left, RIGHT=right)
- ESC: Exit application

**GUI:**
- Select object from dropdown
- Enter angle and force values
- Click LAUNCH to fire
- Click RESET to restart
- Adjust camera speed with slider

### Bug Fixes
- Fixed arrow key panning to move in correct directions
- Fixed camera pan to respect camera orientation
- Improved object selection detection
- Better 3D-to-2D projection for dragging

### Performance
- Optimized grid rendering for infinite extent
- Maintained 60 FPS target
- Efficient GUI rendering

---

**All original features preserved:**
- 8 different objects with realistic masses
- Physics simulation with gravity
- Trajectory visualization
- Dark minimalistic aesthetic
- All tests passing (10/10)
