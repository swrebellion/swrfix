"""
Star Wars: Rebellion Community Fix Installer
GUI implementation using tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
import webbrowser

from installer import RebellionFixInstaller
from config import VERSION, PATCH_FILES
from utils import is_admin, run_as_admin


class InstallerGUI:
    """Main GUI class for the installer"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.installer = RebellionFixInstaller()
        self.current_step = 0
        self.total_steps = 6  # Added shortcut modification step
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Setup main window properties"""
        self.root.title(f"Star Wars: Rebellion Community Fix Installer v{VERSION}")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # Set icon if available
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
    
    def create_widgets(self):
        """Create and layout GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Star Wars: Rebellion Community Fix Installer",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        version_label = ttk.Label(
            main_frame,
            text=f"Version {VERSION}",
            font=("Arial", 10)
        )
        version_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Game path frame
        path_frame = ttk.LabelFrame(main_frame, text="Game Installation", padding="10")
        path_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=60)
        self.path_entry.grid(row=0, column=0, padx=(0, 10))
        
        self.browse_button = ttk.Button(path_frame, text="Browse...", command=self.browse_for_game)
        self.browse_button.grid(row=0, column=1)
        
        self.detect_button = ttk.Button(path_frame, text="Auto-Detect", command=self.auto_detect_game)
        self.detect_button.grid(row=0, column=2, padx=(10, 0))
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Installation Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.backup_var = tk.BooleanVar(value=True)
        backup_check = ttk.Checkbutton(
            options_frame,
            text="Create backup of original files (recommended)",
            variable=self.backup_var
        )
        backup_check.grid(row=0, column=0, sticky=tk.W)
        
        self.compatibility_var = tk.BooleanVar(value=True)
        compatibility_check = ttk.Checkbutton(
            options_frame,
            text="Configure Windows XP compatibility mode (recommended)",
            variable=self.compatibility_var
        )
        compatibility_check.grid(row=1, column=0, sticky=tk.W)
        
        self.briefing_var = tk.BooleanVar(value=False)
        briefing_check = ttk.Checkbutton(
            options_frame,
            text="Remove introduction briefing files",
            variable=self.briefing_var
        )
        briefing_check.grid(row=2, column=0, sticky=tk.W)
        
        # Progress frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress_var = tk.StringVar(value="Ready to install")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            maximum=self.total_steps
        )
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        self.install_button = ttk.Button(
            buttons_frame,
            text="Install Community Fix",
            command=self.start_installation,
            style="Accent.TButton"
        )
        self.install_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.uninstall_button = ttk.Button(
            buttons_frame,
            text="Uninstall/Restore",
            command=self.start_uninstall
        )
        self.uninstall_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.log_button = ttk.Button(
            buttons_frame,
            text="View Log",
            command=self.view_log
        )
        self.log_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.exit_button = ttk.Button(
            buttons_frame,
            text="Exit",
            command=self.root.quit
        )
        self.exit_button.pack(side=tk.RIGHT)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        path_frame.columnconfigure(0, weight=1)
        progress_frame.columnconfigure(0, weight=1)
        
        # Auto-detect game on startup
        self.root.after(100, self.auto_detect_game)
    
    def browse_for_game(self):
        """Open file dialog to browse for game installation"""
        folder = filedialog.askdirectory(
            title="Select Star Wars: Rebellion Installation Folder",
            initialdir="C:\\Program Files (x86)"
        )
        
        if folder:
            if self.installer.validate_game_path(folder):
                self.path_var.set(folder)
                self.installer.game_path = folder
            else:
                messagebox.showerror(
                    "Invalid Game Path",
                    "The selected folder does not contain a valid Star Wars: Rebellion installation.\n\n"
                    "Please ensure REBEXE.exe is present in the selected folder."
                )
    
    def auto_detect_game(self):
        """Auto-detect game installation"""
        self.progress_var.set("Searching for game installation...")
        self.root.update()
        
        game_path = self.installer.find_game_installation()
        if game_path:
            self.path_var.set(game_path)
            self.installer.game_path = game_path
            self.progress_var.set(f"Game found: {Path(game_path).name}")
        else:
            self.progress_var.set("Game not found in common locations - please browse manually")
    
    def validate_installation(self) -> bool:
        """Validate installation before starting"""
        # Check game path
        if not self.installer.game_path or not self.installer.validate_game_path(self.installer.game_path):
            messagebox.showerror(
                "Invalid Game Path",
                "Please select a valid Star Wars: Rebellion installation folder."
            )
            return False
        
        # Check patch files
        if not self.installer.check_patch_files():
            messagebox.showerror(
                "Missing Patch Files",
                "Required patch files are missing. Please ensure the following files are in the same directory as this installer:\n\n" +
                "\n".join(f"• {f}" for f in PATCH_FILES)
            )
            return False
        
        # Check if already patched
        if self.installer.is_already_patched():
            result = messagebox.askyesno(
                "Already Patched",
                "The game appears to be already patched with version 1.02 or higher.\n\n"
                "Do you want to continue with the installation anyway?",
                icon="question"
            )
            if not result:
                return False
        
        # Warn about Steam version
        if self.installer.is_steam_version:
            result = messagebox.askyesno(
                "Steam Version Detected",
                "Steam version of the game detected.\n\n"
                "WARNING: Steam may verify and restore original files, overwriting this patch.\n"
                "Consider disabling automatic updates for this game in Steam.\n\n"
                "Do you want to continue with the installation?",
                icon="warning"
            )
            if not result:
                return False
        
        # Check permissions
        if not self.installer.check_permissions():
            if not is_admin():
                result = messagebox.askyesno(
                    "Administrative Rights Required",
                    "Administrative rights are required to install to this location.\n\n"
                    "Would you like to restart the installer as administrator?",
                    icon="warning"
                )
                if result:
                    run_as_admin()
                    self.root.quit()
                return False
            else:
                messagebox.showerror(
                    "Permission Error",
                    "Unable to write to the game directory. Please check folder permissions."
                )
                return False
        
        # Check if game is running
        if self.installer.is_game_running():
            messagebox.showerror(
                "Game Running",
                "Star Wars: Rebellion is currently running. Please close the game before installing the patch."
            )
            return False
        
        # Check disk space (need at least 50MB for backup and installation)
        free_space = self.installer.get_disk_space()
        if free_space < 50 * 1024 * 1024:  # 50MB
            messagebox.showerror(
                "Insufficient Disk Space",
                "Insufficient disk space for installation and backup.\n"
                f"At least 50MB is required."
            )
            return False
        
        return True
    
    def start_installation(self):
        """Start the installation process in a separate thread"""
        if not self.validate_installation():
            return
        
        # Disable buttons during installation
        self.install_button.config(state="disabled")
        self.uninstall_button.config(state="disabled")
        self.browse_button.config(state="disabled")
        self.detect_button.config(state="disabled")
        
        # Set installer options
        self.installer.skip_backup = not self.backup_var.get()
        self.installer.remove_briefings = self.briefing_var.get()
        
        # Start installation thread
        thread = threading.Thread(target=self.run_installation)
        thread.daemon = True
        thread.start()
    
    def run_installation(self):
        """Run installation process"""
        try:
            self.current_step = 0
            self.update_progress("Starting installation...", 0)
            
            # Step 1: Create backup
            if not self.installer.skip_backup:
                self.update_progress("Creating backup...", 1)
                if not self.installer.create_backup():
                    raise Exception("Failed to create backup")
            else:
                self.current_step += 1
            
            # Step 2: Install patch files
            self.update_progress("Installing patch files...", 2)
            if not self.installer.install_patch_files():
                raise Exception("Failed to install patch files")
            
            # Step 3: Configure compatibility
            if self.compatibility_var.get():
                self.update_progress("Configuring compatibility settings...", 3)
                self.installer.configure_compatibility()
            else:
                self.current_step += 1
            
            # Step 4: Modify shortcuts with -w flag (CRITICAL)
            self.update_progress("Modifying shortcuts with -w flag...", 4)
            self.installer.modify_shortcuts()
            
            # Step 5: Remove briefings
            if self.installer.remove_briefings:
                self.update_progress("Removing briefing files...", 5)
                self.installer.remove_intro_briefings()
            else:
                self.current_step += 1
            
            # Step 6: Complete
            self.update_progress("Installation completed!", 6)
            
            # Show completion dialog
            self.root.after(0, self.show_completion_dialog)
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error_dialog(str(e)))
        finally:
            # Re-enable buttons
            self.root.after(0, self.enable_buttons)
    
    def start_uninstall(self):
        """Start uninstallation process"""
        if not self.installer.game_path or not self.installer.validate_game_path(self.installer.game_path):
            messagebox.showerror(
                "Invalid Game Path",
                "Please select a valid Star Wars: Rebellion installation folder."
            )
            return
        
        backup_folders = self.installer.get_backup_folders()
        if not backup_folders:
            messagebox.showerror(
                "No Backup Found",
                "No backup folders found in the game directory.\n"
                "Cannot restore original files."
            )
            return
        
        result = messagebox.askyesno(
            "Confirm Uninstall",
            f"This will restore original game files from backup.\n\n"
            f"Backup folder: {backup_folders[0].name}\n\n"
            "Do you want to continue?",
            icon="question"
        )
        
        if result:
            if self.installer.restore_from_backup():
                messagebox.showinfo(
                    "Uninstall Complete",
                    "The community fix has been uninstalled and original files have been restored."
                )
            else:
                messagebox.showerror(
                    "Uninstall Failed",
                    "Failed to restore original files from backup."
                )
    
    def update_progress(self, message: str, step: int):
        """Update progress bar and message"""
        def update():
            self.progress_var.set(message)
            self.progress_bar.config(value=step)
            self.root.update()
        
        self.root.after(0, update)
    
    def show_completion_dialog(self):
        """Show installation completion dialog"""
        # Show multiplayer info first if requested
        from config import MULTIPLAYER_INFO
        messagebox.showinfo(
            "Multiplayer Port Information",
            MULTIPLAYER_INFO
        )
        
        # Show completion options
        result = messagebox.askyesnocancel(
            "Installation Complete",
            "Star Wars: Rebellion Community Fix has been installed successfully!\n\n"
            f"Modified {len(self.installer.shortcuts_modified)} shortcuts with -w flag.\n"
            f"Steam version detected: {'Yes' if self.installer.is_steam_version else 'No'}\n\n"
            "Would you like to:\n"
            "• Yes: Launch the game now\n"
            "• No: Open game folder\n"
            "• Cancel: Close installer",
            icon="info"
        )
        
        if result is True:  # Launch game
            self.launch_game()
        elif result is False:  # Open folder
            self.open_game_folder()
    
    def show_error_dialog(self, error_message: str):
        """Show error dialog"""
        messagebox.showerror(
            "Installation Failed",
            f"Installation failed with the following error:\n\n{error_message}\n\n"
            "Please check the log file for more details."
        )
    
    def enable_buttons(self):
        """Re-enable buttons after installation"""
        self.install_button.config(state="normal")
        self.uninstall_button.config(state="normal")
        self.browse_button.config(state="normal")
        self.detect_button.config(state="normal")
    
    def launch_game(self):
        """Launch the game"""
        if self.installer.game_path:
            exe_path = Path(self.installer.game_path) / "REBEXE.exe"
            if exe_path.exists():
                try:
                    import subprocess
                    subprocess.Popen([str(exe_path)], cwd=self.installer.game_path)
                except Exception as e:
                    messagebox.showerror(
                        "Launch Failed",
                        f"Failed to launch the game: {e}"
                    )
    
    def open_game_folder(self):
        """Open game folder in Windows Explorer"""
        if self.installer.game_path:
            try:
                import subprocess
                subprocess.Popen(['explorer', self.installer.game_path])
            except Exception as e:
                messagebox.showerror(
                    "Open Folder Failed",
                    f"Failed to open game folder: {e}"
                )
    
    def view_log(self):
        """Open log file in default text editor"""
        log_file = Path("rebellion_fix_install.log")
        if log_file.exists():
            try:
                import subprocess
                subprocess.Popen(['notepad', str(log_file)])
            except Exception as e:
                messagebox.showerror(
                    "Open Log Failed",
                    f"Failed to open log file: {e}"
                )
        else:
            messagebox.showinfo(
                "No Log File",
                "Log file not found."
            )
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()
