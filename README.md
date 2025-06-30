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
- Windows 7/8/10/11
- Star Wars: Rebellion (any version - GOG, Steam, or original)
- Administrator privileges (for installations in Program Files)

### GUI Installation
1. Download the installer and patch files
2. Place the patch files (`D3Dlmm.dll`, `d3drm.dll`, `DDraw.dll`, `REBEXE.exe`) in the same directory as the installer
3. Run the installer
4. The installer will automatically detect your game installation
5. Choose your installation options
6. Click "Install Community Fix"

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
