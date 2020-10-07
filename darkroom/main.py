#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time

from luma.core.interface.serial import noop, spi
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from PIL import ImageFont
from pynput import keyboard

from darkroom.enlarger import Enlarger

X_OFFSET = int(os.getenv('X_OFFSET', 0))
Y_OFFSET = int(os.getenv('Y_OFFSET', -2))
BLOCK_DIR = int(os.getenv('BLOCK_DIR', -90))
ENLARGER_PIN = int(os.getenv('ENLARGER_PIN', 18))
STARTUP_MESSAGE = os.getenv('STARTUP_MESSAGE', 'LOVE U')
FONT_FILE = os.getenv('FONT_FILE', os.path.join(os.path.dirname(__file__), "fonts", "scoreboard.ttf"))

font_path = os.path.abspath(FONT_FILE)

font = ImageFont.truetype(font_path, 10)

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=BLOCK_DIR)

timer = 0.0
set_timer_mode = False
set_timer_capture = ""


enlarger = Enlarger(pin=ENLARGER_PIN)


def display(text):
    with canvas(device) as draw:
        draw.text((X_OFFSET, Y_OFFSET), text, font=font, fill="white")


def display_time(number):
    display("{:.1f}".format(number).zfill(4))


def print_light():
    enlarger.execute(timer, draw=display_time)


def add(amount=0.1):
    global timer
    timer += amount
    if timer >= 100:
        timer = 99.9
    display_time(timer)


def rem(amount=0.1):
    global timer
    timer -= amount
    if timer < 0.0:
        timer = 0.0
    display_time(timer)


def set_timer_mode_toggle():
    global set_timer_mode, timer, set_timer_capture
    if set_timer_mode:
        try:
            new_timer = float(set_timer_capture)
        except ValueError as err:
            print("Bad timer value {}".format(err))
            set_timer_capture = ""
            display("error")
            time.sleep(1)
            display_time(timer)
            return
        else:
            set_timer_capture = ""
            if 100 > new_timer >= 0:
                timer = new_timer
                display_time(timer)
            else:
                display("error")
                time.sleep(1)
                display_time(timer)
                print("Bad timer value: {}".format(new_timer))
    else:
        display("Enter*")
    set_timer_mode = not set_timer_mode


def cancel():
    global set_timer_mode, set_timer_capture
    enlarger.cancel()
    set_timer_mode = False
    display_time(timer)
    set_timer_capture = ""


def on_press(key):
    if enlarger.printing:
        return
    actions = {"+": add, "-": rem}
    stringed = str(key).strip("'")

    if stringed in actions:
        return actions[stringed]()


def on_release(key):
    global set_timer_capture
    actions = {
        "Key.enter": print_light,
        "/": enlarger.toggle,
        "Key.backspace": cancel,
        "*": set_timer_mode_toggle,
    }
    stringed = str(key).strip("'")

    if stringed == "Key.backspace":
        cancel()
        return

    if enlarger.printing:
        return

    if set_timer_mode:
        if stringed in ".0123456789":
            set_timer_capture += stringed
            display(set_timer_capture + "*")
            return
        elif stringed in ".,":
            set_timer_capture += "."
            display(set_timer_capture + "*")
            return
        elif stringed == "Key.enter" or stringed == "*":
            set_timer_mode_toggle()
            return
        else:
            try:
                key.char
            except AttributeError:
                pass
            else:
                if str(key.char).startswith("5") or key.char is None:
                    set_timer_capture += "5"
                    display(set_timer_capture + "*")
                    return
    elif stringed in actions:
        return actions[stringed]()


def main():
    display(STARTUP_MESSAGE)
    time.sleep(4)
    display_time(timer)
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    finally:
        display("------")


if __name__ == "__main__":
    main()
