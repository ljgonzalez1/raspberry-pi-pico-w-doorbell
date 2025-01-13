"""
LED heartbeat indicator module with multiple states and patterns.
"""
import uasyncio
from machine import Pin
from config import settings
from utils.logging import dprint as print


class HeartLED:
    """
    LED controller with multiple states and patterns.
    Supports normal heartbeat, fast connecting blink, and solid sending state.
    """

    STATE_NORMAL = 'normal'
    STATE_CONNECTING = 'connecting'
    STATE_SENDING = 'sending'

    def __init__(self, led_pin: Pin):
        """Initialize HeartLED with a pin."""
        self.led = led_pin
        self.current_state = self.STATE_NORMAL
        self._enabled = settings.LED_ENABLED
        self._running = True

    async def run(self):
        """Run the LED pattern based on current state."""
        if not self._enabled:
            self.off()
            return

        while self._running:
            pattern = settings.LED_PATTERNS[self.current_state]

            for state, duration in pattern['pattern']:
                if not self._running:
                    break

                self.led.value(state)

                # Print "Alive" only in normal state when turning on
                if (self.current_state == self.STATE_NORMAL and
                    state == 1):
                    print("Alive")

                await uasyncio.sleep_ms(duration)

    def set_state(self, state):
        """Change the LED state/pattern."""
        if not self._enabled:
            return

        if state in settings.LED_PATTERNS:
            self.current_state = state
        else:
            print(f"Unknown LED state: {state}")

    def off(self):
        """Turn off the LED."""
        if self._enabled:
            self.led.off()

    def stop(self):
        """Stop the LED pattern."""
        self._running = False
        self.off()
