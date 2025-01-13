"""
LED heartbeat indicator functionality.
"""
import uasyncio as asyncio
from machine import Pin


class HeartLED:
    def __init__(self, led_pin: Pin):
        self.led = led_pin
        self._running = True

    async def run(self):
        """Runs the heartbeat pattern."""
        while self._running:
            await self._beat_pattern()

    async def _beat_pattern(self):
        """Executes one heartbeat pattern."""
        patterns = [(0, 10), (1, 10), (1, 10), (0, 10),
                    (1, 100), (0, 400)]
        for state, duration in patterns:
            self.led.value(state)
            await asyncio.sleep_ms(duration)

    def off(self):
        """Turns off the LED."""
        self.led.off()

    def stop(self):
        """Stops the heartbeat."""
        self._running = False
