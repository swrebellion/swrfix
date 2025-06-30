#!/usr/bin/env python3
"""
Star Wars: Rebellion Community Fix Installer
Main entry point for the application
"""

import sys
import argparse
import os
from pathlib import Path

from gui import InstallerGUI
from installer import RebellionFixInstaller
from config import VERSION, PATCH_FILES


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description=f'Star Wars: Rebellion Community Fix Installer v{VERSION}',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--silent', 
        action='store_true',
        help='Install with defaults, no prompts'
    )
    
    parser.add_argument(
        '--path',
        type=str,
        help='Specify game installation path'
    )
    
    parser.add_argument(
        '--nobriefing',
        action='store_true',
        help='Remove briefing files automatically'
    )
    
    parser.add_argument(
        '--nobackup',
        action='store_true',
        help='Skip backup creation'
    )
    
    parser.add_argument(
        '--uninstall',
        action='store_true',
        help='Uninstall patch and restore from backup'
    )
    
    return parser.parse_args()


def run_silent_install(args):
    """Run silent installation with command line arguments"""
    installer = RebellionFixInstaller()
    
    try:
        # Set options based on arguments
        installer.skip_backup = args.nobackup
        installer.remove_briefings = args.nobriefing
        
        # Find or set game path
        if args.path:
            if not installer.validate_game_path(args.path):
                print(f"Error: Invalid game path: {args.path}")
                return False
            installer.game_path = args.path
        else:
            game_path = installer.find_game_installation()
            if not game_path:
                print("Error: Could not find Star Wars: Rebellion installation")
                return False
            installer.game_path = game_path
        
        print(f"Installing to: {installer.game_path}")
        
        # Check for patch files
        if not installer.check_patch_files():
            print("Error: Patch files not found. Please ensure patch files are in the same directory as this installer.")
            return False
        
        # Run installation steps
        if not args.nobackup:
            print("Creating backup...")
            if not installer.create_backup():
                print("Error: Failed to create backup")
                return False
        
        print("Installing patch files...")
        if not installer.install_patch_files():
            print("Error: Failed to install patch files")
            return False
        
        print("Configuring compatibility settings...")
        installer.configure_compatibility()
        
        if args.nobriefing:
            print("Removing briefing files...")
            installer.remove_intro_briefings()
        
        print("Installation completed successfully!")
        return True
        
    except Exception as e:
        print(f"Installation failed: {str(e)}")
        return False


def run_uninstall(args):
    """Run uninstallation process"""
    installer = RebellionFixInstaller()
    
    try:
        # Find game path
        if args.path:
            if not installer.validate_game_path(args.path):
                print(f"Error: Invalid game path: {args.path}")
                return False
            installer.game_path = args.path
        else:
            game_path = installer.find_game_installation()
            if not game_path:
                print("Error: Could not find Star Wars: Rebellion installation")
                return False
            installer.game_path = game_path
        
        print(f"Uninstalling from: {installer.game_path}")
        
        if installer.restore_from_backup():
            print("Patch uninstalled successfully!")
            return True
        else:
            print("Error: Failed to restore from backup")
            return False
            
    except Exception as e:
        print(f"Uninstallation failed: {str(e)}")
        return False


def main():
    """Main application entry point"""
    # Check if running on Windows
    if sys.platform != 'win32':
        print("Note: This installer is designed for Windows. Running in demo mode on Linux.")
        print("Some features will be simulated for demonstration purposes.")
    
    args = parse_arguments()
    
    # Handle uninstall
    if args.uninstall:
        success = run_uninstall(args)
        sys.exit(0 if success else 1)
    
    # Handle silent install
    if args.silent:
        success = run_silent_install(args)
        sys.exit(0 if success else 1)
    
    # Run GUI application
    try:
        app = InstallerGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start GUI: {str(e)}")
        print("Try running with --help for command line options")
        sys.exit(1)


if __name__ == '__main__':
    main()
