# TODO: Fix the documentation
"""
Module for managing and sending messages over WiFi.

This module contains functionality to send messages via a WiFi connection.
It utilizes the settings from the `settings` module for network and message details.
The module provides a straightforward approach to sending messages, managing network
connections efficiently, and handling any exceptions that might occur during the process.

Functions
---------
send():
    Sends a message using the settings specified in the settings module.

Example
-------
>>> send()  # Sends a message using the settings specified in the settings module
"""
from utime import sleep
import urequests
from wifi import WiFi

import settings
from logging import dprint as print


def send():
    """
    Sends a message using WiFi.

    This function forms the URL using settings, sends a GET request,
    and then logs the response.
    It handles WiFi connectivity and disconnection to manage network
    resources efficiently and
    captures any exceptions during the message sending process.

    Notes
    -----
    - Any exceptions encountered during message sending are logged,
    and the WiFi is disconnected
      in the finally block to ensure network resources are properly
      managed.
    """
    try:
        WiFi.connect_wifi()

        url = (f"{settings.HOST_PROTOCOL}://{settings.HOST_NAME}:" + \
               f"{settings.HOST_PORT}" + \
               f"/{settings.TARGET_PATH}" + \
               f"?payload={settings.MSG_PAYLOAD}" + \
               f"&title={settings.MSG_TITLE}" + \
               f"&tema={settings.MSG_SUBJECT}")

        response = urequests.get(url)

        print(response.text)

        response.close()

        # Deactivate WiFi to save energy
        WiFi.disconnect_wifi()

    except Exception as e:
        print(f"Error al enviar mensaje: {e}")

    finally:
        if WiFi.wlan.isconnected():
            WiFi.disconnect_wifi()

        return
