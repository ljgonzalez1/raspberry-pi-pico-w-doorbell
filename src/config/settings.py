"""
Settings module for application configuration.
"""
import credentials as creds

# Hardware Configuration
LED_PIN = "LED"
DOORBELL_PIN = 21
LED_ENABLED = True

# Network Configuration
WIFI_SSID = creds.WIFI_SSID
WIFI_PASS = creds.WIFI_PASS
WIFI_CONNECT_TIMEOUT = 10  # seconds

# LED Patterns (state, duration_ms)
LED_PATTERNS = {
    'normal': {
        'pattern': [(0, 300), (1, 300)],
        'repetitions': 1
    },
    'connecting': {
        'pattern': [(0, 75), (1, 75)],
        'repetitions': 1
    },
    'sending': {
        'pattern': [(1, 1000)],
        'repetitions': 1
    }
}

# Provider Specific Settings
PROVIDER_TELEGRAM_ENABLED = True
TELEGRAM_BOT_TOKEN = creds.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_IDS = creds.TELEGRAM_CHAT_IDS
TELEGRAM_MESSAGE = "Doorbell rang!"

PROVIDER_NODE_RED_ENABLED = True
NODE_RED_CONFIG = {
    'protocol': 'http',
    'host': creds.NODE_RED_HOST,
    'port': creds.NODE_RED_PORT,
    'path': 'doorbell',
    'payload': 'Doorbell%20rang!',
    'title': 'Doorbell%20Alert',
    'subject': 'alert'
}

PROVIDER_SIMPLE_GET_ENABLED = True
SIMPLE_GET_CONFIG = {
    'host': creds.SIMPLE_GET_HOST,
    'port': creds.SIMPLE_GET_PORT
}

# Debug Configuration
SERIAL_LOGS = True

# Twilio WhatsApp Configuration
PROVIDER_TWILIO_WHATSAPP_ENABLED = True
TWILIO_WHATSAPP_CONFIG = {
    'account_sid': creds.TWILIO_ACCOUNT_SID,
    'auth_token': creds.TWILIO_AUTH_TOKEN,
    'from_number': creds.TWILIO_WHATSAPP_FROM,
    'to_numbers': creds.TWILIO_WHATSAPP_TO
}

# Twilio SMS Configuration
PROVIDER_TWILIO_SMS_ENABLED = True
TWILIO_SMS_CONFIG = {
    'account_sid': creds.TWILIO_ACCOUNT_SID,
    'auth_token': creds.TWILIO_AUTH_TOKEN,
    'from_number': creds.TWILIO_FROM_PHONE,
    'to_numbers': creds.TWILIO_TO_PHONES
}

# Slack Configuration
PROVIDER_SLACK_ENABLED = True
SLACK_WEBHOOK_URLS = creds.SLACK_WEBHOOK_URLS

# Discord Configuration
PROVIDER_DISCORD_ENABLED = True
DISCORD_WEBHOOK_URLS = creds.DISCORD_WEBHOOK_URLS

# Pushover Configuration
PROVIDER_PUSHOVER_ENABLED = True
PUSHOVER_CONFIG = {
    'token': creds.PUSHOVER_TOKEN,
    'user_keys': creds.PUSHOVER_USER_KEYS
}
