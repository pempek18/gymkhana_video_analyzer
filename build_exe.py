#!/usr/bin/env python3
"""
Build script for creating executable from Gymkhana Video Analyzer
This script is used by GitHub Actions to build the .exe file
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def setup_icon():
    """Set up the icon file for the build"""
    icon_source = Path("img/pacholek.ico")
    icon_dest = Path("icon.ico")
    
    if icon_source.exists():
        # Copy the existing ICO file to the root for PyInstaller
        shutil.copy2(icon_source, icon_dest)
        print(f"✅ Using existing icon: {icon_source}")
        return True
    else:
        print("⚠️ Warning: img/pacholek.ico not found, no icon will be used")
        return False

def install_requirements():
    """Install required packages for building"""
    print("Installing build requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # PyInstaller command with optimized settings
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=GymkhanaVideoAnalyzer", # Executable name
        "--icon=icon.ico",              # Icon file (if available)
        "--add-data=requirements.txt;.", # Include requirements
        "--hidden-import=cv2",          # Ensure OpenCV is included
        "--hidden-import=PIL",          # Ensure PIL is included
        "--hidden-import=numpy",        # Ensure numpy is included
        "--clean",                      # Clean build cache
        "app.py"                        # Main application file
    ]
    
    # Remove icon flag if icon doesn't exist
    if not Path("icon.ico").exists():
        cmd.remove("--icon=icon.ico")
        print("⚠️ No icon.ico found, executable will use default icon")
    
    subprocess.run(cmd, check=True)
    
    print("Build completed successfully!")

def create_installer():
    """Create a simple installer package"""
    print("Creating installer package...")
    
    # Create dist directory structure
    dist_dir = Path("dist")
    package_dir = dist_dir / "GymkhanaVideoAnalyzer"
    package_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_path = dist_dir / "GymkhanaVideoAnalyzer.exe"
    if exe_path.exists():
        shutil.copy2(exe_path, package_dir / "GymkhanaVideoAnalyzer.exe")
    
    # Copy README
    if Path("README.md").exists():
        shutil.copy2("README.md", package_dir / "README.md")
    
    # Copy requirements
    if Path("requirements.txt").exists():
        shutil.copy2("requirements.txt", package_dir / "requirements.txt")
    
    # Create batch file for easy launching
    batch_content = """@echo off
echo Starting Gymkhana Video Analyzer...
start "" "GymkhanaVideoAnalyzer.exe"
"""
    with open(package_dir / "Launch.bat", "w") as f:
        f.write(batch_content)
    
    # Create ZIP package
    shutil.make_archive(str(dist_dir / "GymkhanaVideoAnalyzer-Windows"), 'zip', package_dir)
    
    print("Installer package created!")

def main():
    """Main build process"""
    try:
        print("Starting build process...")
        
        # Set up icon from existing pacholek.ico
        setup_icon()
        
        # Install requirements
        install_requirements()
        
        # Build executable
        build_executable()
        
        # Create installer
        create_installer()
        
        print("Build process completed successfully!")
        print("Executable location: dist/GymkhanaVideoAnalyzer.exe")
        print("Package location: dist/GymkhanaVideoAnalyzer-Windows.zip")
        
        if Path("icon.ico").exists():
            print("✅ Icon included: Your pacholek.ico is now the taskbar icon!")
        
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
