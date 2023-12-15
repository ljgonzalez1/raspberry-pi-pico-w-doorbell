"""
Module for storing configuration settings of the project.

This module contains various configuration constants used throughout the project. These include network settings for message communication, GPIO pin configurations for the Raspberry Pi Pico board, and a flag for enabling or disabling serial logging.

Configuration settings are used by various modules to ensure consistent and centralized management of these values, facilitating easier adjustments and maintenance.

Attributes
----------
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

Example
-------
To use a setting in another module:
>>> import settings
>>> print(settings.HOST_NAME)
'10.0.10.4'
"""

HOST_PROTOCOL = "http"
HOST_NAME = "10.0.10.4"
HOST_PORT = "1880"

TARGET_PATH="timbre"
MSG_PAYLOAD="Son%C3%B3%20el%20timbre"
MSG_TITLE="%C2%A1Timbre!"
MSG_SUBJECT="tema"

LED_PIN="LED"
DOORBELL_PIN=10

SERIAL_LOGS=False

