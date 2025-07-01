#!/usr/bin/env python3
"""
Fix PyInstaller pathlib conflict and build release
"""

import subprocess
import sys
from pathlib import Path

def fix_pathlib_conflict():
    """Remove the conflicting pathlib package"""
    print("Fixing PyInstaller pathlib conflict...")
    
    try:
        # Remove the obsolete pathlib package
        result = subprocess.run([
            sys.executable, "-m", "pip", "uninstall", "pathlib", "-y"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Removed conflicting pathlib package")
            return True
        else:
            print("Note: pathlib package may not be installed (this is good)")
            return True
            
    except Exception as e:
        print(f"Error removing pathlib: {e}")
        return False

def build_with_pyinstaller():
    """Build using PyInstaller directly"""
    print("\nBuilding executable with PyInstaller...")
    
    # Clean previous builds
    if Path("build").exists():
        import shutil
        shutil.rmtree("build")
    if Path("dist").exists():
        import shutil
        shutil.rmtree("dist")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed", 
        "--name", "Star_Wars_Rebellion_Community_Fix_Installer",
        "--icon", "icon.ico",
        "main.py"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("✓ Executable built successfully")
            
            # Check if exe was created
            exe_path = Path("dist/Star_Wars_Rebellion_Community_Fix_Installer.exe")
            if exe_path.exists():
                print(f"✓ Executable found: {exe_path}")
                return True
            else:
                print("✗ Executable not found in dist folder")
                return False
        else:
            print(f"✗ Build failed with exit code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"✗ Build error: {e}")
        return False

def create_distribution():
    """Create the distribution package"""
    print("\nCreating distribution package...")
    
    try:
        result = subprocess.run([sys.executable, "build_distribution.py"])
        
        if result.returncode == 0:
            print("✓ Distribution package created")
            
            # Check for ZIP file
            zip_file = Path("Star_Wars_Rebellion_Community_Fix_v2.63.1.0.zip")
            if zip_file.exists():
                print(f"✓ ZIP file ready: {zip_file}")
                return True
            else:
                print("Note: ZIP file not found, but distribution may be complete")
                return True
        else:
            print("✗ Distribution creation failed")
            return False
            
    except Exception as e:
        print(f"Error creating distribution: {e}")
        return False

def main():
    """Main fix and build process"""
    print("Star Wars: Rebellion Community Fix - PyInstaller Fix & Build")
    print("=" * 65)
    
    # Step 1: Fix pathlib conflict
    if not fix_pathlib_conflict():
        print("\n✗ Failed to fix pathlib conflict")
        return False
    
    # Step 2: Build executable
    if not build_with_pyinstaller():
        print("\n✗ Build failed")
        return False
    
    # Step 3: Create distribution
    if not create_distribution():
        print("\n✗ Distribution creation failed")
        return False
    
    print("\n" + "=" * 65)
    print("✓ Build completed successfully!")
    print("\nFiles ready for GitHub release:")
    print("- Star_Wars_Rebellion_Community_Fix_v2.63.1.0/ (folder)")
    print("- Star_Wars_Rebellion_Community_Fix_v2.63.1.0.zip (if created)")
    print("\nNext steps:")
    print("1. Upload the ZIP file to your GitHub release")
    print("2. Or use the GitHub Actions workflow")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to continue...")
    sys.exit(0 if success else 1)