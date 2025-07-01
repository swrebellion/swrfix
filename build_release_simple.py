#!/usr/bin/env python3
"""
Simple release builder that uses existing build scripts
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Simple release build using existing scripts"""
    print("Star Wars: Rebellion Community Fix - Simple Release Builder")
    print("=" * 60)
    
    # Check if we're on Windows
    if os.name != 'nt':
        print("This build script is designed for Windows.")
        print("Using existing build_distribution.py script...")
        
        try:
            result = subprocess.run([sys.executable, "build_distribution.py"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Build completed successfully!")
                print(result.stdout)
            else:
                print("✗ Build failed:")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"✗ Error running build script: {e}")
            return False
    else:
        # On Windows, try to use the batch file first
        if Path("build.bat").exists():
            print("Using Windows batch build script...")
            try:
                result = subprocess.run(["build.bat"], shell=True)
                if result.returncode == 0:
                    print("✓ Build completed successfully!")
                else:
                    print("✗ Build failed with batch script")
                    return False
            except Exception as e:
                print(f"✗ Error running batch script: {e}")
                print("Trying Python build script instead...")
                
                try:
                    result = subprocess.run([sys.executable, "build_distribution.py"], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        print("✓ Build completed successfully!")
                        print(result.stdout)
                    else:
                        print("✗ Build failed:")
                        print(result.stderr)
                        return False
                except Exception as e:
                    print(f"✗ Error running Python build script: {e}")
                    return False
        else:
            print("build.bat not found, using Python build script...")
            try:
                result = subprocess.run([sys.executable, "build_distribution.py"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✓ Build completed successfully!")
                    print(result.stdout)
                else:
                    print("✗ Build failed:")
                    print(result.stderr)
                    return False
            except Exception as e:
                print(f"✗ Error running build script: {e}")
                return False
    
    # Check if distribution was created
    dist_folder = "Star_Wars_Rebellion_Community_Fix_v2.63.1.0"
    zip_file = f"{dist_folder}.zip"
    
    if Path(dist_folder).exists():
        print(f"✓ Distribution folder created: {dist_folder}")
    
    if Path(zip_file).exists():
        print(f"✓ ZIP file created: {zip_file}")
        print("\nReady for GitHub release!")
        print("\nNext steps:")
        print("1. Upload the ZIP file to your GitHub release")
        print("2. Or use the GitHub Actions workflow for automatic releases")
    else:
        print("Note: No ZIP file found. You may need to create it manually.")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to continue...")
    sys.exit(0 if success else 1)