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


def pin_handler(pin):
    print(f"Interrupción detectada en pin {pin}")
    heart.off()
    messages = Messages()
    messages.send()


def read_intl(pin):
    # If voltage is less than 2V, sends a signal
    if not pin.value():
        pin_handler(pin)


while True:
    for _ in heart.beat():
        for __ in range(300):
            read_intl(doorbell_pin)
            sleep(0.0005)
