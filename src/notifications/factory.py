"""
Factory for creating notification providers.
"""

from .notifier import Notifier
from .providers.base import NotificationProvider
from .providers import (
    telegram_provider,
    node_red_provider
)

class NotificationFactory:
    _providers = {
        'telegram': telegram_provider.TelegramProvider,
        'node_red': node_red_provider.NodeRedProvider
    }

    @classmethod
    def create_notifier(cls, enabled_providers) -> Notifier:
        """Creates a notifier with the specified providers."""
        providers = []
        for provider_name in enabled_providers:
            if provider_name in cls._providers:
                providers.append(cls._providers[provider_name]())
        return Notifier(providers)

    @classmethod
    def register_provider(cls, name: str, provider_class):
        """Registers a new provider type."""
        cls._providers[name] = provider_class
