"""
Module for handling the key pressing functionality.
"""
from __future__ import annotations

import time
from threading import Thread, Event
from typing import Any, Callable

from src.window_manager import connect_to_window, send_key_to_window

CHECK_INTERVAL: float = 0.1  # Seconds between stop-event checks during delay

# Re-validate the Tibia window every N seconds to detect disconnects
# without hammering the Win32 API on every press cycle
_RECONNECT_INTERVAL: float = 5.0


class KeyPresser:
    """Class to handle the key pressing functionality."""

    def __init__(
        self,
        on_key_press: Callable[[str], None] | None = None,
        on_connection_lost: Callable[[], None] | None = None,
    ) -> None:
        self._stop_event: Event = Event()
        self._stop_event.set()  # starts in stopped state
        self.on_key_press = on_key_press
        self.on_connection_lost = on_connection_lost

    @property
    def running(self) -> bool:
        """True when key pressing is active."""
        return not self._stop_event.is_set()

    def start(self, keys: list[str], delays: list[float]) -> bool:
        """Start pressing keys with the given delays."""
        if self.running:
            return False

        self._stop_event.clear()

        for key, delay in zip(keys, delays):
            thread = Thread(target=self._press_key_with_delay, args=(key, float(delay)))
            thread.daemon = True
            thread.start()

        return True

    def stop(self) -> None:
        """Stop all key pressing threads (non-blocking)."""
        self._stop_event.set()

    def _handle_connection_lost(self) -> None:
        """Stop all threads and notify UI on disconnect (called from worker thread)."""
        if not self._stop_event.is_set():
            self._stop_event.set()
            if self.on_connection_lost:
                self.on_connection_lost()

    def _press_key_with_delay(self, key: str, delay: float) -> None:
        """Press a key with a specified delay.

        Uses absolute timestamps so that overhead from window lookups and
        send_keystrokes never accumulates into drift.
        """
        window: Any = None
        last_reconnect: float = 0.0
        next_press: float = time.time()

        while not self._stop_event.is_set():
            now: float = time.time()

            # Connect or periodically re-validate the window handle
            if window is None or (now - last_reconnect) >= _RECONNECT_INTERVAL:
                window, _ = connect_to_window()
                if not window:
                    self._handle_connection_lost()
                    return
                last_reconnect = now

            if not send_key_to_window(window, key):
                # Send failed — invalidate handle and retry next cycle
                window = None
                continue

            if self.on_key_press:
                self.on_key_press(key)

            # Schedule next press at an absolute time
            next_press += delay

            # Sleep until next_press, checking stop event in small intervals
            while not self._stop_event.is_set():
                remaining = next_press - time.time()
                if remaining <= 0:
                    break
                time.sleep(min(remaining, CHECK_INTERVAL)) 