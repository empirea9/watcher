# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### 1. "pip: command not found"
**Problem:** pip is not installed or not in PATH

**Solution:**
```bash
# On Ubuntu/Debian
sudo apt-get install python3-pip

# On macOS
python3 -m ensurepip

# On Windows
python -m ensurepip
```

#### 2. "PyOpenGL installation fails"
**Problem:** PyOpenGL or PyOpenGL_accelerate won't compile

**Solution:**
The requirements.txt already excludes PyOpenGL_accelerate which is optional. If PyOpenGL itself fails:
```bash
# Try installing with --upgrade
pip install --upgrade PyOpenGL

# Or try a different version
pip install PyOpenGL==3.1.6
```

#### 3. "Permission denied" errors
**Problem:** Don't have permission to install packages

**Solution:**
```bash
# Install for current user only
pip install --user -r requirements.txt

# Or use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### Runtime Issues

#### 4. "AttributeError: 'NoneType' object has no attribute 'glGetError'"
**Problem:** Running in headless environment (no display)

**Solution:**
This application requires a graphical display. Solutions:
- Run on a machine with a display
- Use X11 forwarding if on remote server
- For testing without display, use `test_physics_logic.py` which tests logic only

```bash
# Test without graphics
python test_physics_logic.py
```

#### 5. "pygame.error: No available video device"
**Problem:** No display available or SDL not configured

**Solution:**
```bash
# On Linux, ensure X11 is running
echo $DISPLAY  # Should show :0 or similar

# Try setting SDL video driver explicitly
SDL_VIDEODRIVER=x11 python simulator.py

# On headless server, won't work without virtual display
```

#### 6. Black screen or window doesn't appear
**Problem:** OpenGL context creation failed

**Solution:**
- Update graphics drivers
- Check OpenGL support: `glxinfo | grep "OpenGL version"`
- Try running with different renderer:
```bash
# Force software rendering (slower but more compatible)
LIBGL_ALWAYS_SOFTWARE=1 python simulator.py
```

---

### Performance Issues

#### 7. Low frame rate / laggy
**Problem:** Performance issues

**Solution:**
- Close other applications
- Update graphics drivers
- Check system resources: `top` or Task Manager
- Reduce grid size in code:
```python
# In simulator.py, change:
self.draw_grid(size=10, spacing=2)  # Smaller grid
```

#### 8. Application freezes
**Problem:** Application becomes unresponsive

**Solution:**
- Press ESC to exit
- If that doesn't work, force close:
```bash
# On Linux/Mac
pkill -9 python

# On Windows
taskkill /F /IM python.exe
```

---

### Control Issues

#### 9. Camera won't move
**Problem:** Camera controls not responding

**Solution:**
- Ensure window has focus (click on it)
- Check if keys are working:
  - Mouse drag should rotate
  - Scroll should zoom
  - Arrow keys should pan
- Restart application if controls stop working

#### 10. Can't switch objects
**Problem:** TAB key doesn't change object

**Solution:**
- Only works when simulation is not running (Status: READY)
- Press R to reset first
- Then press TAB

#### 11. Object won't launch
**Problem:** SPACE doesn't launch

**Solution:**
- Check if already simulating (can't launch twice)
- Press R to reset
- Ensure window has focus
- Check Status display (should be READY)

---

### Visual Issues

#### 12. Colors look wrong
**Problem:** Colors don't match description

**Solution:**
- Check monitor color calibration
- Ensure color depth is 24-bit or higher
- Try adjusting monitor brightness

#### 13. Trajectory not visible
**Problem:** Can't see blue trajectory line

**Solution:**
- Launch object first (press SPACE)
- Line appears as object moves
- Try different camera angle
- Increase trajectory line width in code:
```python
# In Object3D.draw_trajectory()
glLineWidth(4.0)  # Thicker line
```

#### 14. Text hard to read
**Problem:** UI text is unclear

**Solution:**
- Adjust font size in code:
```python
# In PhysicsSimulator.__init__()
self.font = pygame.font.Font(None, 36)  # Larger font
```

---

### Physics Issues

#### 15. Object moves too fast/slow
**Problem:** Unrealistic speeds

**Solution:**
- Adjust force with E/D keys
- Remember: Force / Mass = Acceleration
- Light objects (bullet, arrow) accelerate more with same force
- Heavy objects (large cube) need more force

#### 16. Trajectory seems wrong
**Problem:** Path doesn't look realistic

**Solution:**
- This is correct physics! Real projectile motion includes:
  - Parabolic arc
  - Gravity pulling down
  - Different masses don't affect trajectory shape with same initial velocity
- Compare with physics equations to verify

#### 17. Object falls through ground
**Problem:** Object goes below y=0

**Solution:**
- This is by design to stop simulation
- Object stops simulating when y < 0
- Press R to reset

---

### Testing Issues

#### 18. Tests fail in headless environment
**Problem:** test_simulator.py fails without display

**Solution:**
Use the logic-only test instead:
```bash
python test_physics_logic.py
```

This tests all physics without requiring OpenGL.

#### 19. Import errors in tests
**Problem:** Can't import simulator module

**Solution:**
```bash
# Ensure you're in the right directory
cd /path/to/watcher

# Check Python path
python -c "import sys; print(sys.path)"

# Run from correct location
python test_physics_logic.py
```

---

### Platform-Specific Issues

#### 20. macOS: "Python quit unexpectedly"
**Problem:** Application crashes on macOS

**Solution:**
- Update to latest pygame: `pip install --upgrade pygame`
- Try running with: `python3 simulator.py` (not just `python`)
- Check macOS OpenGL support (should work on 10.9+)

#### 21. Windows: DLL load failed
**Problem:** Missing DLL errors

**Solution:**
```bash
# Install Visual C++ Redistributable
# Download from Microsoft website

# Or try different pygame version
pip install pygame==2.5.0
```

#### 22. Linux: libGL.so.1: cannot open shared object file
**Problem:** Missing OpenGL libraries

**Solution:**
```bash
# On Ubuntu/Debian
sudo apt-get install libgl1-mesa-glx libglu1-mesa

# On Fedora
sudo dnf install mesa-libGL mesa-libGLU

# On Arch
sudo pacman -S mesa glu
```

---

## Getting Help

If none of these solutions work:

1. **Check the logs:**
   - Look for error messages in terminal
   - Note the exact error text

2. **Verify environment:**
   ```bash
   python --version
   pip list | grep -E "pygame|PyOpenGL|numpy"
   ```

3. **Minimal test:**
   ```bash
   python -c "import pygame; import numpy; print('Imports OK')"
   ```

4. **Run logic tests:**
   ```bash
   python test_physics_logic.py
   ```

5. **Check system requirements:**
   - Python 3.8+
   - Working display
   - OpenGL support
   - 100MB free RAM
   - Modern graphics card (2010+)

---

## Debug Mode

To run with more verbose output, modify simulator.py:

```python
# Add at the top of simulator.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

Or add debug prints:

```python
# In run() method
print(f"FPS: {self.clock.get_fps():.1f}")
print(f"Position: {self.current_object.position}")
```

---

## Still Having Issues?

The most common issues are:
1. ✓ Missing dependencies → Install with pip
2. ✓ No display available → Can't run graphics without display
3. ✓ Outdated graphics drivers → Update them
4. ✓ Wrong Python version → Use 3.8+

For testing without graphics, always use:
```bash
python test_physics_logic.py
```

This validates all physics logic without requiring OpenGL or a display.
