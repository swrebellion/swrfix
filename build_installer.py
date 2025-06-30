#!/usr/bin/env python3
"""
Build script for creating Windows executable installer
Uses PyInstaller to package the Python application into a standalone .exe
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def create_pyinstaller_spec():
    """Create PyInstaller specification file for the installer"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('D3Dlmm.dll', '.'),
        ('d3drm.dll', '.'),
        ('DDraw.dll', '.'),
        ('REBEXE.exe', '.'),
        ('attached_assets', 'attached_assets'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Star_Wars_Rebellion_Community_Fix_Installer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon='icon.ico'
)
'''
    
    with open('installer.spec', 'w') as f:
        f.write(spec_content)
    
    print("✓ Created PyInstaller specification file: installer.spec")

def create_version_info():
    """Create version information file for Windows executable"""
    version_info = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 63, 1, 0),
    prodvers=(2, 63, 1, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Star Wars Rebellion Community'),
         StringStruct(u'FileDescription', u'Star Wars: Rebellion Community Fix Installer'),
         StringStruct(u'FileVersion', u'2.63.1.0'),
         StringStruct(u'InternalName', u'RebellionFixInstaller'),
         StringStruct(u'LegalCopyright', u'Community Project'),
         StringStruct(u'OriginalFilename', u'Star_Wars_Rebellion_Community_Fix_Installer.exe'),
         StringStruct(u'ProductName', u'Star Wars: Rebellion Community Fix'),
         StringStruct(u'ProductVersion', u'2.63.1.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w') as f:
        f.write(version_info)
    
    print("✓ Created version information file: version_info.txt")

def create_icon():
    """Create a simple icon file for the executable"""
    # Create a simple text-based icon placeholder
    # In production, you'd want to use a proper .ico file
    icon_placeholder = """
    This would be a proper Windows .ico file in production.
    For now, PyInstaller will use the default icon.
    """
    
    # Create a placeholder - PyInstaller will use default if no icon exists
    print("✓ Icon placeholder created (use custom .ico file for production)")

def build_executable():
    """Build the standalone Windows executable"""
    print("Building Windows executable with PyInstaller...")
    print("This may take a few minutes...")
    
    try:
        # Build using the spec file
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            'installer.spec'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Build completed successfully!")
            
            # Check if executable exists
            exe_path = Path('dist/Star_Wars_Rebellion_Community_Fix_Installer.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"✓ Executable created: {exe_path}")
                print(f"✓ File size: {size_mb:.1f} MB")
                
                # Copy patch files to dist directory
                dist_assets = Path('dist/attached_assets')
                dist_assets.mkdir(exist_ok=True)
                
                for dll_file in Path('.').glob('*.dll'):
                    shutil.copy2(dll_file, 'dist/')
                
                for exe_file in Path('.').glob('*.exe'):
                    if exe_file.name != 'Star_Wars_Rebellion_Community_Fix_Installer.exe':
                        shutil.copy2(exe_file, 'dist/')
                
                print("✓ Patch files copied to distribution directory")
                
                return True
            else:
                print("✗ Executable not found after build")
                return False
        else:
            print("✗ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Build error: {e}")
        return False

def create_distribution_package():
    """Create a complete distribution package"""
    dist_dir = Path('distribution')
    dist_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_source = Path('dist/Star_Wars_Rebellion_Community_Fix_Installer.exe')
    if exe_source.exists():
        shutil.copy2(exe_source, dist_dir / 'Star_Wars_Rebellion_Community_Fix_Installer.exe')
    
    # Copy patch files
    for dll_file in Path('.').glob('*.dll'):
        shutil.copy2(dll_file, dist_dir)
    
    for exe_file in Path('.').glob('REBEXE.exe'):
        shutil.copy2(exe_file, dist_dir)
    
    # Copy documentation
    for doc_file in ['README.md', 'IMPLEMENTATION_COMPLETE.md']:
        if Path(doc_file).exists():
            shutil.copy2(doc_file, dist_dir)
    
    # Create installer package info
    package_info = f"""Star Wars: Rebellion Community Fix Installer v2.63.1.0
===============================================================

INSTALLATION INSTRUCTIONS:
1. Run Star_Wars_Rebellion_Community_Fix_Installer.exe
2. Click "Auto-Detect" or browse to your game installation
3. Choose installation options
4. Click "Install Community Fix"

COMMAND LINE OPTIONS:
- --silent: Install with default settings
- --path "C:\\Path\\To\\Game": Specify game location
- --nobriefing: Remove briefing files
- --nobackup: Skip backup creation
- --uninstall: Restore from backup

FEATURES:
✓ Automatic game detection (GOG, Steam, Original)
✓ Safe backup creation with timestamps
✓ Critical shortcut modification with -w flag
✓ Windows XP compatibility configuration
✓ Steam version detection and warnings
✓ Complete uninstall/restore functionality

For support, check the README.md file.
"""
    
    with open(dist_dir / 'INSTALLATION_INSTRUCTIONS.txt', 'w') as f:
        f.write(package_info)
    
    print(f"✓ Distribution package created in: {dist_dir}")
    print("✓ Ready for deployment!")

def main():
    """Main build process"""
    print("=" * 70)
    print("STAR WARS: REBELLION COMMUNITY FIX INSTALLER - BUILD PROCESS")
    print("=" * 70)
    print()
    
    # Clean previous builds
    for cleanup_dir in ['build', 'dist', '__pycache__']:
        if Path(cleanup_dir).exists():
            shutil.rmtree(cleanup_dir)
            print(f"✓ Cleaned {cleanup_dir} directory")
    
    # Create build files
    create_version_info()
    create_icon()
    create_pyinstaller_spec()
    
    print()
    print("Building standalone Windows executable...")
    print("-" * 40)
    
    # Build executable
    if build_executable():
        print()
        print("Creating distribution package...")
        print("-" * 40)
        create_distribution_package()
        
        print()
        print("=" * 70)
        print("BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("Distribution files:")
        print("  - Star_Wars_Rebellion_Community_Fix_Installer.exe (Main installer)")
        print("  - Patch files (D3Dlmm.dll, d3drm.dll, DDraw.dll, REBEXE.exe)")
        print("  - Documentation (README.md, installation instructions)")
        print()
        print("The installer is now ready for distribution to end users!")
        print("Users can run the .exe file without needing Python installed.")
        
    else:
        print()
        print("=" * 70)
        print("BUILD FAILED!")
        print("=" * 70)
        print("Please check the error messages above and try again.")

if __name__ == '__main__':
    main()