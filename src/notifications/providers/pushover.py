"""
Pushover notification provider implementation.
"""
import urequests
import ujson
from ..base_provider import BaseProvider
from config import settings
from utils.logging import dprint as print


class PushoverProvider(BaseProvider):
    """Provider for sending notifications via Pushover."""

    def __init__(self):
        """Initialize the Pushover provider."""
        if not settings.PROVIDER_PUSHOVER_ENABLED:
            return

        self.config = settings.PUSHOVER_CONFIG

    async def send(self, message):
        """Send a notification to all configured Pushover users."""
        if not settings.PROVIDER_PUSHOVER_ENABLED:
            return

        for user_key in self.config['user_keys']:
            response = None
            try:
                url = "https://api.pushover.net/1/messages.json"
                data = {
                    "token": self.config['token'],
                    "user": user_key,
                    "message": message
                }

                print(f"Sending Pushover notification")
                response = urequests.post(
                    url,
                    headers={'Content-Type': 'application/json'},
                    data=ujson.dumps(data)
                )

                if response.status_code == 200:
                    print("Pushover notification sent")

                else:
                    print(f"Failed to send to Pushover: {response.text}")

            except Exception as e:
                print(f"Pushover error: {str(e)}")
                raise

            finally:
                if response:
                    response.close()
