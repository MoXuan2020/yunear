# -*- coding: utf-8 -*-

from .singleton_meta import SingletonMeta


class EventBus(object):
    __metaclass__ = SingletonMeta

    MOD_NAME = None
    VERSION = None

    server = None
    client = None

    def init_server(self):
        pass

    def init_client(self):
        pass
