import pywinauto
import time
import threading
import tkinter as tk
from tkinter import messagebox

class KeyPressApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tibia Key Presser")

        self.character_name = tk.StringVar()
        self.keys = []
        self.delays = []
        self.running = False
        self.current_entry = None

        # Create GUI elements
        tk.Label(root, text="Character Name:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.character_name).grid(row=0, column=1, padx=10, pady=5)

        # Create sections for up to 4 keys and delays
        self.key_entries = []
        self.delay_entries = []
        for i in range(4):
            tk.Label(root, text=f"Key {i+1}:").grid(row=i+1, column=0, padx=10, pady=5)
            key_entry = tk.Entry(root)
            key_entry.grid(row=i+1, column=1, padx=10, pady=5)
            key_entry.bind("<Button-1>", self.select_entry)
            self.key_entries.append(key_entry)

            tk.Label(root, text=f"Delay {i+1} (seconds):").grid(row=i+1, column=2, padx=10, pady=5)
            delay_entry = tk.Entry(root)
            delay_entry.grid(row=i+1, column=3, padx=10, pady=5)
            self.delay_entries.append(delay_entry)

        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)

        # Place buttons
        self.start_button.grid(row=5, column=0, padx=10, pady=10)
        self.stop_button.grid(row=5, column=1, padx=10, pady=10)

        self.toggle_buttons()

    def connect_to_window(self):
        title = f"Tibia - {self.character_name.get()}"
        try:
            return pywinauto.Application().connect(title_re=title)
        except pywinauto.findwindows.ElementNotFoundError:
            messagebox.showerror("Error", f"Window with title '{title}' not found.")
            return None

    def press_keys(self, key, delay):
        app = self.connect_to_window()
        if not app:
            return
        window = app.window(title_re=f"Tibia - {self.character_name.get()}")
        while self.running:
            window.send_keystrokes(f'{{{key}}}')
            time.sleep(delay)

    def start(self):
        print(f"Attempting to connect to window with title: Tibia - {self.character_name.get()}")
        
        self.keys = [entry.get() for entry in self.key_entries if entry.get()]
        self.delays = [float(entry.get()) for entry in self.delay_entries if entry.get()]
        
        if len(self.keys) != len(self.delays):
            messagebox.showerror("Input Error", "Each key must have a corresponding delay.")
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
        self.running = False
        for thread in self.threads:
            thread.join()
        self.toggle_buttons()

    def toggle_buttons(self):
        if self.running:
            self.start_button.grid_forget()
            self.stop_button.grid(row=5, column=0, padx=10, pady=10)
        else:
            self.stop_button.grid_forget()
            self.start_button.grid(row=5, column=0, padx=10, pady=10)

    def select_entry(self, event):
        # Set the currently selected entry to capture key press
        self.current_entry = event.widget
        self.root.bind("<KeyPress>", self.bind_key)

    def bind_key(self, event):
        if self.current_entry:
            self.current_entry.delete(0, tk.END)  # Clear previous content
            self.current_entry.insert(0, event.keysym)  # Insert the new key
            self.root.unbind("<KeyPress>")  # Unbind the key press event

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyPressApp(root)
    root.mainloop()
