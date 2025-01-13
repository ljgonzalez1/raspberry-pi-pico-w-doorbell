"""
Logging utility for MicroPython, respecting the SERIAL_LOGS setting from
src/config/settings.py.

Provides a minimal Logger class with methods for different log levels.
"""

from config import settings

class Logger:
    """
    A simple logger that prints messages to the console if SERIAL_LOGS is enabled.
    """

    def __init__(self, name: str):
        """
        Parameters
        ----------
        name : str
            The module or class name that will appear in log messages.
        """
        self.name = name
        self.enabled = settings.SERIAL_LOGS

    def debug(self, msg: str):
        """Logs a debug message."""
        if self.enabled:
            print(f"[DEBUG] {self.name}: {msg}")

    def info(self, msg: str):
        """Logs an info message."""
        if self.enabled:
            print(f"[INFO]  {self.name}: {msg}")

    def warning(self, msg: str):
        """Logs a warning message."""
        if self.enabled:
            print(f"[WARN]  {self.name}: {msg}")

    def error(self, msg: str):
        """Logs an error message."""
        if self.enabled:
            print(f"[ERROR] {self.name}: {msg}")
