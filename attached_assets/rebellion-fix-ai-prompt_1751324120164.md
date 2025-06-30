# AI Code Agent Prompt: Create Star Wars Rebellion Community Fix Installer

## Project Overview
Create an automated installer script/program for the Star Wars: Rebellion Community Fix v2.63.1.0. The installer should be user-friendly and handle the patch installation process with minimal user intervention.

## Technical Requirements

### Platform
- **Target OS**: Windows (7/8/10/11)
- **Language Options**: Python (with PyInstaller for .exe), PowerShell, or Batch script
- **Preferred**: Python with tkinter GUI or PowerShell with Windows Forms

### Source Files Structure
The patch archive (`Rebellion_2.63.1.0_Fix.zip`) contains:
```
├── Star Wars - Rebellion.txt (readme)
├── REBEXE.dplaysvr.Multi-player.txt (port config)
└── Star Wars - Rebellion.zip
    ├── D3Dlmm.dll
    ├── d3drm.dll
    ├── DDraw.dll
    └── REBEXE.exe
```

### Core Functionality

1. **Game Location Detection**
   - Auto-detect common installation paths (check in this order):
     - **GOG**: `C:\GOG Games\Star Wars - Rebellion`
     - **Steam**: `C:\Program Files (x86)\Steam\steamapps\common\Star Wars - Rebellion`
     - **Original**: `C:\Program Files (x86)\LucasArts\Star Wars Rebellion`
   - If not found in any default location:
     - Prompt: "Star Wars: Rebellion was not found in the default locations. Please select your game installation folder."
     - Provide folder browser dialog for manual selection
   - Validate selected folder contains `REBEXE.exe`

2. **Backup Creation**
   - Check for existing backup folders first
   - If backup exists, prompt: "A backup already exists. Create new backup? (Yes/No/Skip backup)"
   - Automatically backup original files before patching:
     - Create `Backup_[timestamp]` folder in game directory
     - Copy original files:
       - D3Dlmm.dll
       - d3drm.dll
       - DDraw.dll
       - REBEXE.exe
       - ALBRIEF.dll (if exists)
       - EMBRIEF.dll (if exists)
   - Show progress during backup
   - Log backed up files for potential restoration

3. **File Installation**
   - Extract patch files from embedded archive or external ZIP
   - Check if already patched (REBEXE.exe version 1.02)
   - If already patched, prompt: "Game appears to be already patched. Continue anyway? (Yes/No)"
   - Copy the 4 core files to game directory with overwrite
   - Verify file integrity after copy (size/hash check)
   - Confirm REBEXE.exe shows version 1.02 after patching

4. **Optional Features**
   - **Introduction Briefing Removal**:
     - Prompt: "The patched version removes the ability to skip introduction briefings. Would you like to delete these briefing files to skip them entirely? (Yes/No)"
     - If Yes: Look for and remove/rename intro briefing files in AVIDATA folder
     - Provide list of files that will be affected
   
   - **Compatibility Settings**:
     - Prompt: "Would you like to automatically set Windows XP compatibility mode for REBEXE.exe? (Recommended)"
     - If Yes: Apply registry settings or use Windows API to set:
       - Compatibility mode: Windows XP SP3
       - Run as administrator: Enabled

5. **User Interface Requirements**
   - Clear title: "Star Wars: Rebellion Community Fix Installer v2.63.1.0"
   - Progress indicators for each step
   - Status messages:
     - "Searching for game installation..."
     - "Creating backup..."
     - "Installing patch files..."
     - "Configuring compatibility..."
     - "Installation complete!"
   - Error handling with clear messages
   - Option to view installation log

6. **Error Handling**
   - Check for write permissions before starting
   - Verify sufficient disk space
   - Handle locked files (game running)
   - Provide rollback option if installation fails
   - Log all operations to `rebellion_fix_install.log`

7. **Post-Installation**
   - Show summary of installed files
   - Display multiplayer port information from the port config file
   - Option to launch game immediately
   - Option to open game folder

### Code Structure Suggestions

```python
# Example structure for Python implementation
import os
import win32com.client  # For shortcut manipulation

class RebellionFixInstaller:
    def __init__(self):
        self.game_path = None
        self.backup_path = None
        self.shortcuts_modified = []
        self.common_paths = [
            r"C:\GOG Games\Star Wars - Rebellion",
            r"C:\Program Files (x86)\Steam\steamapps\common\Star Wars - Rebellion",
            r"C:\Program Files (x86)\LucasArts\Star Wars Rebellion"
        ]
        
    def find_game_installation(self):
        # Check common paths in order
        for path in self.common_paths:
            if os.path.exists(os.path.join(path, "REBEXE.exe")):
                return path
        return None
        
    def browse_for_folder(self):
        # Open folder dialog
        # Validate selection contains REBEXE.exe
        
    def create_backup(self):
        # Create timestamped backup
        # Copy original files
        
    def install_patch_files(self):
        # Extract and copy files
        # Verify installation
        
    def find_shortcuts(self):
        # Search desktop and start menu for .lnk files
        # Return list of shortcut paths pointing to REBEXE.exe
        
    def modify_shortcut(self, shortcut_path):
        # Load shortcut
        # Add -w flag to arguments
        # Save shortcut
        # Track modification
        
    def create_shortcuts(self):
        # Create desktop shortcut with -w flag
        # Optionally create start menu shortcut
        # Set icon and working directory
        
    def configure_compatibility(self):
        # Set Windows compatibility
        # Registry modifications
        
    def remove_intro_briefings(self):
        # Rename ALBRIEF.dll and EMBRIEF.dll to .backup
        
    def main(self):
        # GUI main loop or CLI flow
```

### Additional Requirements
- Include embedded version info and patch credits
- Add uninstaller option that restores from backup
- Support silent/command-line installation for advanced users:
  - `/silent` - Install with defaults, no prompts
  - `/path "C:\path\to\game"` - Specify game path
  - `/nobriefing` - Remove briefing files automatically
  - `/nobackup` - Skip backup creation
  - `/help` - Show command line options
- Ensure UAC elevation is requested when needed
- Include the network port configuration info as reference
- **Critical**: Ensure all shortcuts are updated with -w flag for proper operation
- Log all shortcut modifications for potential rollback
- Detect if Steam version and warn about potential file verification overwriting the patch
- For Steam installations, consider modifying Steam launch options if possible

### Testing Checklist
The installer should handle:
- [ ] Fresh installation on clean system
- [ ] Upgrade over existing patched version
- [ ] Game in Program Files (requires admin)
- [ ] Game in custom location
- [ ] Missing files scenarios
- [ ] Insufficient permissions
- [ ] Game currently running
- [ ] Shortcut modification (existing shortcuts)
- [ ] Shortcut creation (no shortcuts exist)
- [ ] Multiple shortcuts in different locations
- [ ] Shortcuts with existing command-line arguments

### Deliverables
1. Executable installer (standalone .exe)
2. Source code with comments
3. Brief user documentation
4. Build instructions for future updates