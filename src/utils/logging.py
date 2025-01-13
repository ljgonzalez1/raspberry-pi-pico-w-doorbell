"""
Logging utility module.
"""
from config import settings


def dprint(*args, **kwargs):
    """
    Debug print function.
    Only prints if SERIAL_LOGS is enabled in settings.

    Args:
        *args: Variable length argument list to print
        **kwargs: Arbitrary keyword arguments for print function
    """
    if settings.SERIAL_LOGS:
        print(*args, **kwargs)
