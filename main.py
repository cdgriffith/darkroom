#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import os
from threading import Thread, Lock

from pynput import keyboard
# from PIL import ImageFont
# from luma.core.interface.serial import spi, noop
# from luma.core.render import canvas
# from luma.led_matrix.device import max7219
# from luma.core.legacy.font import proportional, LCD_FONT
#
# serial = spi(port=0, device=0, gpio=noop())
# device = max7219(serial, cascaded=4, block_orientation=0) # may be 90 or -90
#
# font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'lato' 'Lato-Regular.ttf'))
# font = ImageFont.truetype(font_path, 12)
# font = proportional(LCD_FONT)

action_lock = Lock()
focus = False
timer = 10.1
capture_mode = False


def display(text):
    with canvas(device) as draw:
        draw.text((0, 0), text, font=font, fill="white")


def toggle_focus():
    global focus
    with action_lock:
        focus = not focus


def print_light():
    pass


def cancel():
    global focus
    focus = False
    power_off()


def power_off():
    pass


def power_on():
    pass


actions = {
    "7": toggle_focus
}


def on_release(key):
    if capture_mode:
        # only update timer
        pass
    if not getattr(key, "char", None):
        pass
    else:
        if key.char == '5':
            print('oh')

    # Key.home == 7
    # Key.up == 8
    # Key.page_up == 9
    # Key.left == 4
    # Key.<12> == 5
    # Key.right == 6
    # Key.end == 1
    # Key.down == 2
    # Key.page_down == 3
    # Key.insert = 0
    # Key.delete = .


    print('{0} released'.format(key))
    # if key == keyboard.Key.esc:
    #     # Stop listener
    #     return False




if __name__ == '__main__':
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()