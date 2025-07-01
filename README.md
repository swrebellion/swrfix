# Star Wars: Rebellion Community Fix Installer

An automated installer for the Star Wars: Rebellion Community Fix v2.63.1.0, designed to make the patch installation process simple and user-friendly.

## Features

### Automatic Game Detection
- Automatically detects Star Wars: Rebellion installations in common locations:
  - GOG: `C:\GOG Games\Star Wars - Rebellion`
  - Steam: `C:\Program Files (x86)\Steam\steamapps\common\Star Wars - Rebellion`
  - Original: `C:\Program Files (x86)\LucasArts\Star Wars Rebellion`
- Manual folder selection if auto-detection fails
- Validates game installation before proceeding

### Safe Installation Process
- Creates timestamped backups of original files before patching
- Verifies file integrity after installation
- Checks for sufficient disk space and permissions
- Detects if game is currently running

### Patch Installation
- Installs the following community fix files:
  - `D3Dlmm.dll` - DirectX compatibility
  - `d3drm.dll` - Direct3D retained mode
  - `DDraw.dll` - DirectDraw compatibility
  - `REBEXE.exe` - Updated game executable (v1.02)

### Additional Features
- Windows XP compatibility mode configuration
- Optional removal of introduction briefing files
- Comprehensive error handling and logging
- Uninstall/restore functionality
- Command-line support for advanced users

## Installation

### Requirements
- Windows 7/8/10/11 (32-bit or 64-bit)
- Star Wars: Rebellion (any version - GOG, Steam, or original)
- 50MB free disk space
- Administrator privileges (for installations in Program Files)

### Download & Install
1. **Download the release package** from GitHub Releases
2. **Extract all files** to a folder on your computer
3. **Run** `Star_Wars_Rebellion_Community_Fix_Installer.exe`
4. **Follow the installer wizard**:
   - Click "Auto-Detect" to find your game installation
   - Or use "Browse" to manually select your game folder
   - Choose installation options (briefing removal, etc.)
   - Click "Install Community Fix"

### What's Included
The release package contains:
- Main installer executable (no Python installation required)
- All required patch files (`D3Dlmm.dll`, `d3drm.dll`, `DDraw.dll`, `REBEXE.exe`)
- Documentation and installation instructions

### Command Line Installation
The installer supports several command-line options for advanced users:

```bash
# Silent installation with default settings
installer.exe --silent

# Specify custom game path
installer.exe --silent --path "C:\Games\Star Wars Rebellion"

# Skip backup creation
installer.exe --silent --nobackup

# Automatically remove briefing files
installer.exe --silent --nobriefing

# Uninstall patch and restore from backup
installer.exe --uninstall

## For Developers

### Building from Source

**Prerequisites:**
- Python 3.11+ 
- PyInstaller (`pip install pyinstaller pywin32`)

**Quick Build:**
```cmd
python prepare_release.py
```

**Alternative Build Methods:**
```cmd
# Windows batch script
build.bat

# Quick release (if executable already exists)
python quick_release.py

# Fix PyInstaller issues
python fix_pyinstaller.py
```

### Project Structure
```
├── main.py           # Entry point
├── installer.py      # Core installation logic  
├── gui.py           # GUI implementation
├── config.py        # Configuration constants
├── utils.py         # Utility functions
├── build scripts/   # Release preparation tools
└── .github/         # GitHub Actions workflow
```

### GitHub Releases

**Automatic Release:**
```bash
git tag v2.63.1.0
git push origin v2.63.1.0
```

**Manual Release:**
1. Run `python prepare_release.py`
2. Upload the generated ZIP file to GitHub Releases

## Support

- **Installation Issues**: Check `rebellion_fix_install.log` for detailed error information
- **Multiplayer Setup**: Ensure ports TCP/UDP 2300-2400 are open in your firewall
- **Steam Users**: Be aware that Steam may overwrite patch files during game verification

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Star Wars: Rebellion Community Fix v2.63.1.0 developers
- All contributors and testers
- Star Wars: Rebellion community
