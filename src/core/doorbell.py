"""
Core doorbell monitoring functionality.
"""
import uasyncio as asyncio
from machine import Pin

from utils.logging import Logger

class Doorbell:
    def __init__(self, pin: Pin, heart_led, notifier):
        self.pin = pin
        self.heart_led = heart_led
        self.notifier = notifier
        self.logger = Logger(__name__)

    async def monitor(self):
        """Monitors the doorbell pin for changes."""
        while True:
            if not self.pin.value():
                self.logger.info("Doorbell pressed")
                self.heart_led.off()
                await self.notifier.notify("Doorbell pressed")
                await asyncio.sleep_ms(500)  # Debounce
            await asyncio.sleep_ms(1)
