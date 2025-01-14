"""
Network manager for WiFi connections.
"""
import network
import uasyncio
from config import settings
from utils.logging import dprint as print


class NetworkManager:
    """
    Manages WiFi network connections.
    Implements singleton pattern to ensure single network instance.
    """

    _instance = None
    MAX_ATTEMPTS = 120  # 120 attempts * 0.5s = 60s total

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NetworkManager, cls).__new__(cls)
            cls._instance.wlan = network.WLAN(network.STA_IF)
            cls._instance.is_initialized = False
        return cls._instance

    def __init__(self):
        if not self.is_initialized:
            self.ssid = "CompuMundoHiperMegaRed 2.4GHz"
            self.password = "amapolas3920sinespacios"
            self.timeout = settings.WIFI_CONNECT_TIMEOUT
            self.wlan.active(True)
            self.is_initialized = True

    def _get_status_text(self, status):
        """Convierte el código de estado numérico a texto."""
        status_dict = {
            0: "IDLE",              # Sin actividad
            1: "CONNECTING",        # Intentando conectar
            2: "WRONG_PASSWORD",    # Contraseña incorrecta
            3: "NO_AP_FOUND/GOT_IP",  # No encontró AP o ya tiene IP
            4: "CONNECT_FAIL",      # Falló la conexión
            -1: "CONNECTION FAILED",
            -2: "NO MATCHING SSID IN RANGE",
            -3: "AUTH FAIL"
        }
        return f"{status} ({status_dict.get(status, 'UNKNOWN')})"

    async def _hard_reset_wifi(self):
        """Realiza un reinicio completo de la interfaz WiFi."""
        print("Realizando reinicio duro del WiFi...")

        # Desactivar completamente
        self.wlan.disconnect()
        self.wlan.active(False)
        await uasyncio.sleep(1)  # Esperar a que se limpie todo

        # Reactivar
        self.wlan.active(True)
        await uasyncio.sleep(1)  # Esperar a que se inicialice

        # Intentar nueva conexión
        print("Reconectando después del reinicio...")
        self.wlan.connect(self.ssid, self.password)
        await uasyncio.sleep(1)  # Dar tiempo para iniciar la conexión

    async def connect(self):
        """
        Connect to WiFi network with multiple attempts.

        Returns:
            bool: True if connection successful, False otherwise
        """
        if self.wlan.isconnected():
            config = self.wlan.ifconfig()
            print("\n=== Already Connected! ===")
            print(f"IP Address: {config[0]}")
            print("=======================\n")
            return True

        try:
            print(f"Connecting to WiFi network: {self.ssid}")
            self.wlan.connect(self.ssid, self.password)

            # Wait for connection with retries
            attempts = 0

            while not self.wlan.isconnected() and attempts < self.MAX_ATTEMPTS:
                attempts += 1
                current_status = self.wlan.status()
                print(f"\n--- Connection attempt {attempts}/{self.MAX_ATTEMPTS} ---")
                print(f"Active: {self.wlan.active()}")
                print(f"Initial Status: {self._get_status_text(current_status)}")

                print(self.ssid, self.password)

                # Hacer hard reset cada 15 intentos
                if attempts % 15 == 0:
                    print(f"Realizando hard reset periódico en intento {attempts}...")
                    await self._hard_reset_wifi()
                    print(f"Post-reset Status: {self._get_status_text(self.wlan.status())}")
                    print(f"Post-reset Active: {self.wlan.active()}")
                    continue

                if current_status == network.STAT_CONNECTING:
                    print(f"Still connecting... Status: {self._get_status_text(current_status)}")

                elif current_status == network.STAT_WRONG_PASSWORD:
                    print(f"Wrong password! Status: {self._get_status_text(current_status)}")
                    return False

                elif current_status == network.STAT_NO_AP_FOUND:
                    print(f"Network not found! Status: {self._get_status_text(current_status)}")
                    return False

                elif current_status == network.STAT_CONNECT_FAIL:
                    print(f"Connection failed! Status: {self._get_status_text(current_status)}")
                    print("MAC Address:", ":".join(["{:02x}".format(b) for b in self.wlan.config('mac')]))
                    try:
                        print("RSSI:", self.wlan.status('rssi'))
                        print("Channel:", self.wlan.config('channel'))

                    except:
                        pass
                    self.wlan.connect(self.ssid, self.password)

                elif current_status == network.STAT_GOT_IP:
                    print(f"Got IP! Status: {self._get_status_text(current_status)}")

                await uasyncio.sleep(0.5)

                # Estado después del intento
                final_status = self.wlan.status()
                print(f"End of attempt status: {self._get_status_text(final_status)}")
                print(f"Interface active: {self.wlan.active()}")
                print("-----------------------------------")

            if self.wlan.isconnected():
                config = self.wlan.ifconfig()
                print("\n=== WiFi Connected Successfully! ===")
                print(f"IP Address: {config[0]}")
                print(f"Subnet Mask: {config[1]}")
                print(f"Gateway: {config[2]}")
                print(f"DNS Server: {config[3]}")
                print("\n=== Additional Info ===")
                print("MAC Address:", ":".join(["{:02x}".format(b) for b in self.wlan.config('mac')]))
                print("Channel:", self.wlan.config('channel'))
                print("RSSI (Signal Strength):", self.wlan.status('rssi'), "dBm")
                print("SSID:", self.wlan.config('ssid'))
                print("============================\n")
                return True
            else:
                print(f"\n=== Connection Failed! ===")
                print(f"Final Status: {self._get_status_text(self.wlan.status())}")
                print(f"Total Attempts: {attempts}/{self.MAX_ATTEMPTS}")
                try:
                    print("Last Known Channel:", self.wlan.config('channel'))
                    print("MAC Address:", ":".join(["{:02x}".format(b) for b in self.wlan.config('mac')]))
                except:
                    pass
                print("========================\n")
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