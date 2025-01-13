"""
Factory for creating notification providers.
"""
from typing import List
from .notifier import Notifier
from .providers.base import NotificationProvider
from .providers import (
    telegram_provider,
    node_red_provider
)

class NotificationFactory:
    _providers = {
        'telegram': telegram_provider,
        'node_red': node_red_provider
    }

    @classmethod
    def create_notifier(cls, enabled_providers: List[str]) -> Notifier:
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
