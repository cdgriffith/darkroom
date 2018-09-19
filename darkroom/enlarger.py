#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

from gpiozero import OutputDevice


class Enlarger(OutputDevice):

    def __init__(self, pin):
        super(Enlarger, self).__init__(pin, initial_value=True)
        self.printing = False
        self.print_thread = None
        self.timer_thread = None
        self.draw = None
        self.state = False
        self.off()

    def toggle(self):
        if self.printing:
            return False
        if self.state:
            self.off()
        else:
            self.on()

    def on(self):
        self.state = True
        self._write(False)

    def off(self):
        self.state = False
        self._write(True)

    def execute(self, length, draw):
        if self.printing:
            return False
        self.printing = True
        self.draw = draw
        self.timer_thread = Thread(target=self._timer, args=(length, ))
        self.print_thread = Thread(target=self._print_off, args=(length,))
        self.print_thread.setDaemon(True)
        self.timer_thread.setDaemon(True)
        self.on()
        self.print_thread.start()
        self.timer_thread.start()

    def _timer(self, length):
        initial = length
        while length > 0:
            self.draw(length)
            if not self.printing:
                self.draw(initial)
                return
            time.sleep(.2)
            length -= .2
        self.draw(initial)

    def _print_off(self, length):
        initial = length
        while length > 0:
            if not self.printing:
                self.draw(initial)
                return
            time.sleep(.1)
            length -= .1
        self.printing = False
        self.off()

    def cancel(self):
        self.off()
        self.printing = False
        self.print_thread = None
        self.timer_thread = False
