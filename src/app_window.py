"""Main application window for the Tibia Key Presser."""
from __future__ import annotations

import os
import sys
import tkinter as tk
from tkinter import ttk

from src.key_entry import KeyEntry
from src.key_presser import KeyPresser
from src.window_manager import connect_to_window

MAX_KEY_PAIRS = 8


COLOR_ERROR = "#c0392b"
COLOR_INFO = "#3498db"
COLOR_STATUS_FG = "#ffffff"


class AppWindow:
    """Main application window for the Tibia Key Presser."""

    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.root.title("Tibia Key Presser")
        self.root.minsize(420, 120)
        self._set_window_icon()
        self._setup_styles()
        
        self.key_presser = KeyPresser(
            on_key_press=self._on_key_pressed,
            on_connection_lost=self._on_connection_lost
        )
        self._setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._poll_window_title()
    
    def _setup_styles(self) -> None:
        """Configure ttk styles for modern look."""
        style = ttk.Style()
        
        # Use clam theme as base (more customizable)
        style.theme_use('clam')
        
        # Configure colors
        bg_color = "#f5f5f5"
        accent_color = "#2d5a27"  # Dark green (Tibia theme)
        accent_hover = "#3d7a37"
        danger_color = "#c0392b"
        danger_hover = "#e74c3c"
        
        self.root.configure(bg=bg_color)
        
        # Frame styles
        style.configure("TFrame", background=bg_color)
        style.configure("Card.TFrame", background="white", relief="flat")
        
        # Label styles
        style.configure("TLabel", background=bg_color, font=("Segoe UI", 9))
        
        # Entry styles
        style.configure("TEntry", padding=5)
        style.map("TEntry",
            fieldbackground=[("focus", "#fff3cd"), ("!focus", "white")],
        )
        
        # Spinbox styles
        style.configure("TSpinbox", padding=5, arrowsize=12)
        
        # Button styles
        style.configure("TButton", padding=(10, 5), font=("Segoe UI", 9))
        
        # Start button (green)
        style.configure("Start.TButton", 
            background=accent_color, 
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )
        style.map("Start.TButton",
            background=[("active", accent_hover), ("disabled", "#cccccc")]
        )
        
        # Stop button (red)
        style.configure("Stop.TButton",
            background=danger_color,
            foreground="white", 
            font=("Segoe UI", 10, "bold")
        )
        style.map("Stop.TButton",
            background=[("active", danger_hover)]
        )
        
        # Add button
        style.configure("Add.TButton", font=("Segoe UI", 9))
        
    def _set_window_icon(self) -> None:
        """Set the window icon."""
        icon_path = None
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            path = os.path.join(sys._MEIPASS, 'tkp_icon.ico')
            if os.path.exists(path):
                icon_path = path
        else:
            path = os.path.join('icons', 'tkp_icon.ico')
            if os.path.exists(path):
                icon_path = os.path.abspath(path)

        if icon_path:
            try:
                self.root.iconbitmap(default=icon_path)
            except tk.TclError:
                pass
            
    def _setup_ui(self) -> None:
        """Set up the UI components."""
        # Main container with padding
        self.main_frame = ttk.Frame(self.root, padding=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Entries container
        self.entries_frame = ttk.Frame(self.main_frame)
        self.entries_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Button bar
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X)
        
        # Status/info label on the left
        self.status_label = tk.Label(
            self.button_frame, text="",
            fg=COLOR_STATUS_FG, bg=COLOR_ERROR,
            font=("Segoe UI", 9, "bold"),
            padx=8, pady=2
        )
        # Don't pack initially - only show when there's a message
        
        # Right side buttons
        right_buttons = ttk.Frame(self.button_frame)
        right_buttons.pack(side=tk.RIGHT)
        
        self.add_button = ttk.Button(
            right_buttons, text="+ Add Key", 
            command=self._add_key_entry,
            style="Add.TButton"
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Start/Stop buttons
        self.start_button = ttk.Button(
            right_buttons, text="▶ Start",
            command=self.start,
            style="Start.TButton",
            width=12
        )
        self.start_button.pack(side=tk.LEFT)
        
        self.stop_button = ttk.Button(
            right_buttons, text="■ Stop",
            command=self.stop,
            style="Stop.TButton",
            width=12
        )
        # Don't pack stop button initially
        
        # Key binding for the whole application
        self.root.bind("<KeyPress>", self._handle_key_press)
        
        # Key entries list
        self.key_entries = []
        self._add_key_entry()
    
    def _add_key_entry(self) -> None:
        """Add a new key-delay entry."""
        if len(self.key_entries) >= MAX_KEY_PAIRS:
            return
            
        index = len(self.key_entries)
        entry = KeyEntry(
            self.entries_frame, index, 
            on_delete=self._delete_key_entry,
            on_waiting=self._on_key_waiting
        )
        self.key_entries.append(entry)
        
        # Update delete button states
        self._update_delete_buttons()
        self._update_add_button_visibility()
    
    def _delete_key_entry(self, entry: KeyEntry) -> None:
        """Delete a key-delay entry."""
        if len(self.key_entries) <= 1:
            return

        entry.destroy()
        self.key_entries.remove(entry)

        # Re-index remaining entries
        for i, e in enumerate(self.key_entries):
            e.update_index(i)

        self._update_delete_buttons()
        self._update_add_button_visibility()
    
    def _update_delete_buttons(self) -> None:
        """Update delete button states based on entry count."""
        single_entry = len(self.key_entries) == 1
        for entry in self.key_entries:
            if single_entry:
                entry.delete_button.state(["disabled"])
            else:
                entry.delete_button.state(["!disabled"])
    
    def _update_add_button_visibility(self) -> None:
        """Update Add Key button visibility."""
        if len(self.key_entries) >= MAX_KEY_PAIRS:
            self.add_button.pack_forget()
        else:
            # Pack before start_button to maintain left position
            self.add_button.pack(side=tk.LEFT, padx=(0, 10), before=self.start_button)
            
    def _poll_window_title(self) -> None:
        """Periodically update the window title with character name."""
        _, character_name = connect_to_window()
        if character_name:
            self.root.title(f"Tibia Key Presser - {character_name}")
        else:
            self.root.title("Tibia Key Presser")
        self.root.after(5000, self._poll_window_title)
            
    def _on_key_waiting(self, is_waiting: bool, source_entry: KeyEntry | None = None) -> None:
        """Handle key waiting state change."""
        if is_waiting:
            # Stop waiting on all other entries first
            for entry in self.key_entries:
                if entry is not source_entry and entry.current_entry:
                    entry.cancel_waiting()
            self._show_info("⌨ Press a key to bind...")
        else:
            self._hide_status()
    
    def _handle_key_press(self, event: tk.Event) -> None:
        """Handle key press events for key binding."""
        for entry in self.key_entries:
            if entry.current_entry:
                entry.set_key(event.keysym)
                self._hide_status()
                break
    
    def _on_connection_lost(self) -> None:
        """Handle Tibia disconnection (called from background thread)."""
        self.root.after(0, self._handle_connection_lost)

    def _handle_connection_lost(self) -> None:
        """Reset UI to idle state and show disconnect message."""
        self._toggle_buttons(running=False)
        self._show_error("Pick character first")

    def _on_key_pressed(self, key: str) -> None:
        """Flash the key entry when the bot presses a key (called from background thread)."""
        self.root.after(0, lambda: self._flash_key_entry(key))

    def _flash_key_entry(self, key: str) -> None:
        """Flash the corresponding key entry."""
        for entry in self.key_entries:
            if entry.get_key() == key:
                entry.flash()
                break
    
    def _show_error(self, message: str) -> None:
        """Show error message with red styling."""
        self.status_label.config(text=message, bg=COLOR_ERROR, fg=COLOR_STATUS_FG)
        self.status_label.pack(side=tk.LEFT)

    def _show_info(self, message: str) -> None:
        """Show info message with blue styling."""
        self.status_label.config(text=message, bg=COLOR_INFO, fg=COLOR_STATUS_FG)
        self.status_label.pack(side=tk.LEFT)

    def _hide_status(self) -> None:
        """Hide the status message."""
        self.status_label.pack_forget()
    
    def start(self) -> None:
        """Start the key pressing."""
        keys = []
        delays = []
        
        # Check for empty key entries and highlight them
        has_empty = False
        for entry in self.key_entries:
            key = entry.get_key()
            delay = entry.get_delay()
            if key and delay:
                keys.append(key)
                delays.append(float(delay))
                entry.clear_error()
            elif not key:
                entry.show_error()
                has_empty = True
        
        if not keys or has_empty:
            self._show_error("⚠ Bind at least one key")
            return
        
        if self.key_presser.start(keys, delays):
            self._toggle_buttons(running=True)
            self._hide_status()
    
    def stop(self) -> None:
        """Stop the key pressing."""
        self.key_presser.stop()
        self._toggle_buttons(running=False)

    def _toggle_buttons(self, running: bool) -> None:
        """Toggle UI state based on running status."""
        if running:
            self.start_button.pack_forget()
            self.stop_button.pack(side=tk.LEFT)
            self.add_button.state(["disabled"])
            for entry in self.key_entries:
                entry.set_state("disabled")
        else:
            self.stop_button.pack_forget()
            self.start_button.pack(side=tk.LEFT)
            self.add_button.state(["!disabled"])
            for entry in self.key_entries:
                entry.set_state("normal")
            self._update_delete_buttons()
    
    def on_closing(self) -> None:
        """Handle window close."""
        if self.key_presser.running:
            self.key_presser.stop()
        self.root.destroy()
