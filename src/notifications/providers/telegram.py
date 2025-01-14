"""
Telegram notification provider implementation.
"""
import urequests
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

    def _url_encode(self, text):
        """
        Codifica manualmente un texto para URL.
        """
        # Caracteres seguros que no necesitan codificación
        safe = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~"
        result = ""

        for char in str(text):
            if char in safe:
                result += char
            else:
                # Convertir el carácter a bytes y luego a hexadecimal
                for byte in char.encode('utf-8'):
                    result += f"%{byte:02X}"

        return result

    async def send(self, message):
        """Send a message to all configured Telegram chats."""
        if not settings.PROVIDER_TELEGRAM_ENABLED:
            return

        print(f"Preparing to send message: '{message}'")

        response = None
        try:
            for chat_id in settings.TELEGRAM_CHAT_IDS:
                try:
                    # Codificar el mensaje
                    encoded_message = self._url_encode(message)
                    url = f"{self.base_url}/sendMessage?chat_id={chat_id}&text={encoded_message}"

                    print(f"Sending Telegram message to {chat_id}")
                    print(f"URL: {url}")

                    response = urequests.get(url)

                    print(f"Response status: {response.status_code}")
                    print(f"Response text: {response.text}")

                    if response.status_code == 200:
                        print(f"Message sent successfully to {chat_id}")
                    else:
                        print(f"Failed to send to {chat_id}: {response.text}")

                except Exception as e:
                    print(f"Error sending to {chat_id}: {str(e)}")
                finally:
                    if response:
                        response.close()

        except Exception as e:
            print(f"Telegram error: {str(e)}")
            raise
