"""
Module for debugging logging.

This module provides functionalities to print debug messages, which are active
only when the SERIAL_LOGS flag from the settings module is set to True. This
allows for easy enabling or disabling of logging for debugging purposes.

Functions
---------
dprint(*args, **kwargs):
    Print debug messages if SERIAL_LOGS is enabled.
"""

from settings import SERIAL_LOGS


def dprint(*args, **kwargs):
    """
    Print debug messages, if SERIAL_LOGS is enabled.

    This function acts as a wrapper around the built-in print function,
    enabling conditional printing of debug messages based on the
    SERIAL_LOGS setting.

    Parameters
    ----------
    *args :
        Variable length argument list to be printed.
    **kwargs :
        Arbitrary keyword arguments to be passed to the print function.
    """

    if SERIAL_LOGS:
        print(*args, **kwargs)


