"""
Telegram notification provider implementation.
"""
import urequests
import ujson
from ..base_provider import BaseProvider
from config import settings
from utils.logging import dprint as print


class TelegramProvider(BaseProvider):
    """Provider for sending notifications via Telegram."""

    def __init__(self):
        """Initialize the Telegram provider."""
        if not settings.PROVIDER_TELEGRAM_ENABLED:
            return

        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    async def send(self, message):
        """Send a message to all configured Telegram chats."""
        if not settings.PROVIDER_TELEGRAM_ENABLED:
            return

        response = None
        try:
            url = f"{self.base_url}/sendMessage"

            for chat_id in settings.TELEGRAM_CHAT_IDS:
                try:
                    print(f"Sending Telegram message to {chat_id}")

                    data = {
                        "chat_id": chat_id,
                        "text": message
                    }

                    response = urequests.post(
                        url,
                        headers={'Content-Type': 'application/json'},
                        data=ujson.dumps(data)
                    )

                    if response.status_code == 200:
                        print(f"Message sent to {chat_id}")
                    else:
                        print(f"Failed to send to {chat_id}: {response.text}")

                finally:
                    if response:
                        response.close()

        except Exception as e:
            print(f"Telegram error: {str(e)}")
            raise
