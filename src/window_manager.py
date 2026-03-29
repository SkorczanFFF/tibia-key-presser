"""
Module for managing connections to the Tibia game window.
"""
from __future__ import annotations

import logging
from typing import Any

from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError

log = logging.getLogger(__name__)

TIBIA_TITLE_RE = r"^Tibia - .*"
TIBIA_TITLE_PREFIX = "Tibia - "


def connect_to_window() -> tuple[Any, str | None]:
    """Connect to the Tibia window.

    Returns a (window, character_name) pair. Both are None on failure.
    """
    try:
        app = Application().connect(title_re=TIBIA_TITLE_RE)
        window = app.top_window()
        window_title: str = window.window_text()

        character_name: str | None = None
        if window_title.startswith(TIBIA_TITLE_PREFIX):
            character_name = window_title[len(TIBIA_TITLE_PREFIX):].strip()

        return window, character_name
    except ElementNotFoundError:
        return None, None
    except Exception:
        log.warning("Unexpected error connecting to Tibia window", exc_info=True)
        return None, None


def send_key_to_window(window: Any, key: str) -> bool:
    """Send a keystroke to the given window.

    Returns True on success, False on failure.
    """
    if not window:
        return False
    try:
        window.send_keystrokes(f'{{{key}}}')
        return True
    except Exception:
        log.warning("Failed to send key '%s' to Tibia window", key, exc_info=True)
        return False 