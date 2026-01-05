"""
Module for handling the key pressing functionality.
"""
from threading import Thread
from time import sleep, time
from datetime import datetime
from src.core.window_manager import TibiaWindowManager
from src.utils.constants import CHECK_INTERVAL

class KeyPresser:
    """Class to handle the key pressing functionality."""
    
    def __init__(self, on_key_press=None):
        """Initialize the KeyPresser."""
        self.running = False
        self.threads = []
        self.on_key_press = on_key_press
        
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
        
        last_press = time()
        while self.running:
            now = time()
            actual_interval = now - last_press
            last_press = now
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] [{key}] interval: {actual_interval:.3f}s (expected: {delay}s)")
            
            TibiaWindowManager.send_key_to_window(window, key)
            if self.on_key_press:
                self.on_key_press(key)
            
            # Break down the delay into smaller intervals
            for _ in range(intervals):
                if not self.running:
                    return
                sleep(CHECK_INTERVAL)
            
            # Handle any remaining time
            remaining_time = delay - (intervals * CHECK_INTERVAL)
            if remaining_time > 0 and self.running:
                sleep(remaining_time) 