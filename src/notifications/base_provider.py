"""
Base notification provider interface.
"""


class BaseProvider:
    """Base class for all notification providers."""

    async def send(self, message):
        """
        Send a notification message.

        Args:
            message (str): The message to send

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError()
