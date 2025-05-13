"""
Module for handling the key pressing functionality.
"""
from threading import Thread
from time import sleep
from src.core.window_manager import TibiaWindowManager
from src.utils.constants import CHECK_INTERVAL

class KeyPresser:
    """Class to handle the key pressing functionality."""
    
    def __init__(self):
        """Initialize the KeyPresser."""
        self.running = False
        self.threads = []
        
    def start(self, keys, delays):
        """
        Start pressing keys with the given delays.
        
        Args:
            keys (list): List of keys to press
            delays (list): List of delays in seconds
        """
        if self.running:
            return False
            
        self.running = True
        self.threads = []
        
        for key, delay in zip(keys, delays):
            thread = Thread(target=self._press_key_with_delay, args=(key, float(delay)))
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
            
        return True
        
    def stop(self):
        """Stop all key pressing threads."""
        self.running = False
        for thread in self.threads:
            thread.join()
        
    def _press_key_with_delay(self, key, delay):
        """
        Press a key with a specified delay.
        
        Args:
            key (str): The key to press
            delay (float): Delay between key presses in seconds
        """
        app, window, _ = TibiaWindowManager.connect_to_window()
        if not app or not window:
            return
            
        # Calculate how many small intervals we need
        intervals = int(delay / CHECK_INTERVAL)
        
        while self.running:
            TibiaWindowManager.send_key_to_window(window, key)
            
            # Break down the delay into smaller intervals
            for _ in range(intervals):
                if not self.running:
                    return
                sleep(CHECK_INTERVAL)
            
            # Handle any remaining time
            remaining_time = delay - (intervals * CHECK_INTERVAL)
            if remaining_time > 0 and self.running:
                sleep(remaining_time) 