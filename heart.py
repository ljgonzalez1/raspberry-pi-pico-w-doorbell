"""
Module for simulating heartbeats using an onboard LED on a Raspberry Pi Pico board.

This module contains the Heart class, which controls an LED to indicate the operational status of a Raspberry Pi Pico board.
The heartbeats are represented as 'normal' and 'fast' to signify the board's state, whether it's idle or actively processing tasks.
The class is particularly useful for real-time monitoring of the board's status through visual feedback provided by LED patterns.

Classes
-------
Heart
    A class to represent an activity and status indicator for the Raspberry Pi Pico board using an LED.

Example
-------
from machine import Pin
import settings

onboard_led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)
heart = Heart(onboard_led)
heart.start()  # Start the heartbeat indicator
# ... perform tasks ...
heart.stop()   # Stop the heartbeat indicator
"""

from utime import sleep
from logging import dprint as print


class Heart:
    """
    A class to represent an activity and status indicator for the Raspberry Pi
    Pico board using an LED.

    The `Heart` class uses an onboard LED to indicate the operational status of
    the Raspberry Pi Pico board. It simulates different heartbeats to represent the board's state,
    indicating whether it's idle or actively processing tasks. This class is especially useful
    for monitoring the board's status in real-time, providing visual feedback through LED patterns.

    Attributes
    ----------
    led : Pin
        The pin object from `machine.Pin` that controls the onboard LED.

    Methods
    -------
    beat():
        Executes a heartbeat pattern. This method is a generator that yields LED states.

    Example
    -------
    >>> from machine import Pin
    >>> import settings
    >>> led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)
    >>> heart = Heart(led)
    >>> for i in range(50):
    ...     [None for _ in heart.beat()]  # Simulate heartbeats
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

        This method is a generator that yields a sequence of LED states to simulate a heartbeat pattern.
        The pattern represents the operational status of the Raspberry Pi Pico board.

        Yields
        ------
        None
            Used to control the LED states in a loop.
        """
        for state in (0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1):
            for _ in range(10):
                if state:
                    self.led.on()

                else:
                    self.led.off()

                sleep(0.005)
                yield


if __name__ == '__main__':
    from machine import Pin
    import settings

    led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)

    heart = Heart(led)

    for i in range(50):
        [None for _ in heart.beat()]
