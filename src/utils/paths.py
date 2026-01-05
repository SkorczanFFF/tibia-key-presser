"""Resource path utilities for dev and PyInstaller environments."""
import os
import sys


def find_icon_ico():
    """Find .ico file for window icon. Returns absolute path or None."""
    # PyInstaller frozen exe - icon is in _MEIPASS root
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, 'tkp_icon.ico')
        if os.path.exists(path):
            return path
    
    # Development - icon is in icons/ folder
    path = os.path.join('icons', 'tkp_icon.ico')
    if os.path.exists(path):
        return os.path.abspath(path)
    
    return None
