"""
Main entry point for the Tibia Key Presser application.
"""
# Prevent unnecessary module imports for PyInstaller
import sys
import os

# Create fake module to exclude libraries from PyInstaller
class PyInstallerImportBlocker:
    """Prevent PyInstaller from including unnecessary modules."""
    def __init__(self, *args):
        self.module_names = args

    def find_module(self, fullname, path=None):
        if fullname in self.module_names:
            return self
        return None

    def load_module(self, fullname):
        return sys.modules.get(fullname)

# Only add the blocker if not running from PyInstaller
if not getattr(sys, 'frozen', False):
    sys.meta_path.append(PyInstallerImportBlocker('numpy', 'pandas', 'matplotlib', 'scipy', 'PyQt5', 'PySide2', 'wx'))

import tkinter as tk
from src.ui.app_window import AppWindow
from src.ui.loading_screen import LoadingScreen

def main():
    """Launch the Tibia Key Presser application."""
    # Show loading screen first
    loading_screen = LoadingScreen()
    loading_screen.show()
    
    # Create main application
    root = tk.Tk()
    app = AppWindow(root, loading_screen)
    
    # Hide loading screen immediately when main window is ready
    loading_screen.hide()
    
    # Start the main loop
    root.mainloop()
    
    # Clean up loading screen
    loading_screen.destroy()

if __name__ == "__main__":
    main() 