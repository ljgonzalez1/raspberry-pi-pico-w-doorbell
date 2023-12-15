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
    the Raspberry Pi Pico board. It simulates different heartbeats ('normal'
    and 'fast') to represent the board's state - whether it's idle or actively
    processing tasks. This class is especially useful for monitoring the
    board's status in real-time, providing visual feedback through LED
    patterns.

    Attributes
    ----------
    led : Pin
        The pin object from `machine.Pin` that controls the onboard LED.
    __heart_rate : str, private
        The current state of the indicator (either 'normal' or 'fast').
    running : bool
        Flag to indicate whether the indicator loop is active.

    Methods
    -------
    beat():
        Executes a heartbeat based on the current heart rate status.
    start():
        Starts the indicator loop in a separate thread.
    stop():
        Stops the indicator loop and turns off the LED.
    tachycardia():
        Sets the indicator status to 'fast' to simulate active processing.

    Notes
    -----
    The class utilizes threading to allow the heartbeat simulation to run
    asynchronously without blocking the main program execution. This is
    particularly useful in scenarios where the Raspberry Pi Pico board is
    handling multiple tasks simultaneously.

    Example
    -------
    >>> from machine import Pin
    >>> import settings
    >>> onboard_led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)
    >>> heart = Heart(onboard_led)
    >>> heart.start()  # Start the heartbeat indicator
    >>> # ... perform tasks ...
    >>> heart.stop()   # Stop the heartbeat indicator
    """

    def __init__(self, onboard_led):
        """
        Initialize the Heart object as an indicator for the Raspberry Pi Pico
        board.

        Parameters
        ----------
        onboard_led : Pin
            The pin object (from machine.Pin) that controls the onboard LED.

        Attributes
        ----------
        led : Pin
            Stores the pin object that controls the onboard LED.
        __heart_rate : str, private
            The current state of the indicator, initially set to 'normal'.
        running : bool
            Indicates whether the indicator loop is active. Set to True at
            initialization.
        """
        self.led = onboard_led
        self.__heart_rate = "normal"
        self.running = True

    def beat(self):
        """
        Executes a heartbeat based on the current heart rate status.

        This method checks the current heart rate status (normal or
        fast) and triggers the corresponding heartbeat pattern. If the heart
        rate is fast, it executes a fast heartbeat and then resets the heart
        rate to normal.

        Notes
        -----
        - This method uses the private methods `__normal_beat` and
          `__fast_beat`
          to produce the heartbeat patterns.
        - The heart rate status is modified to 'normal' after a
          'fast' beat.
        """
        if self.heart_rate == "normal":
            self.__normal_beat()

        elif self.heart_rate == "fast":
            self.__fast_beat()
            self.heart_rate = "normal"

    def __alive(self):
        """
        Continuously indicates the board is active by calling the `beat`
        method.

        This private method keeps signaling the board's activity as long as
        the 'running' attribute is True. It's used to indicate the board is
        responsive.

        Notes
        -----
        - The method will exit once the 'running' attribute is set to False.
        """
        while self.running:
            self.beat()

    def __die(self):
        """
        Turns off the onboard LED, indicating the board is no longer active.

        This private method is used to signal that the board has stopped
        functioning by turning off the onboard LED.

        Notes
        -----
        - This method is typically called when the board needs to be indicated
        as non-responsive.
        """
        self.led.off()

    def __normal_beat(self):
        print("Alive")
        for state in (0, 1, 1, 0):
            if state:
                self.led.on()

            else:
                self.led.off()

            sleep(0.02)
        self.led.on()
        sleep(0.3)

    def __fast_beat(self):
        """
        Simulates the board being actively engaged in a task.

        This private method indicates that the board is actively working by
        rapidly toggling the onboard LED.

        Notes
        -----
        - This method is typically called to indicate active processing or
        response to an external trigger.
        """
        print("Working")
        sleep_time = 0.03
        max_time = 5

        for _ in range(int(max_time / sleep_time / 2)):
            self.led.on()
            sleep(sleep_time)
            self.led.off()
            sleep(sleep_time)

        self.led.on()

    def tachycardia(self):
        """
        Sets the indicator status to 'fast'.

        This method is used to indicate that the board is actively engaged in
        a task, changing the indicator status to 'fast'. This will trigger a
        rapid LED toggle pattern.

        Notes
        -----
        - The rapid LED toggle effect is achieved through the `beat` method,
          which calls `__fast_beat` based on the indicator status.
        """
        self.heart_rate = "fast"

    @property
    def heart_rate(self):
        """
        Get the current indicator status.

        This property method returns the current status of the indicator, which
        can be either 'normal' or 'fast'.

        Returns
        -------
        str
            The current status of the indicator ('normal' or 'fast').

        Notes
        -----
        - This property provides a way to check the current operational status
          of the board as indicated by the LED.
        """
        return self.__heart_rate

    @heart_rate.setter
    def heart_rate(self, value):
        """
        Set the indicator status.

        This property setter is used to change the status of the indicator. It
        accepts either 'normal' or 'fast'. Setting the status to 'fast'
        triggers a rapid LED toggle pattern to indicate active processing or
        response.

        Parameters
        ----------
        value : str
            The desired status for the indicator ('normal' or 'fast').

        Notes
        -----
        - Changing the status to 'fast' will result in a rapid LED toggle when
          the `beat` method is called.
        - Any value other than 'fast' will set the status to 'normal',
          resulting in a regular heartbeat pattern.
        """
        if value == "fast":
            self.__heart_rate = "fast"

        else:
            self.__heart_rate = "normal"
        print(value)

    def start(self):
        """
        Starts the indicator loop in a separate thread.

        This method initiates the indicator loop, signaling the board's
        responsiveness by creating a new thread running the `__alive` method.

        Notes
        -----
        - The `__alive` method, running in the new thread, will continue as
        long as 'running' is True.
        """
        _thread.start_new_thread(self.__alive, ())

    def stop(self):
        """
        Stops the indicator loop, signaling the board is no longer active.

        This method terminates the indicator loop by setting 'running' to
        False, stopping the `__alive` method. It also calls `__die` to turn off
        the onboard LED, indicating the board is not responsive.

        Notes
        -----
        - This method should be used to cleanly indicate the board's
        non-responsiveness.
        """
        self.running = False
        self.__die()


if __name__ == '__main__':
    from machine import Pin
    import settings

    onboard_led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)

    heart = Heart(onboard_led)

    heart.__normal_beat()
    heart.__fast_beat()

