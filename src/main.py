from machine import Pin
from utime import sleep

import settings

from heart import Heart
from messages import Messages

from logging import dprint as print

onboard_led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)
doorbell_pin = Pin(settings.DOORBELL_PIN, Pin.IN, Pin.PULL_UP)

heart = Heart(onboard_led)


def interrupt_handler(pin):
    print(f"Interrupt detected in pin: {pin}")
    heart.off()
    messages = Messages()
    messages.send()


# If voltage is less than ~2V, sends a signal
doorbell_pin.irq(trigger=Pin.IRQ_FALLING, handler=interrupt_handler)

while True:
    for _ in heart.beat():
        sleep(0.15)
