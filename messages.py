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
"""
from utime import sleep
import urequests
from wifi import WiFi

import settings
from logging import dprint as print


class Messages:
    def send(self):
        self.__send_node_red_message()
        self.__send_telegram_message():

    def __send_telegram_message(self):
        pass

    def __send_node_red_message(self):
        def send_node_red():
            url = (f"{settings.HOST_PROTOCOL}://{settings.HOST_NAME}:" + \
                   f"{settings.HOST_PORT}" + \
                   f"/{settings.TARGET_PATH}" + \
                   f"?payload={settings.MSG_PAYLOAD}" + \
                   f"&title={settings.MSG_TITLE}" + \
                   f"&tema={settings.MSG_SUBJECT}")

            response = urequests.get(url)

            print(response.text)

            response.close()

        self.try_send_message(send_node_red)

    @staticmethod
    def try_send_message(send_message_func):
        try:
            WiFi.connect_wifi()

            send_message_func()

            # Deactivate WiFi to save energy
            WiFi.disconnect_wifi()

        except Exception as e:
            print(f"Error al enviar mensaje: {e}")

        finally:
            if WiFi.wlan.isconnected():
                WiFi.disconnect_wifi()

            return