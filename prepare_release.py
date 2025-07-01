#!/usr/bin/env python3
"""
Star Wars: Rebellion Community Fix Installer
Release preparation script
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
import zipfile

def check_requirements():
    """Check if all requirements are met for building"""
    print("Checking requirements...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")
    
    # Check if pywin32 is installed (for Windows shortcuts)
    try:
        import win32com
        print("✓ pywin32 is installed")
    except ImportError:
        print("✗ pywin32 not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
        print("✓ pywin32 installed")
    
    # Check if all patch files exist
    patch_files = ["D3Dlmm.dll", "d3drm.dll", "DDraw.dll", "REBEXE.exe"]
    for patch_file in patch_files:
        if Path(patch_file).exists():
            print(f"✓ {patch_file} found")
        else:
            print(f"✗ Missing patch file: {patch_file}")
            return False
    
    return True

def build_executable():
    """Build the standalone executable"""
    print("\nBuilding executable...")
    
    # Clean previous builds
    if Path("build").exists():
        shutil.rmtree("build")
    if Path("dist").exists():
        shutil.rmtree("dist")
    
    # Try to find pyinstaller executable
    pyinstaller_cmd = None
    
    # Check if pyinstaller is in PATH
    try:
        subprocess.check_call(["pyinstaller", "--version"], 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
        pyinstaller_cmd = "pyinstaller"
        print("✓ Found pyinstaller in PATH")
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Try python -m PyInstaller
        try:
            subprocess.check_call([sys.executable, "-m", "PyInstaller", "--version"], 
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.DEVNULL)
            pyinstaller_cmd = [sys.executable, "-m", "PyInstaller"]
            print("✓ Found PyInstaller as Python module")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ PyInstaller not found. Trying to install...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])
                pyinstaller_cmd = [sys.executable, "-m", "PyInstaller"]
                print("✓ PyInstaller installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install PyInstaller: {e}")
                return False
    
    # Build command
    if isinstance(pyinstaller_cmd, str):
        cmd = [pyinstaller_cmd]
    else:
        cmd = pyinstaller_cmd
    
    cmd.extend([
        "--onefile",
        "--windowed",
        "--name", "Star_Wars_Rebellion_Community_Fix_Installer",
        "main.py"
    ])
    
    # Add icon if it exists
    if Path("icon.ico").exists():
        cmd.extend(["--icon", "icon.ico"])
        print("✓ Using icon.ico for executable")
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("✓ Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed with exit code {e.returncode}")
        print("Try running the command manually to see detailed error messages")
        return False
    except FileNotFoundError as e:
        print(f"✗ Command not found: {e}")
        print("Please ensure PyInstaller is properly installed")
        return False

def create_distribution():
    """Create complete distribution package"""
    print("\nCreating distribution package...")
    
    # Create distribution directory
    dist_name = "Star_Wars_Rebellion_Community_Fix_v2.63.1.0"
    dist_path = Path(dist_name)
    
    if dist_path.exists():
        shutil.rmtree(dist_path)
    
    dist_path.mkdir()
    
    # Copy main executable
    exe_source = Path("dist/Star_Wars_Rebellion_Community_Fix_Installer.exe")
    if exe_source.exists():
        shutil.copy2(exe_source, dist_path / "Star_Wars_Rebellion_Community_Fix_Installer.exe")
        print("✓ Copied main executable")
    else:
        print("✗ Main executable not found!")
        return False
    
    # Copy patch files
    patch_files = ["D3Dlmm.dll", "d3drm.dll", "DDraw.dll", "REBEXE.exe"]
    for patch_file in patch_files:
        if Path(patch_file).exists():
            shutil.copy2(patch_file, dist_path / patch_file)
            print(f"✓ Copied {patch_file}")
        else:
            print(f"✗ Missing patch file: {patch_file}")
    
    # Copy documentation
    docs = ["README.md", "LICENSE"]
    for doc in docs:
        if Path(doc).exists():
            shutil.copy2(doc, dist_path / doc)
            print(f"✓ Copied {doc}")
    
    # Create installation instructions
    instructions = """Star Wars: Rebellion Community Fix Installer v2.63.1.0
========================================================

QUICK START:
1. Run Star_Wars_Rebellion_Community_Fix_Installer.exe
2. Click "Auto-Detect" to find your game
3. Click "Install Community Fix"

FEATURES:
✓ Automatic game detection (GOG, Steam, Original versions)
✓ Safe backup creation with timestamps
✓ Critical shortcut modification with -w flag for proper operation
✓ Windows XP compatibility configuration
✓ Steam version detection and warnings
✓ Complete uninstall/restore functionality

COMMAND LINE OPTIONS:
Star_Wars_Rebellion_Community_Fix_Installer.exe [options]

--silent                Install with default settings, no GUI
--path "C:\\Game\\Path"    Specify game installation directory
--nobriefing            Remove introduction briefing files
--nobackup              Skip backup creation (not recommended)
--uninstall             Restore game from backup

SYSTEM REQUIREMENTS:
- Windows 7/8/10/11 (32-bit or 64-bit)
- Star Wars: Rebellion (any version: GOG, Steam, or Original)
- 50MB free disk space
- Administrator privileges (for Program Files installations)

MULTIPLAYER CONFIGURATION:
Default Ports: TCP/UDP 2300-2400
Ensure these ports are open in your firewall for multiplayer games.

SUPPORT:
For issues, please check the log file: rebellion_fix_install.log
"""
    
    with open(dist_path / "INSTALLATION_INSTRUCTIONS.txt", "w") as f:
        f.write(instructions)
    print("✓ Created installation instructions")
    
    print(f"✓ Distribution package created: {dist_name}")
    return dist_path

def create_zip_archive(dist_path):
    """Create ZIP archive for release"""
    print("\nCreating ZIP archive...")
    
    zip_name = f"{dist_path.name}.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dist_path.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(dist_path.parent)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")
    
    print(f"✓ ZIP archive created: {zip_name}")
    return zip_name

def main():
    """Main release preparation process"""
    print("Star Wars: Rebellion Community Fix - Release Preparation")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("\n✗ Requirements check failed!")
        return False
    
    # Build executable
    if not build_executable():
        print("\n✗ Build failed!")
        return False
    
    # Create distribution
    dist_path = create_distribution()
    if not dist_path:
        print("\n✗ Distribution creation failed!")
        return False
    
    # Create ZIP archive
    zip_file = create_zip_archive(dist_path)
    
    print("\n" + "=" * 60)
    print("✓ Release preparation complete!")
    print(f"✓ Distribution folder: {dist_path}")
    print(f"✓ ZIP archive: {zip_file}")
    print("\nReady for GitHub release upload!")
    print("\nNext steps:")
    print("1. Push your code to GitHub")
    print("2. Create a new release on GitHub")
    print("3. Upload the ZIP file to the release")
    print("4. Or push a git tag to trigger automatic release via GitHub Actions")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)