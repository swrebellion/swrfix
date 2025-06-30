#!/usr/bin/env python3
"""
Distribution packaging script for Windows
Run this on Windows after building the executable
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_distribution():
    """Create complete distribution package"""
    
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
        print(f"✓ Copied main executable")
    else:
        print("✗ Main executable not found! Run PyInstaller first.")
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
    docs = ["README.md", "IMPLEMENTATION_COMPLETE.md"]
    for doc in docs:
        if Path(doc).exists():
            shutil.copy2(doc, dist_path / doc)
    
    # Create installation instructions
    instructions = f"""Star Wars: Rebellion Community Fix Installer v2.63.1.0
================================================================

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

INSTALLATION PROCESS:
The installer will automatically:
1. Detect your game installation
2. Create a timestamped backup of original files
3. Install 4 patch files (D3Dlmm.dll, d3drm.dll, DDraw.dll, REBEXE.exe)
4. Configure Windows XP compatibility mode
5. Modify shortcuts to include the critical -w flag
6. Optionally remove introduction briefing files

MULTIPLAYER CONFIGURATION:
Default Ports: TCP/UDP 2300-2400
Ensure these ports are open in your firewall for multiplayer games.

TROUBLESHOOTING:
- If auto-detection fails, use the Browse button to manually select your game folder
- For Steam versions, disable automatic updates to prevent patch overwrites
- Run as Administrator if you get permission errors
- Check the log file (rebellion_fix_install.log) for detailed error information

For support and updates, visit the community forums.

Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open(dist_path / "INSTALLATION_INSTRUCTIONS.txt", 'w') as f:
        f.write(instructions)
    
    # Create ZIP package
    zip_name = f"{dist_name}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dist_path.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(dist_path.parent)
                zipf.write(file_path, arcname)
    
    print(f"✓ Created distribution package: {zip_name}")
    
    # Calculate sizes
    exe_size = (dist_path / "Star_Wars_Rebellion_Community_Fix_Installer.exe").stat().st_size / (1024*1024)
    zip_size = Path(zip_name).stat().st_size / (1024*1024)
    
    print(f"✓ Executable size: {exe_size:.1f} MB")
    print(f"✓ Package size: {zip_size:.1f} MB")
    print(f"✓ Ready for distribution!")
    
    return True

if __name__ == "__main__":
    print("Creating distribution package...")
    create_distribution()
