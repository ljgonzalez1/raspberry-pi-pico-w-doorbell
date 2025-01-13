"""
Network management for MicroPython on Raspberry Pi Pico W.

Provides an asynchronous WiFiManager class to connect/disconnect from WiFi
when needed.
"""

import network
import uasyncio as asyncio
from config import settings
from utils.logging import Logger

class WiFiManager:
    """
    Manages the Wi-Fi connection using MicroPython's network module.
    Uses async/await to allow non-blocking behavior in a uasyncio environment.
    """

    def __init__(self):
        self.logger = Logger(__name__)
        self._wlan = network.WLAN(network.STA_IF)

    async def connect(self):
        """
        Connects to the Wi-Fi network specified in the settings.
        If already connected, logs a message and returns immediately.
        """
        if self._wlan.isconnected():
            self.logger.debug("WiFiManager: Already connected to Wi-Fi.")
            return

        self.logger.info("WiFiManager: Activating Wi-Fi interface...")
        self._wlan.active(True)
        self.logger.info(f"WiFiManager: Connecting to SSID '{settings.WIFI_SSID}'...")
        self._wlan.connect(settings.WIFI_SSID, settings.WIFI_PASS)

        # Intentamos conectarnos durante un número limitado de iteraciones
        for attempt in range(50):
            if self._wlan.isconnected():
                self.logger.info("WiFiManager: Successfully connected to Wi-Fi.")
                return
            self.logger.debug(f"WiFiManager: Connection attempt {attempt+1}...")
            await asyncio.sleep_ms(200)

        # Si no se conecta tras varios intentos, mostramos error
        self.logger.error("WiFiManager: Could not connect to WiFi after multiple attempts.")

    async def disconnect(self):
        """
        Disconnects from the Wi-Fi network if connected,
        then deactivates the Wi-Fi interface.
        """
        if self._wlan.isconnected():
            self.logger.debug("WiFiManager: Disconnecting from Wi-Fi...")
            self._wlan.disconnect()
        self._wlan.active(False)
        self.logger.info("WiFiManager: Wi-Fi interface deactivated.")

    def is_connected(self) -> bool:
        """
        Checks if the WLAN interface is connected to a network.

        Returns
        -------
        bool
            True if connected, False otherwise.
        """
        return self._wlan.isconnected()
