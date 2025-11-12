# Installation Guide - Version 2.0

## Error: "No module named 'pygame_gui'"

If you see this error, it means you need to install the new dependency added in Version 2.0.

### Solution

Run this command in your terminal/command prompt:

```bash
pip install -r requirements.txt
```

Or install pygame-gui specifically:

```bash
pip install pygame-gui==0.6.9
```

### Why This Happened

Version 2.0 introduced a professional GUI interface using the `pygame-gui` library. This is a new dependency that wasn't in Version 1.0.

### Step-by-Step Installation

#### Windows (Command Prompt or PowerShell)

```cmd
# Navigate to the project directory
cd C:\Users\YourUsername\Downloads\watcher

# Install all dependencies
pip install -r requirements.txt

# Run the simulator
python simulator.py
```

#### macOS/Linux (Terminal)

```bash
# Navigate to the project directory
cd ~/Downloads/watcher

# Install all dependencies
pip install -r requirements.txt

# Run the simulator
python simulator.py
```

### Alternative: Use start.py

The `start.py` script will automatically check for missing dependencies and offer to install them:

```bash
python start.py
```

When prompted, type `y` to install missing dependencies.

### Verifying Installation

To verify pygame-gui is installed correctly:

```bash
python -c "import pygame_gui; print('pygame-gui version:', pygame_gui.__version__)"
```

Expected output:
```
pygame-gui version: 0.6.9
```

### Complete Dependency List

Version 2.0 requires:

1. **pygame** 2.5.2 - Graphics and windowing
2. **PyOpenGL** 3.1.7 - 3D rendering
3. **numpy** 1.26.3 - Mathematical operations
4. **pygame-gui** 0.6.9 - GUI interface (NEW in v2.0)

### Troubleshooting

#### Issue: "pip: command not found"

Try using:
```bash
python -m pip install -r requirements.txt
```

or

```bash
python3 -m pip install -r requirements.txt
```

#### Issue: "Permission denied"

On Linux/macOS, you might need to install for your user only:
```bash
pip install --user -r requirements.txt
```

#### Issue: pygame-gui conflicts

If you have issues with pygame-gui, try:
```bash
pip uninstall pygame-gui
pip install pygame-gui==0.6.9
```

#### Issue: Old pygame version

pygame-gui requires pygame-ce (Community Edition) 2.1.4+. If you get compatibility errors:
```bash
pip install --upgrade pygame
pip install pygame-gui==0.6.9
```

### Fresh Installation

If you want to start completely fresh:

```bash
# Uninstall all related packages
pip uninstall pygame PyOpenGL numpy pygame-gui -y

# Install fresh from requirements.txt
pip install -r requirements.txt
```

### Virtual Environment (Recommended)

For a clean installation, use a virtual environment:

#### Windows
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python simulator.py
```

#### macOS/Linux
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python simulator.py
```

### Need More Help?

1. Check you're in the correct directory (where `requirements.txt` is located)
2. Make sure you're using Python 3.8 or higher: `python --version`
3. Try updating pip: `pip install --upgrade pip`
4. Check if requirements.txt exists: `ls requirements.txt` (Linux/Mac) or `dir requirements.txt` (Windows)

### Quick Commands Summary

```bash
# 1. Navigate to project folder
cd path/to/watcher

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run simulator
python simulator.py
```

That's it! After installing dependencies, the simulator should launch without errors.
