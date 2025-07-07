# -*- coding: utf-8 -*-


class EventHandler(object):

    def __init__(self, event):
        self.event = event
        self.func = None
        self.mod = None

    def __call__(self, func_or_args=None):
        if not self.func:
            self.func = func_or_args

        else:
            self.func(self.mod, self.event(func_or_args))

        return self
