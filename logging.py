from settings import SERIAL_LOGS

if SERIAL_LOGS:
    import micropython


def dprint(*args, **kwargs):
    if SERIAL_LOGS:
        print(*args, **kwargs)


def show_mem(*args, **kwargs):
    if SERIAL_LOGS:
        micropython.mem_info(*args, **kwargs)

