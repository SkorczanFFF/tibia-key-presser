"""Main entry point for the Tibia Key Presser application."""
from __future__ import annotations

import tkinter as tk
from src.app_window import AppWindow


def main() -> None:
    """Launch the Tibia Key Presser application."""
    root = tk.Tk()
    AppWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
