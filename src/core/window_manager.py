"""
Module for managing connections to the Tibia game window.
"""
from pywinauto import Application

class TibiaWindowManager:
    """Class to handle connections to the Tibia game window."""
    
    @staticmethod
    def connect_to_window():
        """
        Connect to the Tibia window.
        
        Returns:
            tuple: (app, window, character_name) on success, (None, None, None) on failure
        """
        title_re = r"^Tibia - .*"
        try:
            app = Application().connect(title_re=title_re)
            window = app.top_window()
            window_title = window.window_text()

            character_name = None
            if window_title.startswith("Tibia - "):
                character_name = window_title[len("Tibia - "):].strip()
                
            return app, window, character_name
        except Exception as e:
            return None, None, None
            
    @staticmethod
    def send_key_to_window(window, key):
        """
        Send a keystroke to the given window.
        
        Args:
            window: The window to send keystrokes to
            key: The key to send
        """
        if window:
            window.send_keystrokes(f'{{{key}}}') 