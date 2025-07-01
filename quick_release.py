#!/usr/bin/env python3
"""
Quick release builder - uses existing build_distribution.py
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Quick release using existing scripts"""
    print("Star Wars: Rebellion Community Fix - Quick Release")
    print("=" * 50)
    
    # Check if executable exists
    exe_path = Path("dist/Star_Wars_Rebellion_Community_Fix_Installer.exe")
    if exe_path.exists():
        print("✓ Executable already exists")
    else:
        print("✗ Executable not found. Please build it first with:")
        print("  python prepare_release.py")
        print("  or run: build.bat")
        return False
    
    # Run the existing distribution builder
    print("\nCreating distribution package...")
    try:
        result = subprocess.run([sys.executable, "build_distribution.py"])
        if result.returncode == 0:
            print("✓ Distribution package created successfully!")
        else:
            print("✗ Distribution creation failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    # Check results
    dist_folder = "Star_Wars_Rebellion_Community_Fix_v2.63.1.0"
    zip_file = f"{dist_folder}.zip"
    
    if Path(dist_folder).exists():
        print(f"✓ Distribution folder: {dist_folder}")
    
    if Path(zip_file).exists():
        print(f"✓ ZIP file: {zip_file}")
    
    print("\n" + "=" * 50)
    print("✓ Release ready for GitHub!")
    print(f"Upload the folder or ZIP file to your GitHub release.")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to continue...")
    sys.exit(0 if success else 1)