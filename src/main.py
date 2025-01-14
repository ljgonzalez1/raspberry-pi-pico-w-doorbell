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
    last_state = doorbell_pin.value()
    debounce_time = 15  # Reduced from 500ms to 15ms
    consecutive_reads = 0
    required_reads = 3  # Number of consecutive readings needed to confirm
    # press

    while True:
        current_state = doorbell_pin.value()

        # Detect falling edge (button press)
        if current_state == 0 and last_state == 1:
            consecutive_reads += 1
            if consecutive_reads >= required_reads:
                print("¡Sonó el timbre!")
                await notifier.notify("¡Sonó el timbre!")
                consecutive_reads = 0
                # Debounce delay
                await uasyncio.sleep_ms(debounce_time)
        else:
            consecutive_reads = 0

        last_state = current_state
        # Reduced sleep time for faster sampling
        await uasyncio.sleep_ms(0)

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
