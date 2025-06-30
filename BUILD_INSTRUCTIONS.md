# Building Star Wars: Rebellion Community Fix Installer

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
