"""
Main application entry point.
"""
import uasyncio
from machine import Pin

from config import settings
from core.heart_led import HeartLED
from notifications.notifier import Notifier
from notifications.providers.telegram import TelegramProvider
from notifications.providers.node_red import NodeRedProvider
from notifications.providers.simple_get import SimpleGetProvider
from notifications.providers.twilio_whatsapp import TwilioWhatsAppProvider
from notifications.providers.twilio_sms import TwilioSMSProvider
from notifications.providers.slack_webhook import SlackWebhookProvider
from notifications.providers.discord_webhook import DiscordWebhookProvider
from notifications.providers.pushover import PushoverProvider
from utils.logging import dprint as print


# Initialize hardware
led_pin = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)
doorbell_pin = Pin(settings.DOORBELL_PIN, Pin.IN, Pin.PULL_UP)

# Initialize components
heart = HeartLED(led_pin)
if not settings.LED_ENABLED:
    heart.stop()

# Initialize enabled providers
providers = []
if settings.PROVIDER_TELEGRAM_ENABLED:
    providers.append(TelegramProvider())
if settings.PROVIDER_NODE_RED_ENABLED:
    providers.append(NodeRedProvider())
if settings.PROVIDER_SIMPLE_GET_ENABLED:
    providers.append(SimpleGetProvider())
if settings.PROVIDER_TWILIO_WHATSAPP_ENABLED:
    providers.append(TwilioWhatsAppProvider())
if settings.PROVIDER_TWILIO_SMS_ENABLED:
    providers.append(TwilioSMSProvider())
if settings.PROVIDER_SLACK_ENABLED:
    providers.append(SlackWebhookProvider())
if settings.PROVIDER_DISCORD_ENABLED:
    providers.append(DiscordWebhookProvider())
if settings.PROVIDER_PUSHOVER_ENABLED:
    providers.append(PushoverProvider())

# Initialize notifier
notifier = Notifier(providers, heart)


async def monitor_doorbell():
    """Monitor doorbell state and trigger notifications."""
    while True:
        if not doorbell_pin.value():
            print("Doorbell pressed!")
            await notifier.notify("Doorbell pressed!")
            # Debounce delay
            await uasyncio.sleep_ms(500)
        await uasyncio.sleep_ms(1)


async def main():
    """Main application coroutine."""
    tasks = [
        uasyncio.create_task(heart.run()),
        uasyncio.create_task(monitor_doorbell())
    ]
    await uasyncio.gather(*tasks)


# Run the event loop
try:
    print("Starting doorbell monitor...")
    uasyncio.run(main())
except KeyboardInterrupt:
    print("Application stopped")
except Exception as e:
    print(f"Fatal error: {str(e)}")
finally:
    # Clean up
    if heart:
        heart.stop()
