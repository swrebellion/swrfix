#!/usr/bin/env python3
"""
Simple build script for creating a standalone installer package
Creates a basic PyInstaller command that will work on Windows
"""

import os
import shutil
from pathlib import Path

def create_build_instructions():
    """Create detailed build instructions for Windows deployment"""
    
    instructions = """# Building Star Wars: Rebellion Community Fix Installer

## Prerequisites (Windows)
1. Install Python 3.11+ from python.org
2. Install PyInstaller: `pip install pyinstaller`
3. Install pywin32: `pip install pywin32`

## Build Process

### Method 1: Simple One-Line Build
```cmd
pyinstaller --onefile --windowed --name "Star_Wars_Rebellion_Community_Fix_Installer" --icon=icon.ico main.py
```

### Method 2: Advanced Build with Custom Spec
```cmd
pyinstaller installer.spec
```

### Method 3: Complete Distribution Package
```cmd
python build_distribution.py
```

## Files Required for Distribution
- Star_Wars_Rebellion_Community_Fix_Installer.exe (main executable)
- D3Dlmm.dll (patch file)
- d3drm.dll (patch file)
- DDraw.dll (patch file)
- REBEXE.exe (patch file)

## Distribution Structure
```
Star_Wars_Rebellion_Community_Fix_v2.63.1.0/
├── Star_Wars_Rebellion_Community_Fix_Installer.exe
├── D3Dlmm.dll
├── d3drm.dll
├── DDraw.dll
├── REBEXE.exe
├── README.md
└── INSTALLATION_INSTRUCTIONS.txt
```

## Testing the Executable
1. Copy all files to a clean Windows machine
2. Run the .exe file
3. Test auto-detection and manual selection
4. Verify all installation steps complete successfully
5. Test uninstall functionality

## Notes
- The executable will be approximately 15-25MB
- Windows Defender may flag the executable initially (normal for PyInstaller)
- Users do not need Python installed to run the .exe file
- The installer requires Windows 7 or higher
"""

    with open('BUILD_INSTRUCTIONS.md', 'w') as f:
        f.write(instructions)
    
    print("✓ Created BUILD_INSTRUCTIONS.md")

def create_distribution_script():
    """Create a distribution packaging script for Windows"""
    
    script = '''#!/usr/bin/env python3
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
    instructions = f\"\"\"Star Wars: Rebellion Community Fix Installer v2.63.1.0
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
--path "C:\\\\Game\\\\Path"    Specify game installation directory
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
\"\"\"
    
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
'''

    with open('build_distribution.py', 'w') as f:
        f.write(script)
    
    print("✓ Created build_distribution.py")

def create_simple_spec():
    """Create a simplified PyInstaller spec file"""
    
    spec = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Star_Wars_Rebellion_Community_Fix_Installer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''

    with open('installer_simple.spec', 'w') as f:
        f.write(spec)
    
    print("✓ Created installer_simple.spec")

def create_batch_build_script():
    """Create a Windows batch script for easy building"""
    
    batch_script = '''@echo off
echo Building Star Wars: Rebellion Community Fix Installer...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from python.org
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Check if pywin32 is installed
python -c "import win32api" >nul 2>&1
if errorlevel 1 (
    echo Installing pywin32...
    pip install pywin32
)

echo.
echo Building executable...
pyinstaller --onefile --windowed --name "Star_Wars_Rebellion_Community_Fix_Installer" main.py

if exist "dist\\Star_Wars_Rebellion_Community_Fix_Installer.exe" (
    echo.
    echo ✓ Build successful!
    echo ✓ Executable created: dist\\Star_Wars_Rebellion_Community_Fix_Installer.exe
    echo.
    echo Creating distribution package...
    python build_distribution.py
    echo.
    echo ✓ Ready for distribution!
    echo Check the created ZIP file for the complete package.
) else (
    echo.
    echo ✗ Build failed!
    echo Check the output above for errors.
)

echo.
pause
'''

    with open('build.bat', 'w') as f:
        f.write(batch_script)
    
    print("✓ Created build.bat (Windows batch script)")

def main():
    """Create all build-related files"""
    print("Creating build files for Windows deployment...")
    print("=" * 50)
    
    create_build_instructions()
    create_distribution_script()
    create_simple_spec()
    create_batch_build_script()
    
    print()
    print("✓ All build files created successfully!")
    print()
    print("TO BUILD ON WINDOWS:")
    print("1. Copy all project files to a Windows machine")
    print("2. Install Python 3.11+ from python.org")
    print("3. Run: build.bat")
    print("   OR")
    print("4. Run: pip install pyinstaller pywin32")
    print("5. Run: pyinstaller --onefile --windowed main.py")
    print()
    print("The result will be a standalone .exe file that users")
    print("can run without having Python installed.")

if __name__ == '__main__':
    main()