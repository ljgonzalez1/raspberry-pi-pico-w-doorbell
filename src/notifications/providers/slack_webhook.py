"""
Slack webhook notification provider implementation.
"""
import urequests
import ujson
from ..base_provider import BaseProvider
from config import settings
from utils.logging import dprint as print


class SlackWebhookProvider(BaseProvider):
    """Provider for sending notifications via Slack webhooks."""

    def __init__(self):
        """Initialize the Slack webhook provider."""
        if not settings.PROVIDER_SLACK_ENABLED:
            return

        self.webhook_urls = settings.SLACK_WEBHOOK_URLS

    async def send(self, message):
        """Send a message to all configured Slack webhooks."""
        if not settings.PROVIDER_SLACK_ENABLED:
            return

        for webhook_url in self.webhook_urls:
            response = None
            try:
                data = {
                    "text": message
                }

                print(f"Sending to Slack webhook")
                response = urequests.post(
                    webhook_url,
                    headers={'Content-Type': 'application/json'},
                    data=ujson.dumps(data)
                )

                if response.status_code == 200:
                    print("Slack message sent")

                else:
                    print(f"Failed to send to Slack: {response.text}")

            except Exception as e:
                print(f"Slack error: {str(e)}")
                raise

            finally:
                if response:
                    response.close()
