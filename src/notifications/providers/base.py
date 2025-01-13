"""
Base interface for notification providers.
"""
from abc import ABC, abstractmethod

class NotificationProvider(ABC):
    @abstractmethod
    async def send(self, message: str):
        """Sends a notification through the provider."""
        pass

    @abstractmethod
    async def connect(self):
        """Establishes connection if needed."""
        pass

    @abstractmethod
    async def disconnect(self):
        """Closes connection if needed."""
        pass
