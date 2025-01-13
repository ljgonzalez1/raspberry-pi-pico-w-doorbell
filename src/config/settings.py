"""
Application settings and configuration.
"""

from . import credentials

# Hardware Configuration
LED_PIN = "LED"
DOORBELL_PIN = 21

# Network Configuration
WIFI_SSID = credentials.WIFI_SSID
WIFI_PASS = credentials.WIFI_PASS

# Notification Providers
ENABLED_PROVIDERS = [
    'telegram',
    'node_red'
]  # Add/remove as needed

# Provider-specific Settings
TELEGRAM_BOT_TOKEN = credentials.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_IDS = credentials.TELEGRAM_CHAT_IDS

NODE_RED_CONFIG = {
    'protocol': 'http',
    'host': '10.0.10.4',
    'port': '1880',
    'path': 'timbre'
}

# Other Settings
SERIAL_LOGS = True
