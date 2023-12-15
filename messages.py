# TODO: Fix the documentation
"""
Module for managing and sending messages over WiFi.

This module contains the Messages class which is responsible for sending
messages via a WiFi connection.
It makes use of the settings from the `settings` module for network and
message details. The class
includes a locking mechanism to prevent concurrent message sending, ensuring
message handling is
thread-safe.

Classes
-------
Messages
    Handles the sending of messages and ensures thread-safe operations using
    a locking mechanism.

Example
-------
>>> msg = Messages()
>>> msg.send()  # Sends a message using the settings specified in the
settings module
"""
from utime import sleep
import urequests
from wifi import WiFi

import settings
from logging import dprint as print


class Messages:
    """
    A class to handle message sending over WiFi.

    This class provides functionalities to send messages over a WiFi
    network. It uses a locking mechanism
    to ensure that message sending is thread-safe and that messages are
    sent one at a time.

    Attributes
    ----------
    lock : Messages.Lock
        A lock object to ensure thread-safe operations.

    Methods
    -------
    send():
        Initiates the message sending process in a new thread.
    """

    class Lock:
        """
        A simple lock mechanism to control access to resources in a
        thread-safe manner.

        This inner class is used by the Messages class to prevent
        concurrent execution of critical sections
        of code, particularly for sending messages.

        Attributes
        ----------
        __locked : bool, private
            Indicates whether the lock is currently held or not.

        Methods
        -------
        acquire():
            Acquires the lock.
        release():
            Releases the lock.
        is_locked:
            Returns the current state of the lock.
        """
        def __init__(self):
            self.__locked = False

        def acquire(self):
            """
            Acquires the lock, setting the lock state to True.
            """
            self.__locked = True

        def release(self):
            """
            Releases the lock, setting the lock state to False.
            """
            self.__locked = False

        @property
        def is_locked(self):
            """
            Returns the current state of the lock.

            Returns
            -------
            bool
                True if the lock is currently acquired,
                False otherwise.
            """
            return self.__locked

    def __init__(self):
        """
        Initializes the Messages object with a released lock.
        """
        self.lock = Messages.Lock()
        self.lock.release()

    def send(self):
        """
        A private method to manage the sending of a message.

        This method checks if the lock is not acquired and proceeds
        to send a message. It acquires
        the lock before sending the message and releases it
        afterward to ensure thread safety.

        Notes
        -----
        - This method is intended to be called within a separate
        thread.
        """
        if not self.lock.is_locked:
            print("Taking lock")
            self.lock.acquire()
            self.__send_msg()
            print("Releasing lock")
            self.lock.release()

    @staticmethod
    def __send_msg():
        """
        A private static method to send a message using WiFi.

        This method forms the URL using settings, sends a GET
        request, and then logs the response.
        It handles WiFi connectivity and disconnection to manage
        network resources efficiently.

        Notes
        -----
        - The method captures any exceptions during the message
        sending process and logs them.
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


