# import _thread
from utime import sleep

from logging import dprint as print


class Heart:
    def __init__(self, onboard_led):
        self.led = onboard_led
        self.__heart_rate = "normal"
        self.running = True

    def beat(self):
        if self.heart_rate == "normal":
            self.__normal_beat()

        elif self.heart_rate == "fast":
            self.__fast_beat()
            self.heart_rate = "normal"

    def __alive(self):
        while self.running:
            self.beat()

    def __die(self):
        self.led.off()

    def __normal_beat(self):
        print("Alive")
        # for state in (0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0):
        for state in (0, 1, 1, 0):
            if state:
                self.led.on()

            else:
                self.led.off()

            sleep(0.02)
        self.led.on()
        sleep(0.3)

    def __fast_beat(self):
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
        self.heart_rate = "fast"

    @property
    def heart_rate(self):
        return self.__heart_rate

    @heart_rate.setter
    def heart_rate(self, value):
        if value == "fast":
            self.__heart_rate = "fast"

        else:
            self.__heart_rate = "normal"
        print(value)

    def start(self):
        _thread.start_new_thread(self.__alive, ())

    def stop(self):
        self.running = False
        self.__die()


if __name__ == '__main__':
    from machine import Pin
    import settings

    onboard_led = Pin(settings.LED_PIN, mode=Pin.OUT, value=0)

    heart = Heart(onboard_led)

    heart.__normal_beat()
    heart.__fast_beat()

