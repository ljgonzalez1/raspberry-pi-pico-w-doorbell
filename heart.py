"""
Module for simulating heartbeats using an onboard LED on a Raspberry Pi Pico
board.

This module contains the Heart class, which controls an LED to indicate the
operational status of a Raspberry Pi Pico board.

Classes
-------
Heart
    A class to represent an activity and status indicator for the Raspberry Pi
    Pico board using an LED.

Example
-------
from machine import Pin
import settings
from utime import sleep

onboard_led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)
heart = Heart(onboard_led)

# Simulate heartbeats
for _ in range(10):
    for _ in heart.beat():
        for _ in range(2000):
            sleep(0.001)
"""

from utime import sleep

from logging import dprint as print


class Heart:
    """
    A class to represent an activity and status indicator for the Raspberry Pi
    Pico board using an LED.

    The `Heart` class uses an onboard LED to indicate the operational status of
    the Raspberry Pi Pico board. It simulates a heartbeat pattern to represent the board's activity.
    This class is useful for monitoring the board's status in real-time, providing visual feedback
    through LED patterns.

    Attributes
    ----------
    led : Pin
        The pin object from `machine.Pin` that controls the onboard LED.

    Methods
    -------
    beat():
        Executes a heartbeat pattern. This method is a generator that yields LED states.
    on():
        Turns the LED on.
    off():
        Turns the LED off.

    Example
    -------
    >>> from machine import Pin
    >>> import settings
    >>> onboard_led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)
    >>> heart = Heart(onboard_led)
    >>> for _ in range(10):
    ...     for _ in heart.beat():
    ...         for _ in range(2000):
    ...             sleep(0.001)  # Simulate heartbeats
    """

    def __init__(self, onboard_led):
        """
        Initialize the Heart object as an indicator for the Raspberry Pi Pico board.

        Parameters
        ----------
        onboard_led : Pin
            The pin object (from machine.Pin) that controls the onboard LED.
        """
        self.led = onboard_led

    def beat(self):
        """
        Executes a heartbeat pattern.

        This method is a generator that yields a sequence of LED
        states to simulate a heartbeat pattern.
        The pattern is a simple representation of the board's activity.

        Yields
        ------
        None
            Used to control the LED states in a loop.
        """

        print("Alive")
        for state in (0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1):
            for i in range(3):
                if state:
                    self.on()

                else:
                    self.off()

                sleep(0.01)
                yield

    def off(self):
        """
        Turns the LED off.
        """
        self.led.off()

    def on(self):
        """
        Turns the LED on.
        """
        self.led.on()


if __name__ == '__main__':
    from machine import Pin
    import settings

    onboard_led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)

    heart = Heart(onboard_led)

    for _ in range(10):
        for _ in heart.beat():
            for _ in range(2000):
                sleep(0.001)
