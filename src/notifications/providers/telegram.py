"""
Telegram notification provider implementation.
"""
import ujson
import urequests
from .base import NotificationProvider
from core.network import WiFiManager
from config import settings


class TelegramProvider(NotificationProvider):
    def __init__(self):
        self.wifi = WiFiManager()
        self.base_url = f"https://api.telegram.org/bot" \
                        f"{settings.TELEGRAM_BOT_TOKEN}"

    async def send(self, message: str):
        try:
            await self.connect()
            for chat_id in settings.TELEGRAM_CHAT_IDS:
                await self._send_message(chat_id, message)
        finally:
            await self.disconnect()

    async def _send_message(self, chat_id: str, message: str):
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message
        }
        response = urequests.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=ujson.dumps(data)
        )
        response.close()

    async def connect(self):
        await self.wifi.connect()

    async def disconnect(self):
        await self.wifi.disconnect()
