"""
Node-RED notification provider implementation.
"""

import urequests
from .base import NotificationProvider
from core.network import WiFiManager
from config import settings


class NodeRedProvider(NotificationProvider):
    """
    Sends notifications to a Node-RED endpoint via HTTP GET requests.
    """

    def __init__(self):
        """
        Initializes the Node-RED provider with the configuration specified
        in settings.
        """
        self.wifi = WiFiManager()
        self.config = settings.NODE_RED_CONFIG
        self.url = (
            f"{self.config['protocol']}://"
            f"{self.config['host']}:{self.config['port']}/"
            f"{self.config['path']}"
        )
        self.connected = False

    async def connect(self):
        """
        Establishes a connection to the network using WiFiManager.
        """
        await self.wifi.connect()
        self.connected = True

    async def send(self, message: str):
        """
        Sends the message as a query parameter to the Node-RED endpoint.

        Parameters
        ----------
        message : str
            The message to send.
        """
        if not self.connected:
            await self.connect()

        try:
            # Attach message as a payload query parameter
            payload_url = f"{self.url}?payload={message}"
            response = urequests.get(payload_url)
            response.close()
        except Exception as e:
            print(f"Error sending message to Node-RED: {e}")

    async def disconnect(self):
        """
        Disconnects from the network using WiFiManager.
        """
        await self.wifi.disconnect()
        self.connected = False
