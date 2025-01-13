"""
Discord webhook notification provider implementation.
"""
import urequests
import ujson
from ..base_provider import BaseProvider
from config import settings
from utils.logging import dprint as print


class DiscordWebhookProvider(BaseProvider):
    """Provider for sending notifications via Discord webhooks."""

    def __init__(self):
        """Initialize the Discord webhook provider."""
        if not settings.PROVIDER_DISCORD_ENABLED:
            return

        self.webhook_urls = settings.DISCORD_WEBHOOK_URLS

    async def send(self, message):
        """Send a message to all configured Discord webhooks."""
        if not settings.PROVIDER_DISCORD_ENABLED:
            return

        for webhook_url in self.webhook_urls:
            response = None

            try:
                data = {
                    "content": message
                }

                print(f"Sending to Discord webhook")
                response = urequests.post(
                    webhook_url,
                    headers={'Content-Type': 'application/json'},
                    data=ujson.dumps(data)
                )

                if response.status_code == 204:
                    print("Discord message sent")

                else:
                    print(f"Failed to send to Discord: {response.text}")

            except Exception as e:
                print(f"Discord error: {str(e)}")
                raise

            finally:
                if response:
                    response.close()
