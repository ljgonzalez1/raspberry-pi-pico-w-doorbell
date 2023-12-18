from machine import Pin
from utime import sleep

import settings

from heart import Heart
from messages import Messages

from logging import dprint as print

onboard_led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)
doorbell_pin = Pin(settings.DOORBELL_PIN, Pin.IN, Pin.PULL_UP)

heart = Heart(onboard_led)


def debounce(pin):
    """
    A function that sets an interrupt on a pin and waits for a specified amount
    of time before triggering the interrupt handler.

    Args:
        pin (Pin): The pin to set the interrupt on.

    Returns:
        None.

    """
    pin.irq(handler=None)

    # Calls the interrupt_handler function when an interrupt is detected on the
    # pin.
    pin.irq(trigger=Pin.IRQ_FALLING, handler=interrupt_handler)

    # Waits for a specified amount of time before triggering the interrupt
    # handler.
    sleep(0.2)

    # Resets the interrupt on the pin and sets it to trigger on a low-level
    # signal.
    pin.irq(trigger=Pin.IRQ_LOW_LEVEL, handler=debounce)


def interrupt_handler(pin):
    """
    This function is called when an interrupt is detected on the specified pin.

    Args:
        pin (Pin): The pin that generated the interrupt.

    Returns:
        None.

    """
    print(f"Interrupt detected in pin: {pin}")
    heart.off()
    messages = Messages()
    messages.send()


# If voltage is less than ~2V, sends a signal
doorbell_pin.irq(trigger=Pin.IRQ_FALLING, handler=debounce)

while True:
    for _ in heart.beat():
        sleep(0.15)
