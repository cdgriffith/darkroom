#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import time
from threading import Thread

from pynput import keyboard
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219

from darkroom.enlarger import Enlarger

from PIL import ImageFont

font_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 'fonts',
                 'scoreboard.ttf'))
font = ImageFont.truetype(font_path, 10)

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90)

timer = 0.0
set_timer_mode = False
set_timer_capture = ""


enlarger = Enlarger(pin=18)


def display(text):
    with canvas(device) as draw:
        draw.text((0, -1), text, font=font, fill="white")


def display_time(number):
    d = Thread(target=display, args=("{:.1f}".format(number).zfill(4),))
    d.setDaemon(True)
    d.start()


def print_light():
    enlarger.execute(timer, draw=display_time)


def add(amount=.1):
    global timer
    timer += amount
    if timer >= 100:
        timer = 99.9
    display_time(timer)


def rem(amount=.1):
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
            set_timer_capture = ''
            display("error")
            time.sleep(1)
            display_time(timer)
            return
        else:
            set_timer_capture = ''
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
    set_timer_capture = ''


def on_press(key):
    if enlarger.printing:
        return
    actions = {
        '+': add,
        '-': rem
    }
    stringed = str(key).strip("'")

    if stringed in actions:
        return actions[stringed]()


def on_release(key):
    global set_timer_capture
    actions = {
        'Key.enter': print_light,
        '/': enlarger.toggle,
        'Key.backspace': cancel,
        '*': set_timer_mode_toggle
    }
    stringed = str(key).strip("'")

    if stringed == 'Key.backspace':
        cancel()
        return

    if enlarger.printing:
        return

    if set_timer_mode:
        if stringed in '.0123456789':
            set_timer_capture += stringed
            display(set_timer_capture + "*")
            return
        elif stringed in '.,':
            set_timer_capture += "."
            display(set_timer_capture + "*")
            return
        elif stringed == 'Key.enter' or stringed == '*':
            set_timer_mode_toggle()
            return
        else:
            try:
                key.char
            except AttributeError:
                pass
            else:
                if str(key.char).startswith('5'):
                    set_timer_capture += '5'
                    return
    elif stringed in actions:
        return actions[stringed]()


if __name__ == '__main__':
    print("Starting at ")
    display("LOVE U")
    time.sleep(4)
    display_time(timer)
    try:
        with keyboard.Listener(on_press=on_press,
                               on_release=on_release) as listener:
            listener.join()
    finally:
        display("------")
