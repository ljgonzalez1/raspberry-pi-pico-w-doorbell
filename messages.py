from utime import sleep
import urequests
# import _thread
from wifi import WiFi

import settings
from logging import dprint as print


class Messages:
    class Lock:
        def __init__(self):
            self.__locked = False

        def acquire(self):
            self.__locked = True

        def release(self):
            self.__locked = False

        @property
        def is_locked(self):
            return self.__locked

    def __init__(self):
        self.lock = Messages.Lock()
        self.lock.release()

    def __send(self):
        if not self.lock.is_locked:
            print("Tomando lock")
            self.lock.acquire()
            self.__send_msg()
            print("Liberando lock")
            self.lock.release()

    def send(self):
        if not self.lock.is_locked:
            print("Creando thread")
            _thread.start_new_thread(self.__send, ())

        else:
            print("Lock ocupado por otro Thread")

    @staticmethod
    def __send_msg():
        try:
            WiFi.connect_wifi()

            # Construir la URL
            url = (f"{settings.HOST_PROTOCOL}://{settings.HOST_NAME}:" + \
                   f"{settings.HOST_PORT}" + \
                   f"/{settings.TARGET_PATH}" + \
                   f"?payload={settings.MSG_PAYLOAD}" + \
                   f"&title={settings.MSG_TITLE}" + \
                   f"&tema={settings.MSG_SUBJECT}")

            # Realizar la solicitud GET
            response = urequests.get(url)

            # Imprimir la respuesta del servidor
            print(response.text)

            response.close()

            # Desactivar wifi para ahorrar energía
            WiFi.disconnect_wifi()

        except Exception as e:
            print(f"Error al enviar mensaje: {e}")

        finally:
            # Asegurar que la conexión WiFi se cierre en caso de un error
            if WiFi.wlan.isconnected():
                WiFi.disconnect_wifi()


