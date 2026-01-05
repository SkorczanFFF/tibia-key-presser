"""Main application window for the Tibia Key Presser."""
import tkinter as tk
from tkinter import ttk, messagebox

from src.ui.components.key_entry import KeyEntry
from src.core.key_presser import KeyPresser
from src.core.window_manager import TibiaWindowManager
from src.utils.constants import MAX_KEY_PAIRS
from src.utils.paths import find_icon_ico


class AppWindow:
    """Main application window for the Tibia Key Presser."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Tibia Key Presser")
        self.root.minsize(420, 120)
        self._set_window_icon()
        self._setup_styles()
        
        self.key_presser = KeyPresser(on_key_press=self._on_key_pressed)
        self._setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._update_window_title()
    
    def _setup_styles(self):
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
        
    def _set_window_icon(self):
        """Set the window icon."""
        icon_path = find_icon_ico()
        if icon_path:
            try:
                self.root.iconbitmap(default=icon_path)
            except Exception:
                pass
            
    def _setup_ui(self):
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
            fg="#ffffff", bg="#c0392b",
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
    
    def _add_key_entry(self):
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
    
    def _delete_key_entry(self, index):
        """Delete a key-delay entry."""
        if self.key_presser.running:
            messagebox.showwarning("Running", "Stop the presser before deleting keys.")
            return
            
        if len(self.key_entries) <= 1:
            return
            
        # Remove the entry
        self.key_entries[index].grid_remove()
        del self.key_entries[index]
        
        # Re-index remaining entries
        for i, entry in enumerate(self.key_entries):
            entry.update_index(i)
        
        self._update_delete_buttons()
        self._update_add_button_visibility()
    
    def _update_delete_buttons(self):
        """Update delete button states based on entry count."""
        single_entry = len(self.key_entries) == 1
        for entry in self.key_entries:
            if single_entry:
                entry.delete_button.state(["disabled"])
            else:
                entry.delete_button.state(["!disabled"])
    
    def _update_add_button_visibility(self):
        """Update Add Key button visibility."""
        if len(self.key_entries) >= MAX_KEY_PAIRS:
            self.add_button.pack_forget()
        else:
            # Pack before start_button to maintain left position
            self.add_button.pack(side=tk.LEFT, padx=(0, 10), before=self.start_button)
            
    def _update_window_title(self):
        """Update the window title with character name if connected."""
        _, _, character_name = TibiaWindowManager.connect_to_window()
        if character_name:
            self.root.title(f"Tibia Key Presser - {character_name}")
            
    def _on_key_waiting(self, is_waiting, source_entry=None):
        """Handle key waiting state change."""
        if is_waiting:
            # Stop waiting on all other entries first
            for entry in self.key_entries:
                if entry is not source_entry and entry.current_entry:
                    entry.cancel_waiting()
            self._show_info("⌨ Press a key to bind...")
        else:
            self._hide_status()
    
    def _handle_key_press(self, event):
        """Handle key press events for key binding."""
        for entry in self.key_entries:
            if entry.current_entry:
                entry.set_key(event.keysym)
                self._hide_status()
                break
    
    def _on_key_pressed(self, key):
        """Flash the key entry when the bot presses a key (called from background thread)."""
        self.root.after(0, lambda: self._flash_key_entry(key))
    
    def _flash_key_entry(self, key):
        """Flash the corresponding key entry."""
        for entry in self.key_entries:
            if entry.get_key() == key:
                entry.flash()
                break
    
    def _show_error(self, message):
        """Show error message with red styling."""
        self.status_label.config(text=message, bg="#c0392b", fg="#ffffff")
        self.status_label.pack(side=tk.LEFT)
    
    def _show_info(self, message):
        """Show info message with blue styling."""
        self.status_label.config(text=message, bg="#3498db", fg="#ffffff")
        self.status_label.pack(side=tk.LEFT)
    
    def _hide_status(self):
        """Hide the status message."""
        self.status_label.pack_forget()
    
    def start(self):
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
        else:
            messagebox.showinfo("Running", "Already running.")
    
    def stop(self):
        """Stop the key pressing."""
        self.key_presser.stop()
        self._toggle_buttons(running=False)
    
    def _toggle_buttons(self, running):
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
    
    def on_closing(self):
        """Handle window close."""
        if self.key_presser.running:
            self.key_presser.stop()
        self.root.destroy()
