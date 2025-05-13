"""
Module for the KeyEntry component which represents a key-delay pair.
"""
import tkinter as tk

class KeyEntry:
    """A component representing a key-delay pair in the UI."""
    
    def __init__(self, parent, index, on_delete=None):
        """
        Initialize a KeyEntry component.
        
        Args:
            parent: Parent frame to place this component
            index (int): Index of this entry
            on_delete: Callback function for when the delete button is pressed
        """
        self.parent = parent
        self.index = index
        self.on_delete = on_delete
        self.current_entry = None
        
        # Key label
        self.key_label = tk.Label(parent, text=f"Key {index+1}:")
        self.key_label.grid(row=index, column=0, padx=10, pady=5, sticky="e")
        
        # Key entry
        self.key_entry = tk.Entry(parent)
        self.key_entry.grid(row=index, column=1, padx=10, pady=5, sticky="ew")
        self.key_entry.bind("<Button-1>", self.select_entry)
        
        # Delay label
        self.delay_label = tk.Label(parent, text=f"Delay {index+1} (seconds):")
        self.delay_label.grid(row=index, column=2, padx=10, pady=5, sticky="e")
        
        # Delay spinbox
        self.delay_spinbox = tk.Spinbox(parent, from_=0.0, to=10.0, increment=0.1, format="%.1f")
        self.delay_spinbox.grid(row=index, column=3, padx=10, pady=5, sticky="ew")
        
        # Reset button for key entry
        self.reset_button = tk.Button(parent, text="Reset", command=self.reset_key)
        self.reset_button.grid(row=index, column=4, padx=10, pady=5)
        
        # Delete button for key entry
        self.delete_button = tk.Button(parent, text="Delete", command=self.delete_key)
        self.delete_button.grid(row=index, column=5, padx=10, pady=5)
    
    def select_entry(self, event):
        """Set this entry as the currently selected key entry."""
        self.current_entry = event.widget
        self.key_entry.config(bg="yellow")  # Highlight selected entry
        return "break"  # Prevent default handling
        
    def set_key(self, key):
        """Set the key value in the entry field."""
        if self.current_entry:
            self.current_entry.config(bg="white")
            self.current_entry.delete(0, tk.END)
            self.current_entry.insert(0, key)
            self.current_entry = None
            
    def reset_key(self):
        """Reset the key entry."""
        self.key_entry.delete(0, tk.END)
        
    def delete_key(self):
        """Call the delete callback if provided."""
        if self.on_delete:
            self.on_delete(self.index)
            
    def get_key(self):
        """Get the current key value."""
        return self.key_entry.get()
        
    def get_delay(self):
        """Get the current delay value."""
        return self.delay_spinbox.get()
        
    def update_index(self, new_index):
        """Update the index and labels of this entry."""
        self.index = new_index
        self.key_label.config(text=f"Key {new_index+1}:")
        self.delay_label.config(text=f"Delay {new_index+1} (seconds):")
        
    def grid_remove(self):
        """Remove all widgets from the grid."""
        self.key_label.grid_forget()
        self.key_entry.grid_forget()
        self.delay_label.grid_forget()
        self.delay_spinbox.grid_forget()
        self.reset_button.grid_forget()
        self.delete_button.grid_forget()
        
    def set_state(self, state):
        """
        Set the state of the buttons.
        
        Args:
            state (str): 'normal' or 'disabled'
        """
        self.reset_button.config(state=state)
        self.delete_button.config(state=state) 