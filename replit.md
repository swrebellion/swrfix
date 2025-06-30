# Star Wars: Rebellion Community Fix Installer

## Overview

This project is a Windows desktop application that automates the installation of the Star Wars: Rebellion Community Fix v2.63.1.0. It's designed to make the patching process simple and user-friendly by providing automatic game detection, safe file backup, and validation throughout the installation process.

The application is built in Python using tkinter for the GUI and provides both graphical and command-line interfaces for different user preferences.

## System Architecture

### Frontend Architecture
- **GUI Framework**: tkinter (Python's built-in GUI library)
- **Architecture Pattern**: Single-window application with step-by-step wizard-style interface
- **User Interface**: Simple, intuitive design with progress indicators and clear messaging
- **Accessibility**: Command-line interface available for advanced users and automation

### Backend Architecture
- **Language**: Python 3.x
- **Architecture Pattern**: Object-oriented design with separation of concerns
- **Core Components**:
  - `RebellionFixInstaller`: Main business logic class
  - `InstallerGUI`: GUI presentation layer
  - Configuration module for constants and settings
  - Utilities module for system operations

### File Structure
```
├── main.py           # Entry point and argument parsing
├── installer.py      # Core installation logic
├── gui.py           # GUI implementation
├── config.py        # Configuration constants
├── utils.py         # Utility functions
└── README.md        # Documentation
```

## Key Components

### 1. Game Detection System
- **Purpose**: Automatically locate Star Wars: Rebellion installations
- **Implementation**: Sequential path checking against predefined common locations
- **Fallback**: Manual folder selection dialog
- **Validation**: Verifies presence of `REBEXE.exe` to confirm valid installation

### 2. Backup System
- **Purpose**: Safely preserve original game files before patching
- **Implementation**: Creates timestamped backup directories
- **Files Backed Up**: All DLL files, executable, and briefing files
- **Recovery**: Maintains backup registry for potential restoration

### 3. Installation Engine
- **Purpose**: Apply community fix patches to the game
- **Files Installed**: 
  - `D3Dlmm.dll` (DirectX compatibility)
  - `d3drm.dll` (Direct3D retained mode)
  - `DDraw.dll` (DirectDraw compatibility)
  - `REBEXE.exe` (Updated game executable v1.02)
- **Safety Checks**: Disk space validation, permission checks, running process detection

### 4. Configuration Management
- **Purpose**: Centralize installer settings and constants
- **Implementation**: Single configuration module with version info, file paths, and patch definitions
- **Flexibility**: Easy to update for new patch versions or additional installation paths

## Data Flow

1. **Initialization**: Application starts and loads configuration
2. **Detection Phase**: 
   - Scans common installation paths
   - Validates game installation
   - Prompts for manual selection if needed
3. **Preparation Phase**:
   - Checks system requirements (disk space, permissions)
   - Creates backup of existing files
   - Validates patch files availability
4. **Installation Phase**:
   - Copies patch files to game directory
   - Configures Windows compatibility settings
   - Optionally removes briefing files
5. **Verification Phase**:
   - Validates installed files
   - Confirms successful installation
   - Logs completion status

## External Dependencies

### Runtime Dependencies
- **Python 3.x**: Core runtime environment
- **tkinter**: GUI framework (included with Python)
- **winreg**: Windows registry access (Windows-specific)
- **ctypes**: Windows API access for admin privilege checking

### System Dependencies
- **Windows 7/8/10/11**: Target operating system
- **Administrator privileges**: Required for installations in Program Files
- **Star Wars: Rebellion**: Target game (any version - GOG, Steam, or original)

### Build Dependencies (for distribution)
- **PyInstaller**: For creating standalone executable
- **Windows SDK**: For proper Windows integration

## Deployment Strategy

### Development Environment
- Python 3.x with standard library
- Windows development machine for testing
- Git for version control

### Distribution Strategy
- **Standalone Executable**: PyInstaller-generated .exe for end users
- **Source Distribution**: Python scripts for developers and advanced users
- **Package Structure**: Installer executable bundled with patch files

### Installation Process
1. User downloads installer package
2. Extracts to temporary directory
3. Runs installer executable
4. Follows GUI wizard or uses command-line options
5. Installer handles all file operations and system configuration

## Changelog
- June 30, 2025: Initial setup and core architecture
- June 30, 2025: Implemented all critical features from AI prompt:
  - ✓ Complete game detection system with 7 common paths
  - ✓ Steam version detection and warnings
  - ✓ Critical shortcut modification with -w flag (as specified)
  - ✓ Comprehensive backup system with timestamp support
  - ✓ All 4 patch files installation (D3Dlmm.dll, d3drm.dll, DDraw.dll, REBEXE.exe)
  - ✓ Windows XP compatibility configuration
  - ✓ Multiplayer port information display
  - ✓ Command-line interface with all specified options
  - ✓ Complete error handling and validation
  - ✓ Professional GUI with progress tracking
  - ✓ Uninstall/restore functionality
  - ✓ Cross-platform compatibility (Windows primary, demo on Linux)

## User Preferences

Preferred communication style: Simple, everyday language.