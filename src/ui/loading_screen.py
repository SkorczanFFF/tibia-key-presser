"""
Loading screen for the Tibia Key Presser application.
"""
import tkinter as tk
import os
import sys
from PIL import Image, ImageTk


class LoadingScreen:
    """A loading screen that displays the app icon while the application loads."""
    
    def __init__(self):
        """Initialize the loading screen."""
        self.root = tk.Tk()
        self._setup_window()
        self._setup_icon()
        
    def _setup_window(self):
        """Set up the loading window with no decorations."""
        # Remove window decorations
        self.root.overrideredirect(True)
        
        # Set window size (square to match icon)
        self.root.geometry("300x300")
        
        # Make window stay on top
        self.root.attributes("-topmost", True)
        
        # Set transparent background
        self.root.configure(bg='white')
        self.root.attributes("-transparentcolor", "white")
        
        # Center the window on screen
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 300) // 2
        self.root.geometry(f"300x300+{x}+{y}")
        
        # Force window to be visible
        self.root.lift()
        self.root.focus_force()
        self.root.update()
        
    def _setup_icon(self):
        """Set up and display the icon."""
        # Try to find the icon file
        icon_path = self._find_icon()
        
        if icon_path:
            try:
                print(f"Loading icon from: {icon_path}")
                # Load and resize the icon
                image = Image.open(icon_path)
                
                # Convert to RGBA to handle transparency properly
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                
                # Resize to fit nicely in the window
                image = image.resize((280, 280), Image.Resampling.LANCZOS)
                
                # Create a new image with proper transparency handling
                # Create a white background and composite the icon on top
                background = Image.new('RGBA', (280, 280), (255, 255, 255, 0))  # Transparent background
                background.paste(image, (0, 0), image)
                
                # Convert to PhotoImage for tkinter
                self.icon_photo = ImageTk.PhotoImage(background)
                
                # Create label to display the icon
                self.icon_label = tk.Label(
                    self.root, 
                    image=self.icon_photo, 
                    bg='white'
                )
                self.icon_label.pack(expand=True)
                print("Icon loaded successfully")
                
            except Exception as e:
                print(f"Error loading icon: {e}")
                self._create_fallback_display()
        else:
            print("No icon file found")
            self._create_fallback_display()
            
    def _find_icon(self):
        """Find the icon file in various possible locations."""
        # Get current working directory
        current_dir = os.getcwd()
        print(f"Current working directory: {current_dir}")
        
        # Possible icon locations - prefer PNG over ICO for better transparency
        icon_locations = [
            "tkp_icon.png",                             # PNG - Current directory (root)
            "tkp_icon.ico",                             # ICO fallback - Current directory (root)
            os.path.join("icons", "tkp_icon.png"),     # PNG - Icons directory
            os.path.join("icons", "tkp_icon.ico"),     # ICO fallback - Icons directory
            os.path.join(current_dir, "tkp_icon.png"),  # PNG - Explicit current directory
            os.path.join(current_dir, "tkp_icon.ico"),  # ICO fallback - Explicit current directory
        ]
        
        # If running from frozen executable, add the executable's directory and PyInstaller temp paths
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
            icon_locations.extend([
                os.path.join(base_dir, "tkp_icon.png"),
                os.path.join(base_dir, "tkp_icon.ico"),
                os.path.join(base_dir, "icons", "tkp_icon.png"),
                os.path.join(base_dir, "icons", "tkp_icon.ico")
            ])
            print(f"Running from frozen executable, base dir: {base_dir}")
            
            # PyInstaller creates a temporary directory for data files
            # Try to find the icon in PyInstaller's temp directory
            if hasattr(sys, '_MEIPASS'):
                temp_dir = sys._MEIPASS
                icon_locations.extend([
                    os.path.join(temp_dir, "tkp_icon.png"),
                    os.path.join(temp_dir, "tkp_icon.ico"),
                    os.path.join(temp_dir, "icons", "tkp_icon.png"),
                    os.path.join(temp_dir, "icons", "tkp_icon.ico")
                ])
                print(f"PyInstaller temp directory: {temp_dir}")
        
        # Try each location
        for icon_path in icon_locations:
            print(f"Checking icon location: {icon_path}")
            if os.path.exists(icon_path):
                print(f"Found icon at: {icon_path}")
                return icon_path
                
        print("No icon file found in any location")
        return None
        
    def _create_fallback_display(self):
        """Create a fallback display if icon cannot be loaded."""
        fallback_label = tk.Label(
            self.root,
            text="TKP",
            font=("Arial", 24, "bold"),
            bg='white',
            fg='black'
        )
        fallback_label.pack(expand=True)
        
    def show(self):
        """Show the loading screen."""
        self.root.deiconify()
        self.root.update()
        
    def hide(self):
        """Hide the loading screen."""
        self.root.withdraw()
        
    def destroy(self):
        """Destroy the loading screen."""
        self.root.destroy()
        
    def update(self):
        """Update the loading screen."""
        self.root.update()
