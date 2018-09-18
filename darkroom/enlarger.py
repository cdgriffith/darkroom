#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

from gpiozero import OutputDevice


class Enlarger(OutputDevice):

    def __init__(self, pin, *args, **kwargs):
        super(Enlarger, self).__init__(pin, *args, **kwargs)
        self.printing = False
        self.print_thread = None

    def toggle(self):
        if self.printing:
            return False
        self.toggle()

    def execute(self, length):
        self.printing = True
        self.print_thread = Thread(target=self._print_off, args=(length,))
        self.print_thread.setDaemon(True)
        self.on()
        self.print_thread.start()

    def _print_off(self, length):
        if 0 >= length >= 100:
            print('Bad Length')
            return
        while length > 0:
            if not self.printing:
                return
            time.sleep(.1)
            length -= .1
        self.printing = False
        self.off()

    def cancel(self):
        self.off()
        self.printing = False
        self.print_thread = None
