from machine import Pin
from utime import sleep, ticks_ms, ticks_diff
import gc

import settings

from heart import Heart
from messages import Messages

from logging import dprint as print, show_mem as mem_info

onboard_led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)
doorbell_pin = Pin(settings.DOORBELL_PIN, Pin.IN, Pin.PULL_UP)

heart = Heart(onboard_led)
msg = Messages()

def pin_handler(pin):
    heart.tachycardia()
    print(f"Interrupción detectada en pin {pin}")

    sleep(0.1)

    Messages.send_msg()


def read_intl(pin):
    # If voltage is less than 2V, sends a signal
    if not pin.value():
        pin_handler(pin)


def polling(pin, iters=10):
    for _ in range(iters):
        read_intl(pin)
        sleep(0.001)


while True:
    heart.beat()
    polling(doorbell_pin, 2000)

