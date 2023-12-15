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


# Inicia el heartbeat en un hilo separado
# heart.start()

# last_interrupt_time = 0

def pin_handler(pin):
    # global last_interrupt_time
    # current_time = ticks_ms()

    # 1000 ms de debounce
    # if ticks_diff(current_time, last_interrupt_time) > 1000:
    # last_interrupt_time = current_time

    heart.tachycardia()
    print(f"Interrupción detectada en pin {pin}")

    sleep(0.1)

    # Envía el mensaje en un hilo separado
    # msg.send()
    Messages.__send_msg()

    # sleep(0.1)

    # else:
    #    print()
    #    print("Cooldown...")


# Si el voltaje es menor a 2V, enviar el request
# doorbell_pin.irq(trigger=Pin.IRQ_FALLING, handler=pin_handler)


def read_intl(pin):
    # Si el voltaje es menor a 2V, enviar el request
    if not pin.value():
        pin_handler(pin)


def polling(pin, iters=10):
    for _ in range(iters):
        read_intl(pin)
        sleep(0.001)


while True:
    heart.beat()
    polling(doorbell_pin, 2000)

