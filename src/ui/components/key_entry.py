"""KeyEntry component - a key-delay pair row."""
import tkinter as tk
from tkinter import ttk


class KeyEntry:
    """A component representing a key-delay pair in the UI."""
    
    _styles_configured = False
    
    # Animation colors for pulsating effect
    PULSE_COLORS = ["#fff3cd", "#ffe066", "#ffd700", "#ffe066"]
    NORMAL_BG = "white"
    ERROR_BG = "#ffcccc"
    FLASH_BG = "#90EE90"  # Light green for key press flash
    
    def __init__(self, parent, index, on_delete=None, on_waiting=None):
        self.parent = parent
        self.index = index
        self.on_delete = on_delete
        self.on_waiting = on_waiting
        self.current_entry = None
        self._pulse_job = None
        self._pulse_index = 0
        
        # Configure styles once
        if not KeyEntry._styles_configured:
            self._configure_styles()
            KeyEntry._styles_configured = True
        
        # Create a frame for this row
        self.row_frame = ttk.Frame(parent)
        self.row_frame.grid(row=index, column=0, sticky="ew", pady=(0, 2))
        parent.grid_columnconfigure(0, weight=1)
        
        # Key section
        self.key_label = ttk.Label(self.row_frame, text=f"Key {index+1}:", width=6)
        self.key_label.grid(row=0, column=0, padx=(0, 5), sticky="e")
        
        # Use tk.Entry for direct background control (for animation)
        self.key_entry = tk.Entry(
            self.row_frame, width=10, justify="center",
            font=("Segoe UI", 9), relief="solid", bd=1
        )
        self.key_entry.grid(row=0, column=1, padx=(0, 15), sticky="ew", ipady=3)
        self.key_entry.bind("<Button-1>", self.select_entry)
        self.key_entry.bind("<FocusIn>", self.select_entry)
        self.key_entry.bind("<FocusOut>", self._on_focus_out)
        
        # Delay section
        self.delay_label = ttk.Label(self.row_frame, text="Delay (s):", width=9)
        self.delay_label.grid(row=0, column=2, padx=(0, 5), sticky="e")
        
        self.delay_spinbox = ttk.Spinbox(
            self.row_frame, from_=0.1, to=60.0, increment=0.1, 
            width=6, format="%.1f"
        )
        self.delay_spinbox.set("1.0")
        self.delay_spinbox.grid(row=0, column=3, padx=(0, 15), sticky="ew")
        self.delay_spinbox.bind("<FocusOut>", self._format_delay)
        self.delay_spinbox.bind("<Return>", self._format_delay)
        
        # Reset button (orange themed)
        self.reset_button = ttk.Button(
            self.row_frame, text="↺", width=3, 
            command=self.reset_key,
            style="Reset.TButton"
        )
        self.reset_button.grid(row=0, column=4, padx=(0, 3))
        
        # Delete button (red themed)
        self.delete_button = ttk.Button(
            self.row_frame, text="✕", width=3,
            command=self.delete_key,
            style="Delete.TButton"
        )
        self.delete_button.grid(row=0, column=5)
        
        # Configure column weights
        self.row_frame.grid_columnconfigure(1, weight=1)
        self.row_frame.grid_columnconfigure(3, weight=1)
    
    def _configure_styles(self):
        """Configure button styles."""
        style = ttk.Style()
        
        # Reset button - orange
        style.configure("Reset.TButton", 
            background="#e67e22",
            foreground="white"
        )
        style.map("Reset.TButton",
            background=[("active", "#d35400"), ("disabled", "#bdc3c7")]
        )
        
        # Delete button - red
        style.configure("Delete.TButton",
            background="#c0392b", 
            foreground="white"
        )
        style.map("Delete.TButton",
            background=[("active", "#a93226"), ("disabled", "#bdc3c7")]
        )
    
    def _start_pulse(self):
        """Start pulsating animation."""
        self._stop_pulse()
        self._pulse_index = 0
        self._do_pulse()
    
    def _do_pulse(self):
        """Execute one pulse step."""
        if self.current_entry:
            color = self.PULSE_COLORS[self._pulse_index % len(self.PULSE_COLORS)]
            self.key_entry.configure(bg=color)
            self._pulse_index += 1
            self._pulse_job = self.row_frame.after(200, self._do_pulse)
    
    def _stop_pulse(self):
        """Stop pulsating animation."""
        if self._pulse_job:
            self.row_frame.after_cancel(self._pulse_job)
            self._pulse_job = None
    
    def _on_focus_out(self, event=None):
        """Handle focus out - stop waiting if clicked elsewhere."""
        # Small delay to check if we're still waiting
        self.row_frame.after(100, self._check_focus)
    
    def _check_focus(self):
        """Check if we should stop waiting."""
        if self.current_entry and not self.key_entry.focus_get() == self.key_entry:
            self.cancel_waiting()
            if self.on_waiting:
                self.on_waiting(False)
    
    def cancel_waiting(self):
        """Cancel waiting state without triggering callback."""
        self._stop_pulse()
        self.key_entry.configure(bg=self.NORMAL_BG)
        self.current_entry = None
    
    def select_entry(self, event=None):
        """Set this entry as the currently selected key entry."""
        # Don't allow selection when disabled (e.g., when running)
        if self.key_entry.cget('state') == 'disabled':
            return "break"
        
        self.current_entry = self.key_entry
        self.clear_error()
        self._start_pulse()
        if self.on_waiting:
            self.on_waiting(True, self)
        return "break"
        
    def set_key(self, key):
        """Set the key value in the entry field."""
        if self.current_entry:
            self._stop_pulse()
            self.key_entry.configure(bg=self.NORMAL_BG)
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, key)
            self.current_entry = None
            if self.on_waiting:
                self.on_waiting(False)
            
    def reset_key(self):
        """Reset the key entry."""
        self._stop_pulse()
        self.key_entry.delete(0, tk.END)
        self.current_entry = None
        self.key_entry.configure(bg=self.NORMAL_BG)
    
    def show_error(self):
        """Highlight the key entry as having an error (red)."""
        self._stop_pulse()
        self.key_entry.configure(bg=self.ERROR_BG)
    
    def clear_error(self):
        """Clear the error highlight from key entry."""
        self.key_entry.configure(bg=self.NORMAL_BG)
    
    def flash(self):
        """Flash the entry briefly to indicate the key was pressed."""
        # Use disabledbackground when entry is disabled (bot running)
        if self.key_entry.cget('state') == 'disabled':
            self.key_entry.configure(disabledbackground=self.FLASH_BG)
            self.row_frame.after(150, lambda: self.key_entry.configure(disabledbackground=self.NORMAL_BG))
        else:
            self.key_entry.configure(bg=self.FLASH_BG)
            self.row_frame.after(150, lambda: self.key_entry.configure(bg=self.NORMAL_BG))
        
    def delete_key(self):
        """Call the delete callback if provided."""
        self._stop_pulse()
        if self.on_delete:
            self.on_delete(self.index)
            
    def get_key(self):
        """Get the current key value."""
        return self.key_entry.get()
        
    def get_delay(self):
        """Get the current delay value."""
        self._format_delay()
        return self.delay_spinbox.get()
    
    def _format_delay(self, event=None):
        """Format delay value to always show one decimal (e.g., 2 -> 2.0)."""
        try:
            value = float(self.delay_spinbox.get())
            value = max(0.1, min(60.0, value))
            self.delay_spinbox.delete(0, tk.END)
            self.delay_spinbox.insert(0, f"{value:.1f}")
        except ValueError:
            self.delay_spinbox.delete(0, tk.END)
            self.delay_spinbox.insert(0, "1.0")
        
    def update_index(self, new_index):
        """Update the index and labels of this entry."""
        self.index = new_index
        self.key_label.config(text=f"Key {new_index+1}:")
        self.row_frame.grid(row=new_index, column=0, sticky="ew", pady=(0, 2))
        
    def grid_remove(self):
        """Remove the row frame from the grid."""
        self._stop_pulse()
        self.row_frame.grid_forget()
        
    def set_state(self, state):
        """Set the state of interactive elements."""
        tk_state = "disabled" if state == "disabled" else "normal"
        ttk_state = "disabled" if state == "disabled" else "!disabled"
        self.reset_button.state([ttk_state])
        self.delete_button.state([ttk_state])
        self.key_entry.configure(state=tk_state)
        self.delay_spinbox.state([ttk_state])
