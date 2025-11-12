#!/usr/bin/env python3
"""
Quick Start Script for 3D Projectile Motion Simulator
Checks dependencies and launches the application
"""

import sys
import subprocess

def check_python_version():
    """Check if Python version is sufficient"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required = ['pygame', 'OpenGL', 'numpy', 'pygame_gui']
    missing = []
    
    for package in required:
        try:
            __import__(package if package != 'OpenGL' else 'OpenGL.GL')
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
            missing.append(package)
    
    return len(missing) == 0, missing

def install_dependencies():
    """Install missing dependencies"""
    print("\n🔧 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def launch_simulator():
    """Launch the simulator application"""
    print("\n🚀 Launching 3D Projectile Motion Simulator...")
    print("   Press ESC to exit the application\n")
    try:
        import simulator
        simulator.main()
    except Exception as e:
        print(f"❌ Error launching simulator: {e}")
        import traceback
        traceback.print_exc()
        return False
    return True

def main():
    """Main entry point"""
    print("=" * 60)
    print("   3D PROJECTILE MOTION SIMULATOR - QUICK START")
    print("=" * 60)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    deps_ok, missing = check_dependencies()
    
    if not deps_ok:
        print(f"\n⚠ Missing dependencies: {', '.join(missing)}")
        response = input("\nWould you like to install them now? (y/n): ")
        if response.lower() == 'y':
            if not install_dependencies():
                sys.exit(1)
        else:
            print("\nPlease install dependencies manually:")
            print("  pip install -r requirements.txt")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("   ALL CHECKS PASSED - READY TO LAUNCH")
    print("=" * 60)
    
    # Launch
    if not launch_simulator():
        sys.exit(1)
    
    print("\n✓ Simulator closed successfully")

if __name__ == "__main__":
    main()
