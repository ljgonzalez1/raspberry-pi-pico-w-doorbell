"""
Module for storing sensitive credentials.

This module contains credentials required for WiFi connectivity and Telegram
bot integration. It is used by other modules in the project that require
network access or need to interact with Telegram. The credentials are stored
as constant variables.

Important Note
--------------
The default values for the WiFi and Telegram credentials are placeholders.
Before deploying or running the
application, ensure that these values are updated with the actual credentials
for proper functionality.

Attributes
----------
WIFI_SSID : str
    The WiFi network's SSID. Default is 'CHANGEME'.
WIFI_PASS : str
    The WiFi network's password. Default is 'CHANGEME'.
TELEGRAM_CHAT_IDS : list
    A list of Telegram chat IDs where the bot will send messages.
    Replace with actual chat IDs.
TELEGRAM_BOT_TOKEN : str
    The token for the Telegram bot. Replace with an actual bot token.
"""

WIFI_SSID = "CHANGEME"
WIFI_PASS = "CHANGEME"

TELEGRAM_CHAT_IDS = [
    "-1000000000001"
]
TELEGRAM_BOT_TOKEN = "0123456789:0123456789abcdefghijklmnopqrstuvwxy"
