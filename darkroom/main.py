#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from threading import Thread


from pynput import keyboard
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy.font import proportional, LCD_FONT
import simpleaudio as sa

from darkroom.enlarger import Enlarger

# from PIL import ImageFont
# font_path = os.path.abspath(
# os.path.join(os.path.dirname(__file__), 'fonts', 'lato' 'Lato-Regular.ttf'))
# font = ImageFont.truetype(font_path, 12)

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=0)  # may be 90 or -90


timer = 0.0
set_timer_mode = False
set_timer_capture = ""


enlarger = Enlarger(pin=1)


def display(text, font=proportional(LCD_FONT)):
    with canvas(device) as draw:
        draw.text((0, 0), text, font=font, fill="white")


def print_light():
    enlarger.execute(timer)


def add(amount=1):
    global timer
    timer += amount
    if timer >= 100:
        timer = 99.9
    display("{:.1f}".format(timer).zfill(4))


def rem(amount=1):
    global timer
    timer -= amount
    if timer < 0.0:
        timer = 0.0
    display("{:.1f}".format(timer).zfill(4))


def set_timer(length):
    global timer
    if 0 >= length >= 100:
        print('Bad Length')
        return
    timer = length
    display("{:.1f}".format(timer).zfill(4))


def set_timer_mode_toggle():
    global set_timer_mode, timer
    if set_timer_mode:
        try:
            new_timer = float(set_timer_capture)
        except ValueError:
            print("Bad timer value")
            # blink or something
            return
        else:
            if 0 >= new_timer > 100:
                timer = new_timer
            else:
                print("Bad timer value")
    else:
        pass
        # start blinking
    set_timer_mode = not set_timer_mode


def audio(file):
    wave_obj = sa.WaveObject.from_wave_file(file)
    audio_thread = Thread(target=wave_obj.play)
    audio_thread.setDaemon(True)
    audio_thread.start()


def on_release(key):
    global set_timer_capture
    actions = {
        'Key.enter': print_light,
        '/': enlarger.toggle,
        '+': add,
        '-': rem,
        'Key.backspace': enlarger.cancel,
        '*': set_timer_mode_toggle
    }
    stringed = str(key).strip("'")

    if stringed in actions:
        return actions[stringed]()

    if set_timer_mode:
        converts = {
            'Key.page_up': '9',
            'Key.up': '8',
            'Key.home': '7',
            'Key.right': '6',
            '<12>': '5',
            'Key.left': '4',
            'Key.page_down': '3',
            'Key.down': '2',
            'Key.end': '1',
            'Key.insert': '0',
            'Key.delete': '.',
        }
        if stringed in converts:
            set_timer_capture += converts[stringed]
            return
        if stringed in '.0123456789':
            set_timer_capture += stringed
            return

    print('Unknown key {}'.format(key))


if __name__ == '__main__':
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
