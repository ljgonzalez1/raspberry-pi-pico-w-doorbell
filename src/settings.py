"""
Module for storing configuration settings of the project.

Attributes
----------
WIFI_SSID : str
    The SSID of the WiFi network, imported from the credentials module.
WIFI_PASS : str
    The password of the WiFi network, imported from the credentials module.
TELEGRAM_PAYLOAD : str
    The message payload to be sent to Telegram.
TELEGRAM_CHAT_IDS : list
    The list of Telegram chat IDs to send messages to, imported from the
    credentials module.
TELEGRAM_BOT_TOKEN : str
    The token for the Telegram bot, imported from the credentials module.
HOST_PROTOCOL : str
    The protocol used for network communication, e.g., 'http'.
HOST_NAME : str
    The hostname or IP address of the network host to communicate with.
HOST_PORT : str
    The port number of the network host.
TARGET_PATH : str
    The path on the network host where requests are sent.
MSG_PAYLOAD : str
    The payload of the message to be sent, URL-encoded.
MSG_TITLE : str
    The title of the message to be sent, URL-encoded.
MSG_SUBJECT : str
    The subject or category of the message.
LED_PIN : str
    The identifier for the LED pin on the Raspberry Pi Pico board.
DOORBELL_PIN : int
    The GPIO pin number used for the doorbell input.
SERIAL_LOGS : bool
    Flag to enable or disable serial logging throughout the project.
ENABLE_TELEGRAM : bool
    Flag to enable or disable sending messages to Telegram.
ENABLE_NODE_RED : bool
    Flag to enable or disable sending messages to Node-RED.
"""

import credentials as secrets

WIFI_SSID = secrets.WIFI_SSID
WIFI_PASS = secrets.WIFI_PASS

TELEGRAM_PAYLOAD = "Sonó el timbre"
TELEGRAM_CHAT_IDS = secrets.TELEGRAM_CHAT_IDS
TELEGRAM_BOT_TOKEN = secrets.TELEGRAM_BOT_TOKEN

HOST_PROTOCOL = "http"
HOST_NAME = "10.0.10.4"
HOST_PORT = "1880"

TARGET_PATH = "timbre"
MSG_PAYLOAD = "Son%C3%B3%20el%20timbre"
MSG_TITLE = "%C2%A1Timbre!"
MSG_SUBJECT = "tema"

LED_PIN = "LED"
DOORBELL_PIN = 10

SERIAL_LOGS = True

ENABLE_TELEGRAM = True
ENABLE_NODE_RED = True
