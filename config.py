"""
Star Wars: Rebellion Community Fix Installer
Configuration constants

Contributors:
- TruthRealm: Creator of the Star Wars: Rebellion Community Fix v2.63.1.0 patches
- Stratus (via Replit Agent AI / Claude Sonnet 4): Creator of this installer application
"""

# Installer version
VERSION = "2.63.1.0"

# Common installation paths to check (in order of preference)
COMMON_PATHS = [
    r"C:\GOG Games\Star Wars - Rebellion",
    r"C:\Program Files (x86)\Steam\steamapps\common\Star Wars - Rebellion",
    r"C:\Program Files (x86)\LucasArts\Star Wars Rebellion",
    r"C:\Program Files\LucasArts\Star Wars Rebellion",
    r"C:\Games\Star Wars - Rebellion",
    r"D:\GOG Games\Star Wars - Rebellion",
    r"D:\Program Files (x86)\Steam\steamapps\common\Star Wars - Rebellion"
]

# Patch files that need to be installed
PATCH_FILES = [
    "D3Dlmm.dll",
    "d3drm.dll", 
    "DDraw.dll",
    "REBEXE.exe"
]

# Files to backup before patching
BACKUP_FILES = [
    "D3Dlmm.dll",
    "d3drm.dll",
    "DDraw.dll", 
    "REBEXE.exe",
    "ALBRIEF.dll",  # Alliance briefing files
    "EMBRIEF.dll"   # Empire briefing files
]

# Expected file hashes for verification (if needed)
PATCH_FILE_HASHES = {
    # These would be filled in with actual hashes of the patch files
    # "REBEXE.exe": "expected_hash_here",
    # "D3Dlmm.dll": "expected_hash_here",
    # etc.
}

# Minimum disk space required (in bytes)
MIN_DISK_SPACE = 50 * 1024 * 1024  # 50MB

# Multiplayer port information
MULTIPLAYER_INFO = """
Star Wars: Rebellion Multiplayer Port Configuration:

Default Ports:
- TCP: 2300-2400
- UDP: 2300-2400

For multiplayer games, ensure these ports are open in your firewall.
You may need to forward these ports in your router for hosting games.

The game uses DirectPlay for networking. Modern Windows versions
may require additional configuration for multiplayer functionality.
"""

# Installation notes
INSTALLATION_NOTES = """
Star Wars: Rebellion Community Fix v2.63.1.0

This patch includes:
- Updated DirectX compatibility files
- Fixed REBEXE.exe for modern Windows systems
- Improved stability and performance
- Bug fixes and enhancements

Notes:
- The patched version may remove the ability to skip introduction briefings
- Windows XP compatibility mode is recommended
- Run as administrator may be required
- Original files are backed up before installation

For more information, visit the community forums or check the readme files.
"""

# Registry paths for compatibility settings
COMPATIBILITY_REG_PATH = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"

# Compatibility flags to apply
COMPATIBILITY_FLAGS = "WINXPSP3 RUNASADMIN"

# Log file configuration
LOG_FILE = "rebellion_fix_install.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# GUI configuration
WINDOW_TITLE = f"Star Wars: Rebellion Community Fix Installer v{VERSION}"
WINDOW_SIZE = "600x500"
WINDOW_RESIZABLE = False

# Installation steps for progress tracking
INSTALLATION_STEPS = [
    "Initializing...",
    "Creating backup...", 
    "Installing patch files...",
    "Configuring compatibility...",
    "Modifying shortcuts with -w flag...",
    "Removing briefing files...",
    "Installation complete!"
]

# Error messages
ERROR_MESSAGES = {
    "game_not_found": "Star Wars: Rebellion installation not found in common locations.",
    "invalid_path": "The selected path does not contain a valid game installation.",
    "missing_patch_files": "Required patch files are missing from the installer directory.",
    "insufficient_permissions": "Insufficient permissions to modify game files.",
    "game_running": "The game is currently running. Please close it before installing.",
    "insufficient_space": "Insufficient disk space for installation and backup.",
    "backup_failed": "Failed to create backup of original files.",
    "install_failed": "Failed to install patch files.",
    "already_patched": "The game appears to be already patched."
}

# Success messages
SUCCESS_MESSAGES = {
    "installation_complete": "Community fix installed successfully!",
    "backup_created": "Backup created successfully.",
    "files_installed": "Patch files installed successfully.",
    "compatibility_set": "Compatibility settings configured.",
    "briefings_removed": "Introduction briefing files removed.",
    "restore_complete": "Original files restored from backup."
}
