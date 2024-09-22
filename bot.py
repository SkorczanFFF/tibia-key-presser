import pywinauto
import time
import threading
import tkinter as tk
from tkinter import messagebox

class KeyPressApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tibia Key Presser")

        self.keys = []
        self.delays = []
        self.running = False
        self.current_entry = None
        self.max_pairs = 8  # Max key-delay pairs allowed

        # Main frame for holding the input fields and buttons
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Frame for key and delay entries
        self.entries_frame = tk.Frame(self.main_frame)
        self.entries_frame.grid(row=1, column=0, columnspan=6, pady=5, sticky="ew")

        # Create initial key-delay pair
        self.key_entries = []
        self.delay_spinboxes = []
        self.reset_buttons = []
        self.delete_buttons = []
        self.key_labels = []
        self.delay_labels = []
        self.create_key_delay_pair(0)

        # Frame for buttons
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Button to add more key-delay pairs
        self.add_button = tk.Button(self.button_frame, text="Add Key", command=self.add_key_delay_pair)
        self.add_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Buttons for starting and stopping
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start, bg="green", fg="white")
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop, bg="red", fg="white")

        # Place start/stop buttons
        self.start_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.stop_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Status label for showing messages (moved to the right of the buttons)
        self.status_label = tk.Label(self.button_frame, text="", fg="red")
        self.status_label.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        # Configure grid weights for resizing
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.entries_frame.grid_columnconfigure(1, weight=1)
        self.entries_frame.grid_columnconfigure(3, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

        # Update Add Key button visibility
        self.update_add_button_visibility()

        self.toggle_buttons()

        # Set up protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Include the rest of your class methods here...

    def on_closing(self):
        """Handle the window close event."""
        if self.running:
            self.stop()  # Stop the key pressing threads
        self.root.destroy()  # Close the Tkinter window

    def create_key_delay_pair(self, index):
        """Create a key-delay pair and place it on the grid."""
        # Key label
        key_label = tk.Label(self.entries_frame, text=f"Key {index+1}:")
        key_label.grid(row=index, column=0, padx=10, pady=5, sticky="e")
        self.key_labels.append(key_label)

        # Key entry
        key_entry = tk.Entry(self.entries_frame)
        key_entry.grid(row=index, column=1, padx=10, pady=5, sticky="ew")
        key_entry.bind("<Button-1>", self.select_entry)
        self.key_entries.append(key_entry)

        # Reset button for key entry
        reset_button = tk.Button(self.entries_frame, text="Reset", command=lambda i=index: self.reset_key(i))
        reset_button.grid(row=index, column=4, padx=10, pady=5)
        self.reset_buttons.append(reset_button)

        # Delete button for key entry
        delete_button = tk.Button(self.entries_frame, text="Delete", command=lambda i=index: self.delete_key(i))
        delete_button.grid(row=index, column=5, padx=10, pady=5)
        self.delete_buttons.append(delete_button)

        # Delay label and spinbox
        delay_label = tk.Label(self.entries_frame, text=f"Delay {index+1} (seconds):")
        delay_label.grid(row=index, column=2, padx=10, pady=5, sticky="e")
        self.delay_labels.append(delay_label)

        delay_spinbox = tk.Spinbox(self.entries_frame, from_=0.0, to=10.0, increment=0.1, format="%.1f")
        delay_spinbox.grid(row=index, column=3, padx=10, pady=5, sticky="ew")
        self.delay_spinboxes.append(delay_spinbox)

        # Disable Delete button if it's the only entry
        if len(self.key_entries) == 1:
            delete_button.config(state="disabled")

    def add_key_delay_pair(self):
        """Dynamically add key-delay pairs, up to a maximum of 8."""
        if len(self.key_entries) < self.max_pairs:
            self.create_key_delay_pair(len(self.key_entries))
            self.update_add_button_visibility()

    def delete_key(self, index):
        """Delete the key-delay pair at the specified index."""
        if self.running:
            messagebox.showwarning("Script Running", "Cannot delete while the script is running.")
            return

        if len(self.key_entries) > 1:  # Ensure at least one key-bind row remains
            # Remove widgets from the grid
            self.key_labels[index].grid_forget()
            self.key_entries[index].grid_forget()
            self.delay_labels[index].grid_forget()
            self.delay_spinboxes[index].grid_forget()
            self.reset_buttons[index].grid_forget()
            self.delete_buttons[index].grid_forget()

            # Remove the key-bind pair from the lists
            del self.key_labels[index]
            del self.key_entries[index]
            del self.delay_labels[index]
            del self.delay_spinboxes[index]
            del self.reset_buttons[index]
            del self.delete_buttons[index]

            # Re-arrange remaining key-bind rows
            for i in range(len(self.key_entries)):
                self.key_labels[i].grid(row=i, column=0)
                self.key_entries[i].grid(row=i, column=1)
                self.delay_labels[i].grid(row=i, column=2)
                self.delay_spinboxes[i].grid(row=i, column=3)
                self.reset_buttons[i].grid(row=i, column=4)
                self.delete_buttons[i].grid(row=i, column=5)
                # Update labels
                self.key_labels[i].config(text=f"Key {i+1}:")
                self.delay_labels[i].config(text=f"Delay {i+1} (seconds):")

            # Disable Delete button if there is only one key-delay pair left
            if len(self.key_entries) == 1:
                self.delete_buttons[0].config(state="disabled")
            else:
                self.delete_buttons[0].config(state="normal")

            # Update Add Key button visibility
            self.update_add_button_visibility()

    def connect_to_window(self):
        """Connect to the Tibia window."""
        title_re = r"^Tibia - .*"
        try:
            app = pywinauto.Application().connect(title_re=title_re)
            window = app.top_window()
            window_title = window.window_text()

            if window_title.startswith("Tibia - "):
                character_name = window_title[len("Tibia - "):].strip()
                self.root.title(f"Tibia Key Presser - {character_name}")
            return app
        except pywinauto.findwindows.ElementNotFoundError:
            messagebox.showerror("Error", "No Tibia window found with title starting with 'Tibia - '.")
            return None

    def press_keys(self, key, delay):
        """Send key presses to the connected Tibia window."""
        app = self.connect_to_window()
        if not app:
            return
        window = app.window(title_re=r"^Tibia - .*")
        while self.running:
            window.send_keystrokes(f'{{{key}}}')
            time.sleep(delay)

    def start(self):
        """Start the key pressing threads."""
        if not all(entry.get() for entry in self.key_entries) or not all(spinbox.get() for spinbox in self.delay_spinboxes):
            self.status_label.config(text="Please set all key and delay values before starting.")
            return

        self.keys = []
        self.delays = []

        # Collect key-delay pairs that are set
        for key_entry, delay_spinbox in zip(self.key_entries, self.delay_spinboxes):
            key = key_entry.get()
            delay = delay_spinbox.get()

            if key and delay:
                self.keys.append(key)
                self.delays.append(float(delay))

        # Check if at least one key and its corresponding delay are set
        if not self.keys:
            self.status_label.config(text="At least one key and its corresponding delay must be set.")
            return

        if self.running:
            messagebox.showinfo("Already Running", "The key presser is already running.")
            return

        self.running = True
        self.threads = []
        for key, delay in zip(self.keys, self.delays):
            thread = threading.Thread(target=self.press_keys, args=(key, delay))
            self.threads.append(thread)
            thread.start()

        self.toggle_buttons()

    def stop(self):
        """Stop the key pressing threads."""
        self.running = False
        for thread in self.threads:
            thread.join()
        self.toggle_buttons()

    def toggle_buttons(self):
        """Toggle between start and stop buttons."""
        if self.running:
            self.start_button.config(bg="gray")  # Grey out the Start button
            self.stop_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            self.start_button.grid_forget()
            self.add_button.config(state="disabled")  # Disable the Add Key button
            # Disable all Reset and Delete buttons
            for button in self.reset_buttons:
                button.config(state="disabled")
            for button in self.delete_buttons:
                button.config(state="disabled")
        else:
            self.stop_button.config(bg="red")  # Set the Stop button to its original color
            self.start_button.config(bg="green")  # Set the Start button to its original color
            self.start_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            self.stop_button.grid_forget()
            self.add_button.config(state="normal")  # Re-enable the Add Key button
            # Re-enable all Reset and Delete buttons
            for button in self.reset_buttons:
                button.config(state="normal")
            for button in self.delete_buttons:
                button.config(state="normal")

    def select_entry(self, event):
        """Set the currently selected key entry."""
        if self.running:
            messagebox.showwarning("Script Running", "Cannot select key entry while the script is running.")
            return
        self.current_entry = event.widget
        index = self.key_entries.index(self.current_entry)
        self.status_label.config(text=f"Press any key to bind to Key {index + 1}")
        self.current_entry.config(bg="yellow")  # Highlight selected entry
        self.root.bind("<KeyPress>", self.bind_key)

    def bind_key(self, event):
        """Bind the selected key to the current entry."""
        if self.current_entry:
            self.status_label.config(text="")
            self.current_entry.config(bg="white")
            self.current_entry.delete(0, tk.END)
            self.current_entry.insert(0, event.keysym)
            self.root.unbind("<KeyPress>")

    def reset_key(self, index):
        """Reset the key entry for the specified index."""
        if self.running:
            messagebox.showwarning("Script Running", "Cannot reset key while the script is running.")
            return
        self.key_entries[index].delete(0, tk.END)
        self.status_label.config(text="")

    def update_add_button_visibility(self):
        """Update the visibility of the Add Key button based on the number of pairs."""
        if len(self.key_entries) >= self.max_pairs:
            self.add_button.grid_forget()  # Hide the button
        else:
            self.add_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")  # Show the button

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyPressApp(root)
    root.mainloop()
