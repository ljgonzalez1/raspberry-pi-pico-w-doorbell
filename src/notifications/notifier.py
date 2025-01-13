"""
Notification orchestrator module.
"""
from core.network_manager import NetworkManager
from utils.logging import dprint as print


class Notifier:
    """
    Orchestrates sending notifications through multiple providers.
    Manages network connection and LED status indication.
    """

    def __init__(self, providers, heart_led=None):
        """
        Initialize the notifier.

        Args:
            providers (list): List of notification providers
            heart_led (HeartLED, optional): LED indicator instance
        """
        self.providers = providers
        self.network = NetworkManager()
        self.heart_led = heart_led

    async def notify(self, message):
        """
        Send notifications through all enabled providers.

        Args:
            message (str): Message to send
        """
        network_connected = False

        try:
            if self.heart_led:
                self.heart_led.set_state(self.heart_led.STATE_CONNECTING)

            # Connect to network if needed
            if not self.network.is_connected():
                connected = await self.network.connect()

                if not connected:
                    print("Failed to establish network connection")
                    return

                network_connected = True

            if self.heart_led:
                self.heart_led.set_state(self.heart_led.STATE_SENDING)

            # Send through all providers
            failed_providers = []

            for provider in self.providers:
                try:
                    provider_name = provider.__class__.__name__
                    print(f"Sending via {provider_name}")
                    await provider.send(message)

                except Exception as e:
                    print(f"Error in {provider_name}: {str(e)}")
                    failed_providers.append(provider_name)

            # Report failed providers
            if failed_providers:
                print("Failed providers:")

                for provider in failed_providers:
                    print(f"  - {provider}")

        finally:
            if self.heart_led:
                self.heart_led.set_state(self.heart_led.STATE_NORMAL)

            if network_connected:
                self.network.disconnect()
