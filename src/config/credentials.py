"""
Credentials module for storing sensitive configuration data.
Do not commit this file without placeholder values to version control.
"""

# WiFi Configuration
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_IDS = [
    "CHAT_ID_1",
    "CHAT_ID_2"
]

# Node-RED Configuration
NODE_RED_HOST = "10.0.0.10"
NODE_RED_PORT = "1880"

# Simple GET Configuration
SIMPLE_GET_HOST = "10.0.7.10"
SIMPLE_GET_PORT = "6061"

# Twilio Configuration
TWILIO_ACCOUNT_SID = "YOUR_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_AUTH_TOKEN"

TWILIO_FROM_PHONE = "YOUR_TWILIO_PHONE"  # With country code
TWILIO_TO_PHONES = [
    "RECIPIENT_PHONE_1",  # With country code
    "RECIPIENT_PHONE_2"
]

TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"  # Twilio's WhatsApp number
TWILIO_WHATSAPP_TO = [
    "whatsapp:+1234567890"  # Recipients' WhatsApp numbers
]

# Slack Configuration
SLACK_WEBHOOK_URLS = [
    "https://hooks.slack.com/services/YOUR/WEBHOOK/URL1",
    "https://hooks.slack.com/services/YOUR/WEBHOOK/URL2"
]

# Discord Configuration
DISCORD_WEBHOOK_URLS = [
    "https://discord.com/api/webhooks/YOUR/WEBHOOK/URL1",
    "https://discord.com/api/webhooks/YOUR/WEBHOOK/URL2"
]

# Pushover Configuration
PUSHOVER_TOKEN = "YOUR_APP_TOKEN"
PUSHOVER_USER_KEYS = [
    "USER_KEY_1",
    "USER_KEY_2"
]
