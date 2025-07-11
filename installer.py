"""
Star Wars: Rebellion Community Fix Installer
Core installation logic

Contributors:
- TruthRealm: Creator of the Star Wars: Rebellion Community Fix v2.63.1.0 patches
- Stratus (via Replit Agent AI / Claude Sonnet 4): Creator of this installer application
"""

import os
import shutil
import subprocess
import hashlib
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

from config import COMMON_PATHS, PATCH_FILES, BACKUP_FILES, VERSION
from utils import setup_logging, is_admin, run_as_admin, get_file_version, find_shortcuts, modify_shortcut_arguments, create_shortcut

# Windows-only imports
if sys.platform == 'win32':
    try:
        import winreg
    except ImportError:
        winreg = None
else:
    winreg = None


class RebellionFixInstaller:
    """Main installer class for Star Wars: Rebellion Community Fix"""
    
    def __init__(self):
        self.game_path: Optional[str] = None
        self.backup_path: Optional[str] = None
        self.skip_backup: bool = False
        self.remove_briefings: bool = False
        self.shortcuts_modified: List[str] = []
        self.is_steam_version: bool = False
        self.logger = setup_logging()
        
    def find_game_installation(self) -> Optional[str]:
        """
        Find Star Wars: Rebellion installation in common paths
        Returns path if found, None otherwise
        """
        self.logger.info("Searching for game installation...")
        
        for path in COMMON_PATHS:
            full_path = Path(path)
            exe_path = full_path / "REBEXE.exe"
            
            if exe_path.exists():
                self.logger.info(f"Found game at: {full_path}")
                return str(full_path)
        
        self.logger.info("Game not found in common paths")
        return None
    
    def validate_game_path(self, path: str) -> bool:
        """Validate that the given path contains a valid game installation"""
        game_path = Path(path)
        exe_path = game_path / "REBEXE.exe"
        
        if not exe_path.exists():
            self.logger.error(f"REBEXE.exe not found in {path}")
            return False
        
        self.logger.info(f"Valid game installation found at: {path}")
        
        # Check if this is a Steam installation
        if "steam" in path.lower():
            self.is_steam_version = True
            self.logger.info("Steam version detected")
        
        return True
    
    def check_patch_files(self) -> bool:
        """Check if all required patch files are available"""
        installer_dir = Path(__file__).parent
        
        # Check in installer directory first
        for filename in PATCH_FILES:
            file_path = installer_dir / filename
            if file_path.exists():
                continue
            
            # Check in attached_assets directory
            assets_path = installer_dir / "attached_assets" / filename
            if filename == "REBEXE.exe":
                assets_path = installer_dir / "attached_assets" / "REBEXE_1751323218170.EXE"
            elif filename == "D3Dlmm.dll":
                assets_path = installer_dir / "attached_assets" / "D3DImm_1751323218171.dll"
            elif filename == "DDraw.dll":
                assets_path = installer_dir / "attached_assets" / "DDraw_1751323218169.dll"
            elif filename == "d3drm.dll":
                assets_path = installer_dir / "attached_assets" / "d3drm_1751323218167.dll"
            
            if not assets_path.exists():
                self.logger.error(f"Patch file not found: {filename}")
                return False
        
        self.logger.info("All patch files found")
        return True
    
    def is_already_patched(self) -> bool:
        """Check if the game is already patched by checking REBEXE.exe version"""
        if not self.game_path:
            return False
        
        exe_path = Path(self.game_path) / "REBEXE.exe"
        if not exe_path.exists():
            return False
        
        try:
            version = get_file_version(str(exe_path))
            # Check if version is 1.02 or higher (patched version)
            if version and version >= "1.02":
                self.logger.info("Game appears to be already patched")
                return True
        except Exception as e:
            self.logger.warning(f"Could not check game version: {e}")
        
        return False
    
    def get_backup_folders(self) -> List[Path]:
        """Get list of existing backup folders"""
        if not self.game_path:
            return []
        
        game_dir = Path(self.game_path)
        backup_folders = []
        
        for item in game_dir.iterdir():
            if item.is_dir() and item.name.startswith("Backup_"):
                backup_folders.append(item)
        
        return sorted(backup_folders, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def create_backup(self) -> bool:
        """Create backup of original game files"""
        if not self.game_path:
            self.logger.error("Game path not set")
            return False
        
        game_dir = Path(self.game_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = game_dir / f"Backup_{timestamp}"
        
        try:
            backup_dir.mkdir(exist_ok=True)
            self.backup_path = str(backup_dir)
            
            backed_up_files = []
            for filename in BACKUP_FILES:
                source_file = game_dir / filename
                if source_file.exists():
                    dest_file = backup_dir / filename
                    shutil.copy2(source_file, dest_file)
                    backed_up_files.append(filename)
                    self.logger.info(f"Backed up: {filename}")
            
            # Create backup log
            log_file = backup_dir / "backup_log.txt"
            with open(log_file, 'w') as f:
                f.write(f"Star Wars: Rebellion Community Fix Backup\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Installer Version: {VERSION}\n\n")
                f.write("Backed up files:\n")
                for filename in backed_up_files:
                    f.write(f"- {filename}\n")
            
            self.logger.info(f"Backup created successfully at: {backup_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return False
    
    def install_patch_files(self) -> bool:
        """Install patch files to game directory"""
        if not self.game_path:
            self.logger.error("Game path not set")
            return False
        
        if not self.check_patch_files():
            return False
        
        game_dir = Path(self.game_path)
        installer_dir = Path(__file__).parent
        
        try:
            for filename in PATCH_FILES:
                # Try installer directory first
                source_file = installer_dir / filename
                
                # If not found, check attached_assets with renamed files
                if not source_file.exists():
                    if filename == "REBEXE.exe":
                        source_file = installer_dir / "attached_assets" / "REBEXE_1751323218170.EXE"
                    elif filename == "D3Dlmm.dll":
                        source_file = installer_dir / "attached_assets" / "D3DImm_1751323218171.dll"
                    elif filename == "DDraw.dll":
                        source_file = installer_dir / "attached_assets" / "DDraw_1751323218169.dll"
                    elif filename == "d3drm.dll":
                        source_file = installer_dir / "attached_assets" / "d3drm_1751323218167.dll"
                
                if not source_file.exists():
                    raise Exception(f"Source file not found: {filename}")
                
                dest_file = game_dir / filename
                
                # Copy file
                shutil.copy2(source_file, dest_file)
                
                # Verify copy
                if not dest_file.exists():
                    raise Exception(f"Failed to copy {filename}")
                
                self.logger.info(f"Installed: {filename}")
            
            # Verify installation by checking REBEXE.exe version
            if self.is_already_patched():
                self.logger.info("Patch installation verified successfully")
                return True
            else:
                self.logger.warning("Patch installation could not be verified")
                return True  # Continue anyway, version check might fail for various reasons
                
        except Exception as e:
            self.logger.error(f"Failed to install patch files: {e}")
            return False
    
    def modify_shortcuts(self) -> bool:
        """Find and modify existing shortcuts to add -w flag"""
        if not self.game_path:
            return False
        
        exe_path = Path(self.game_path) / "REBEXE.exe"
        if not exe_path.exists():
            return False
        
        try:
            # Find existing shortcuts
            shortcuts = find_shortcuts(str(exe_path))
            
            for shortcut_path in shortcuts:
                try:
                    # Modify shortcut to add -w flag
                    if modify_shortcut_arguments(str(shortcut_path), "-w"):
                        self.shortcuts_modified.append(str(shortcut_path))
                        self.logger.info(f"Modified shortcut: {shortcut_path}")
                    else:
                        self.logger.warning(f"Failed to modify shortcut: {shortcut_path}")
                except Exception as e:
                    self.logger.warning(f"Error modifying shortcut {shortcut_path}: {e}")
            
            # Create desktop shortcut if none exist
            if not shortcuts:
                desktop_path = Path.home() / "Desktop" / "Star Wars Rebellion.lnk"
                if create_shortcut(
                    str(exe_path),
                    str(desktop_path),
                    arguments="-w",
                    working_directory=str(self.game_path),
                    description="Star Wars: Rebellion with Community Fix"
                ):
                    self.shortcuts_modified.append(str(desktop_path))
                    self.logger.info(f"Created desktop shortcut with -w flag")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to modify shortcuts: {e}")
            return False
    
    def check_existing_backups(self) -> List[str]:
        """Check for existing backup folders and return their names"""
        if not self.game_path:
            return []
        
        game_dir = Path(self.game_path)
        backups = []
        
        for item in game_dir.iterdir():
            if item.is_dir() and item.name.startswith("Backup_"):
                backups.append(item.name)
        
        return sorted(backups, reverse=True)  # Most recent first
    
    def configure_compatibility(self) -> bool:
        """Configure Windows compatibility settings for REBEXE.exe"""
        if not self.game_path:
            return False
        
        exe_path = Path(self.game_path) / "REBEXE.exe"
        if not exe_path.exists():
            return False
        
        # Only run on Windows with winreg available
        if sys.platform != 'win32' or winreg is None:
            self.logger.info("Compatibility settings skipped (not Windows or winreg unavailable)")
            return True
        
        try:
            # Registry path for compatibility settings
            reg_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
            
            # Import winreg constants
            from winreg import CreateKey, HKEY_CURRENT_USER, SetValueEx, REG_SZ
            
            # Open or create registry key
            with CreateKey(HKEY_CURRENT_USER, reg_path) as key:
                # Set compatibility mode and run as administrator
                compatibility_flags = "WINXPSP3 RUNASADMIN"
                SetValueEx(key, str(exe_path), 0, REG_SZ, compatibility_flags)
            
            self.logger.info("Compatibility settings configured")
            return True
            
        except Exception as e:
            self.logger.warning(f"Failed to configure compatibility settings: {e}")
            return False
    
    def remove_intro_briefings(self) -> bool:
        """Remove introduction briefing files"""
        if not self.game_path:
            return False
        
        game_dir = Path(self.game_path)
        briefing_files = ["ALBRIEF.dll", "EMBRIEF.dll"]
        removed_files = []
        
        try:
            for filename in briefing_files:
                file_path = game_dir / filename
                if file_path.exists():
                    backup_name = f"{filename}.backup"
                    backup_path = game_dir / backup_name
                    
                    # Rename to .backup instead of deleting
                    file_path.rename(backup_path)
                    removed_files.append(filename)
                    self.logger.info(f"Removed briefing file: {filename}")
            
            if removed_files:
                self.logger.info(f"Removed {len(removed_files)} briefing files")
            else:
                self.logger.info("No briefing files found to remove")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to remove briefing files: {e}")
            return False
    
    def restore_from_backup(self) -> bool:
        """Restore game files from the most recent backup"""
        if not self.game_path:
            self.logger.error("Game path not set")
            return False
        
        backup_folders = self.get_backup_folders()
        if not backup_folders:
            self.logger.error("No backup folders found")
            return False
        
        # Use most recent backup
        backup_dir = backup_folders[0]
        game_dir = Path(self.game_path)
        
        try:
            restored_files = []
            for filename in BACKUP_FILES:
                backup_file = backup_dir / filename
                if backup_file.exists():
                    dest_file = game_dir / filename
                    shutil.copy2(backup_file, dest_file)
                    restored_files.append(filename)
                    self.logger.info(f"Restored: {filename}")
            
            # Restore briefing files if they were backed up
            for filename in ["ALBRIEF.dll", "EMBRIEF.dll"]:
                backup_file = backup_dir / filename
                if backup_file.exists():
                    dest_file = game_dir / filename
                    shutil.copy2(backup_file, dest_file)
                    restored_files.append(filename)
                    self.logger.info(f"Restored: {filename}")
                
                # Remove .backup version if it exists
                backup_version = game_dir / f"{filename}.backup"
                if backup_version.exists():
                    backup_version.unlink()
            
            self.logger.info(f"Restored {len(restored_files)} files from backup")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore from backup: {e}")
            return False
    
    def check_permissions(self) -> bool:
        """Check if we have write permissions to the game directory"""
        if not self.game_path:
            return False
        
        game_dir = Path(self.game_path)
        
        try:
            # Try to create a temporary file
            test_file = game_dir / "write_test.tmp"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except Exception:
            return False
    
    def get_disk_space(self) -> int:
        """Get available disk space in game directory (in bytes)"""
        if not self.game_path:
            return 0
        
        try:
            return shutil.disk_usage(self.game_path).free
        except Exception:
            return 0
    
    def is_game_running(self) -> bool:
        """Check if the game is currently running"""
        try:
            # Use tasklist to check for running processes
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq REBEXE.exe"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return "REBEXE.exe" in result.stdout
        except Exception:
            return False
