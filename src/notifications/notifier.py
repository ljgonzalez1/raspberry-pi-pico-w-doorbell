"""
Notification orchestrator module.
"""
import uasyncio
from core.network_manager import NetworkManager
from utils.logging import dprint as print


class Notifier:
    """
    Orchestrates sending notifications through multiple providers.
    Manages network connection and LED status indication.
    """

    MAX_RETRIES = 5
    RETRY_DELAY_MS = 1000  # 1 segundo entre intentos

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

    async def _try_send_provider(self, provider, message, attempt=1):
        """
        Try to send message through a provider with retries.

        Args:
            provider: The provider instance
            message (str): Message to send
            attempt (int): Current attempt number

        Returns:
            bool: True if successful, False otherwise
        """
        provider_name = None

        try:
            provider_name = provider.__class__.__name__
            print(f"Sending via {provider_name} (Attempt {attempt}/{self.MAX_RETRIES})")
            await provider.send(message)
            print(f"Successfully sent via {provider_name}")
            return True

        except Exception as e:
            print(f"Error in {provider_name} (Attempt {attempt}): {str(e)}")
            return False

    async def notify(self, message):
        """
        Send notifications through all enabled providers with retries.

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

            # First attempt for all providers
            failed_providers = []
            first_round_failed = []

            for provider in self.providers:
                if not await self._try_send_provider(provider, message):
                    first_round_failed.append(provider)

            # Retry failed providers with delay
            for retry in range(2, self.MAX_RETRIES + 1):  # Start from attempt 2
                if not first_round_failed:
                    break

                # Wait before retry
                await uasyncio.sleep_ms(self.RETRY_DELAY_MS)

                still_failed = []
                for provider in first_round_failed:
                    if not await self._try_send_provider(provider, message, retry):
                        still_failed.append(provider)

                # Update failed list for next round
                first_round_failed = still_failed

            # Add any providers that never succeeded to final failed list
            failed_providers.extend([p.__class__.__name__ for p in first_round_failed])

            # Report failed providers
            if failed_providers:
                print("Failed providers after all retries:")
                for provider in failed_providers:
                    print(f"  - {provider}")

        finally:
            if self.heart_led:
                self.heart_led.set_state(self.heart_led.STATE_NORMAL)
            if network_connected:
                self.network.disconnect()
