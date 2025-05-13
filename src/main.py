"""
Main entry point for the Tibia Key Presser application.
"""
import tkinter as tk
from src.ui.app_window import AppWindow

def main():
    """Launch the Tibia Key Presser application."""
    root = tk.Tk()
    app = AppWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main() 