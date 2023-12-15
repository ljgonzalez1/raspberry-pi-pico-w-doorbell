"""
Module for managing WiFi connectivity.

This module provides the WiFi class, which offers functionalities to connect to and disconnect from a WiFi network.
It uses the WiFi credentials defined in the `credentials` module. The class is designed to be used across
different parts of the project where network connectivity is required.

Classes
-------
WiFi
    Handles WiFi connections, providing methods to connect to and disconnect from a WiFi network.

Example
-------
To establish a WiFi connection:
>>> WiFi.connect_wifi()
To disconnect from a WiFi network:
>>> WiFi.disconnect_wifi()
"""

import network as net
from utime import sleep

import credentials
from logging import dprint as print


class WiFi:
    """
    A class to manage WiFi connections.

    This class provides static methods to connect to and disconnect from
    a WiFi network.
    It uses the credentials from the `credentials` module to establish
    the connection.

    Attributes
    ----------
    WIFI_SSID : str
        The SSID of the WiFi network to connect to.
    WIFI_PASS : str
        The password of the WiFi network.
    wlan : network.WLAN
        The WLAN object for managing the WiFi connection.

    Methods
    -------
    connect_wifi():
        Connects to the WiFi network using the provided credentials.
    disconnect_wifi():
        Disconnects from the WiFi network.
    """

    WIFI_SSID = credentials.WIFI_SSID
    WIFI_PASS = credentials.WIFI_PASS
    wlan = net.WLAN(net.STA_IF)

    @staticmethod
    def connect_wifi():
        """
        Connects to the WiFi network using the provided credentials.

        This method attempts to establish a WiFi connection using
        the SSID and
        password specified in the `credentials` module. It checks
        for existing
        connections and retries the connection process for a fixed
        number of iterations.

        Raises
        ------
        Exception
            If the connection attempt exceeds the maximum number of
            iterations.
        """
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
        """
        Disconnects from the WiFi network.

        This method turns off the WiFi connection and deactivates
        the WLAN interface.

        Raises
        ------
        Exception
            If there is an error during the disconnection process.
        """
        try:
            # Close the WiFi connection
            WiFi.wlan.disconnect()
            WiFi.wlan.active(False)
        except Exception as e:
            print(f"Error al desconectar WiFi: {e}")
