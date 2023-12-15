import network as net
from utime import sleep

import credentials
from logging import dprint as print


class WiFi():
    WIFI_SSID = credentials.WIFI_SSID
    WIFI_PASS = credentials.WIFI_PASS
    wlan = net.WLAN(net.STA_IF)

    @staticmethod
    def connect_wifi():
        if WiFi.wlan.isconnected():
            print("Ya conectado a WiFi.")

        try:
            print("Conectando a WiFi...")
            # Conectarse a la red
            WiFi.wlan.active(True)
            WiFi.wlan.connect(WiFi.WIFI_SSID, WiFi.WIFI_PASS)

            for iters in range(500):
                if WiFi.wlan.isconnected():
                    break

                else:
                    print(f"Esperando conexión ({iters})")
                    sleep(0.05)

                if iters == 499:
                    raise Exception("Máximo de iteraciones excedido")

            print("Conexión WiFi exitosa.")
        except Exception as e:
            print(f"Error al conectar a WiFi: {e}")

    @staticmethod
    def disconnect_wifi():
        try:
            # Close the WiFi connection
            WiFi.wlan.disconnect()
            WiFi.wlan.active(False)
        except Exception as e:
            print(f"Error al desconectar WiFi: {e}")
