"""
Main entry point for the doorbell application.
Initializes and runs the doorbell monitoring system.
"""
from machine import Pin
import uasyncio as asyncio

from config import settings
from core.doorbell import Doorbell
from core.heart_led import HeartLED
from notifications.factory import NotificationFactory


async def main():
    # Initialize LED and doorbell pins
    led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)
    doorbell_pin = Pin(settings.DOORBELL_PIN, Pin.IN, Pin.PULL_UP)

    # Initialize components
    heart = HeartLED(led)
    notifier = NotificationFactory.create_notifier(settings.ENABLED_PROVIDERS)
    doorbell = Doorbell(doorbell_pin, heart, notifier)

    # Create tasks
    tasks = [
        asyncio.create_task(heart.run()),
        asyncio.create_task(doorbell.monitor())
    ]

    # Run event loop
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Application stopped")
