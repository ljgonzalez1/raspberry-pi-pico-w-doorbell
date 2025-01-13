"""
Network manager for WiFi connections.
"""
import network
import utime
from config import settings
from utils.logging import dprint as print


class NetworkManager:
    """
    Manages WiFi network connections.
    Implements singleton pattern to ensure single network instance.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NetworkManager, cls).__new__(cls)
            cls._instance.wlan = network.WLAN(network.STA_IF)
            cls._instance.is_initialized = False
        return cls._instance

    def __init__(self):
        if not self.is_initialized:
            self.ssid = settings.WIFI_SSID
            self.password = settings.WIFI_PASS
            self.timeout = settings.WIFI_CONNECT_TIMEOUT
            self.wlan.active(True)
            self.is_initialized = True

    async def connect(self):
        """
        Connect to WiFi network with multiple attempts.

        Returns:
            bool: True if connection successful, False otherwise
        """
        if self.wlan.isconnected():
            return True

        try:
            print(f"Connecting to WiFi network: {self.ssid}")
            self.wlan.connect(self.ssid, self.password)

            # Wait for connection with retries
            attempts = 0
            max_attempts = 20  # 20 intentos, cada uno con espera de 0.5s = 10s total

            while not self.wlan.isconnected() and attempts < max_attempts:
                attempts += 1
                print(f"Connection attempt {attempts}/{max_attempts}")

                status = self.wlan.status()
                if status == network.STAT_CONNECTING:
                    print("Still connecting...")
                elif status == network.STAT_WRONG_PASSWORD:
                    print("Wrong password")
                    return False
                elif status == network.STAT_NO_AP_FOUND:
                    print("Network not found")
                    return False
                elif status == network.STAT_CONNECT_FAIL:
                    print("Connection failed")
                    # Intentar reconectar
                    self.wlan.connect(self.ssid, self.password)

                await uasyncio.sleep(0.5)

            if self.wlan.isconnected():
                print("WiFi connected!")
                print(f"Network config: {self.wlan.ifconfig()}")
                return True
            else:
                print(f"Failed to connect after {max_attempts} attempts")
                return False

        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False

    def disconnect(self):
        """Disconnect from WiFi network."""
        if self.wlan.isconnected():
            try:
                self.wlan.disconnect()
                self.wlan.active(False)
                print("WiFi disconnected")
            except Exception as e:
                print(f"Disconnection error: {str(e)}")

    def is_connected(self):
        """
        Check if connected to WiFi.

        Returns:
            bool: True if connected, False otherwise
        """
        return self.wlan.isconnected()
