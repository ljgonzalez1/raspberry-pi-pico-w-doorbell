"""
Module for managing and sending messages over WiFi.

This module contains the Messages class, which handles sending messages over a WiFi connection.
It leverages the settings from the `settings` module for network and message details. The Messages class supports
sending messages to both a Node-RED endpoint and Telegram chats. It manages network connections efficiently and handles
any exceptions that might occur during the message sending process.

Classes
-------
Messages
    Handles the process of sending messages to Node-RED and Telegram.

Example
-------
>>> messages = Messages()
>>> messages.send()  # Sends messages as per the configured settings
"""
from utime import sleep
import urequests as requests
import ujson as json
from wifi import WiFi

import settings
from logging import dprint as print


class Messages:
    """
    A class to handle the sending of messages to Node-RED and Telegram.

    This class provides functionalities to send messages to a
    Node-RED endpoint and Telegram chats.
    It manages the creation of the message, sending it, and handling
    the responses.

    Methods
    -------
    send():
        Sends messages to the configured Node-RED endpoint and
        Telegram chats.
    """

    def send(self):
        """
        Sends messages to the configured Node-RED endpoint and
        Telegram chats.

        This method iterates through the list of Telegram chat IDs
        defined in settings and sends the configured
        message to each. It also sends a message to the Node-RED
        endpoint.
        """
        if settings.ENABLE_NODE_RED:
            self.__try_send_message(self._send_node_red_message)

        if settings.ENABLE_TELEGRAM:
            for chat_id in settings.TELEGRAM_CHAT_IDS:
                self.__try_send_message(self._send_telegram_message,
                                        args=(chat_id,))

    def _send_telegram_message(self, chat_id):
        """
        Sends a message to a specified Telegram chat.

        Parameters
        ----------
        chat_id : str
            The Telegram chat ID where the message will be sent.
        """
        url = "https://api.telegram.org/" + \
              f"bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        headers = {'Content-Type': 'application/json'}
        data = {
            "chat_id": f"{chat_id}",
            "text": f"{settings.TELEGRAM_PAYLOAD}"
        }

        json_data = json.dumps(data)
        response = requests.post(url, headers=headers, data=json_data)
        self.__log_response(response)
        response.close()

    def _send_node_red_message(self):
        """
        Sends a message to the configured Node-RED endpoint.
        """
        url = f"{settings.HOST_PROTOCOL}://{settings.HOST_NAME}:" + \
              f"{settings.HOST_PORT}" + \
              f"/{settings.TARGET_PATH}" + \
              f"?payload={settings.MSG_PAYLOAD}" + \
              f"&title={settings.MSG_TITLE}" + \
              f"&tema={settings.MSG_SUBJECT}"

        response = requests.get(url)
        self.__log_response(response)
        response.close()

    @staticmethod
    def __log_response(response):
        """
        Logs the response of the message sending attempt.

        Parameters
        ----------
        response : Response
            The response object from the message sending request.
        """
        if str(response.status_code) in range(200, 300):
            print("Message sent successfully!")
            print("Response:", response.text)

        else:
            print("Failed to send message. Status code:",
                  response.status_code)

    @staticmethod
    def __try_send_message(send_message_func, args=tuple()):
        """
        Attempts to send a message using the specified function and
        arguments.

        Parameters
        ----------
        send_message_func : function
            The function to call for sending the message.
        args : tuple, optional
            Arguments to pass to the message sending function.
        """
        try:
            WiFi.connect_wifi()

            send_message_func(*args)

            # Deactivate WiFi to save energy
            WiFi.disconnect_wifi()

        except Exception as e:
            print("Error encountered:", str(e))

        finally:
            if WiFi.wlan.isconnected():
                WiFi.disconnect_wifi()

