"""
Star Wars: Rebellion Community Fix Installer
Utility functions
"""

import os
import sys
import logging
import subprocess
from pathlib import Path

# Windows-only imports
if sys.platform == 'win32':
    try:
        import ctypes
    except ImportError:
        ctypes = None
else:
    ctypes = None


def setup_logging() -> logging.Logger:
    """Setup logging configuration"""
    logger = logging.getLogger('rebellion_installer')
    logger.setLevel(logging.INFO)
    
    # Create file handler
    handler = logging.FileHandler('rebellion_fix_install.log', encoding='utf-8')
    handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger


def is_admin() -> bool:
    """Check if running with administrator privileges"""
    if sys.platform != 'win32' or ctypes is None:
        return True  # Assume we have permissions on non-Windows
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except:
        return False


def run_as_admin():
    """Restart the application with administrator privileges"""
    if sys.platform != 'win32' or ctypes is None:
        print("Administrator elevation not available on this platform")
        return
        
    try:
        if is_admin():
            return
        
        # Get current script path
        script_path = sys.executable if getattr(sys, 'frozen', False) else __file__
        
        # Run as administrator
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            script_path,
            " ".join(sys.argv[1:]),
            None,
            1
        )
    except Exception as e:
        print(f"Failed to run as administrator: {e}")


def get_file_version(file_path: str) -> str:
    """Get file version from Windows executable"""
    if sys.platform != 'win32':
        # On non-Windows, assume patched version for demo purposes
        return "1.02" if "REBEXE" in file_path else "1.0"
    
    try:
        import win32api
        info = win32api.GetFileVersionInfo(file_path, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}"
        return version
    except:
        return ""


def calculate_file_hash(file_path: str, algorithm: str = 'md5') -> str:
    """Calculate hash of a file"""
    import hashlib
    
    hash_algo = getattr(hashlib, algorithm)()
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_algo.update(chunk)
    
    return hash_algo.hexdigest()


def check_disk_space(path: str, required_bytes: int) -> bool:
    """Check if enough disk space is available"""
    try:
        import shutil
        free_bytes = shutil.disk_usage(path).free
        return free_bytes >= required_bytes
    except:
        return False


def kill_process(process_name: str) -> bool:
    """Attempt to kill a process by name"""
    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", process_name],
            capture_output=True,
            check=True
        )
        return True
    except:
        return False


def create_shortcut(target_path: str, shortcut_path: str, arguments: str = "", 
                   working_directory: str = "", description: str = ""):
    """Create a Windows shortcut"""
    if sys.platform != 'win32':
        print(f"Shortcut creation not available on {sys.platform}")
        return False
        
    try:
        import win32com.client
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        shortcut.Arguments = arguments
        shortcut.WorkingDirectory = working_directory
        shortcut.Description = description
        shortcut.save()
        return True
    except:
        return False


def find_shortcuts(target_exe: str) -> list:
    """Find shortcuts pointing to a specific executable"""
    if sys.platform != 'win32':
        return []
        
    shortcuts = []
    
    # Search common locations
    search_paths = [
        Path.home() / "Desktop",
        Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs",
        Path("C:/ProgramData/Microsoft/Windows/Start Menu/Programs")
    ]
    
    for search_path in search_paths:
        if search_path.exists():
            for shortcut_file in search_path.rglob("*.lnk"):
                try:
                    # Check if shortcut points to our target
                    import win32com.client
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(str(shortcut_file))
                    
                    if shortcut.Targetpath.lower() == target_exe.lower():
                        shortcuts.append(shortcut_file)
                except:
                    continue
    
    return shortcuts


def modify_shortcut_arguments(shortcut_path: str, new_arguments: str) -> bool:
    """Modify arguments of an existing shortcut"""
    if sys.platform != 'win32':
        return False
        
    try:
        import win32com.client
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Arguments = new_arguments
        shortcut.save()
        return True
    except:
        return False


def get_windows_version() -> str:
    """Get Windows version information"""
    try:
        import platform
        return platform.platform()
    except:
        return "Unknown"


def is_process_running(process_name: str) -> bool:
    """Check if a process is currently running"""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return process_name.lower() in result.stdout.lower()
    except:
        return False
