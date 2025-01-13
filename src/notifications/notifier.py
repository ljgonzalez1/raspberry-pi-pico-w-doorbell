"""
Main notification orchestrator.
"""
from .providers.base import NotificationProvider


class Notifier:
    def __init__(self, providers):
        self.providers = providers

    async def notify(self, message: str):
        """Sends notifications through all configured providers."""
        for provider in self.providers:
            await provider.send(message)
