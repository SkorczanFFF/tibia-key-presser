"""
Main application window for the Tibia Key Presser.
"""
import tkinter as tk
from tkinter import messagebox

from src.ui.components.key_entry import KeyEntry
from src.core.key_presser import KeyPresser
from src.core.window_manager import TibiaWindowManager
from src.utils.constants import MAX_KEY_PAIRS

class AppWindow:
    """Main application window for the Tibia Key Presser."""
    
    def __init__(self, root):
        """
        Initialize the application window.
        
        Args:
            root: The Tkinter root window
        """
        self.root = root
        self.root.title("Tibia Key Presser")
        
        # Core components
        self.key_presser = KeyPresser()
        
        # Setup UI components
        self._setup_ui()
        
        # Set up protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Try to connect to Tibia window and update title
        self._update_window_title()
        
    def _setup_ui(self):
        """Set up the UI components."""
        # Main frame for holding the input fields and buttons
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Frame for key and delay entries
        self.entries_frame = tk.Frame(self.main_frame)
        self.entries_frame.grid(row=1, column=0, columnspan=6, pady=5, sticky="ew")
        
        # Key entries
        self.key_entries = []
        self._add_key_entry()  # Add the first entry
        
        # Frame for buttons
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        # Button to add more key-delay pairs
        self.add_button = tk.Button(self.button_frame, text="Add Key", command=self._add_key_entry)
        self.add_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Buttons for starting and stopping
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start, bg="green", fg="white")
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop, bg="red", fg="white")
        
        # Place start/stop buttons
        self.start_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.stop_button.grid_remove()  # Initially hidden
        
        # Status label for showing messages
        self.status_label = tk.Label(self.button_frame, text="", fg="red")
        self.status_label.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        
        # Configure grid weights for resizing
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.entries_frame.grid_columnconfigure(1, weight=1)
        self.entries_frame.grid_columnconfigure(3, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        
        # Key binding for the whole application
        self.root.bind("<KeyPress>", self._handle_key_press)
    
    def _add_key_entry(self):
        """Add a new key-delay entry."""
        if len(self.key_entries) < MAX_KEY_PAIRS:
            index = len(self.key_entries)
            entry = KeyEntry(self.entries_frame, index, on_delete=self._delete_key_entry)
            self.key_entries.append(entry)
            
            # Disable the delete button if it's the only entry
            if len(self.key_entries) == 1:
                entry.delete_button.config(state="disabled")
            else:
                # Enable delete button for all entries
                for entry in self.key_entries:
                    entry.delete_button.config(state="normal")
            
            # Update the Add Key button visibility
            self._update_add_button_visibility()
    
    def _delete_key_entry(self, index):
        """
        Delete a key-delay entry.
        
        Args:
            index (int): Index of the entry to delete
        """
        if self.key_presser.running:
            messagebox.showwarning("Script Running", "Cannot delete while the script is running.")
            return
            
        if len(self.key_entries) > 1:  # Ensure at least one key-bind row remains
            # Remove the entry from the grid
            self.key_entries[index].grid_remove()
            
            # Remove from our list
            del self.key_entries[index]
            
            # Re-index the remaining entries
            for i, entry in enumerate(self.key_entries):
                entry.update_index(i)
                entry.key_label.grid(row=i, column=0)
                entry.key_entry.grid(row=i, column=1)
                entry.delay_label.grid(row=i, column=2)
                entry.delay_spinbox.grid(row=i, column=3)
                entry.reset_button.grid(row=i, column=4)
                entry.delete_button.grid(row=i, column=5)
                
            # Disable Delete button if there is only one key-delay pair left
            if len(self.key_entries) == 1:
                self.key_entries[0].delete_button.config(state="disabled")
                
            # Update Add Key button visibility
            self._update_add_button_visibility()
    
    def _update_add_button_visibility(self):
        """Update the visibility of the Add Key button based on the number of entries."""
        if len(self.key_entries) >= MAX_KEY_PAIRS:
            self.add_button.grid_forget()  # Hide the button
        else:
            self.add_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")  # Show the button
            
    def _update_window_title(self):
        """Update the window title with the character name if connected to Tibia."""
        _, _, character_name = TibiaWindowManager.connect_to_window()
        if character_name:
            self.root.title(f"Tibia Key Presser - {character_name}")
            
    def _handle_key_press(self, event):
        """Handle key press events for the entire application."""
        # Find the currently selected entry
        selected_entry = None
        for entry in self.key_entries:
            if entry.current_entry:
                selected_entry = entry
                break
                
        if selected_entry:
            selected_entry.set_key(event.keysym)
            self.status_label.config(text="")
    
    def start(self):
        """Start the key pressing."""
        # Collect key-delay pairs
        keys = []
        delays = []
        
        for entry in self.key_entries:
            key = entry.get_key()
            delay = entry.get_delay()
            
            if key and delay:
                keys.append(key)
                delays.append(float(delay))
        
        # Check if there's at least one valid key-delay pair
        if not keys:
            self.status_label.config(text="Please set at least one key and delay value.")
            return
        
        # Start the key presser
        if self.key_presser.start(keys, delays):
            self._toggle_buttons(running=True)
        else:
            messagebox.showinfo("Already Running", "The key presser is already running.")
    
    def stop(self):
        """Stop the key pressing."""
        self.key_presser.stop()
        self._toggle_buttons(running=False)
    
    def _toggle_buttons(self, running):
        """
        Toggle button states based on whether the script is running.
        
        Args:
            running (bool): Whether the script is running
        """
        if running:
            # Hide start button, show stop button
            self.start_button.grid_forget()
            self.stop_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            
            # Disable add key button
            self.add_button.config(state="disabled")
            
            # Disable all reset and delete buttons
            for entry in self.key_entries:
                entry.set_state("disabled")
        else:
            # Hide stop button, show start button
            self.stop_button.grid_forget()
            self.start_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            
            # Re-enable add key button
            self.add_button.config(state="normal")
            
            # Re-enable all reset and delete buttons
            for entry in self.key_entries:
                entry.set_state("normal")
                
            # Disable the delete button if it's the only entry
            if len(self.key_entries) == 1:
                self.key_entries[0].delete_button.config(state="disabled")
    
    def on_closing(self):
        """Handle the window close event."""
        if self.key_presser.running:
            self.key_presser.stop()  # Stop the key pressing threads
        self.root.destroy()  # Close the Tkinter window 