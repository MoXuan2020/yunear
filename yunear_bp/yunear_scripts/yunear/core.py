# -*- coding: utf-8 -*-

import inspect

import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from mod.common.mod import Mod

from .client.event.client_event import ClientEvent
from .client.event.custom.custom_client_event import CustomClientEvent
from .common import const
from .dist import Dist
from .event_handler import EventHandler
from .server.event.custom.custom_server_event import CustomServerEvent
from .server.event.server_event import ServerEvent


class Yunear(Mod):

    def __init__(self, name, version=None, dist=Dist.both):
        self.name = name
        self.version = version
        self.dist = dist

    def __call__(self, cls):
        cls.MOD_NAME = self.name
        cls.VERSION = self.version

        if self.dist == Dist.both or self.dist == Dist.server:
            cls.init_server = init_server

        if self.dist == Dist.both or self.dist == Dist.client:
            cls.init_client = init_client

        return self.Binding(cls.MOD_NAME, cls.VERSION)(cls)


@Yunear.InitServer()
def init_server(mod):
    mod.server = serverApi.RegisterSystem(
        mod.MOD_NAME, const.server_name, const.server_cls_path % mod.__module__.split(".")[0]
    )

    event_handler_list = inspect.getmembers(
        mod, lambda member: isinstance(member, EventHandler) and issubclass(member.event, ServerEvent)
    )
    if not event_handler_list:
        return

    engine_namespace = serverApi.GetEngineNamespace()
    engine_system_name = serverApi.GetEngineSystemName()

    for _, event_handler in event_handler_list:
        event_handler.mod = mod

        if issubclass(event_handler.event, CustomServerEvent):
            mod.server.ListenForEvent(
                mod.MOD_NAME, const.client_name, event_handler.event.__name__, mod, event_handler.func
            )

        else:
            mod.server.ListenForEvent(
                engine_namespace, engine_system_name, event_handler.event.__name__, mod, event_handler.func
            )


@Yunear.InitClient()
def init_client(mod):
    mod.client = clientApi.RegisterSystem(
        mod.MOD_NAME, const.client_name, const.client_cls_path % mod.__module__.split(".")[0]
    )

    event_handler_list = inspect.getmembers(
        mod, lambda member: isinstance(member, EventHandler) and issubclass(member.event, ClientEvent)
    )
    if not event_handler_list:
        return

    engine_namespace = clientApi.GetEngineNamespace()
    engine_system_name = clientApi.GetEngineSystemName()

    for _, event_handler in event_handler_list:
        event_handler.mod = mod

        if issubclass(event_handler.event, CustomClientEvent):
            mod.client.ListenForEvent(
                mod.MOD_NAME, const.server_name, event_handler.event.__name__, mod, event_handler.func
            )

        else:
            mod.client.ListenForEvent(
                engine_namespace, engine_system_name, event_handler.event.__name__, mod, event_handler.func
            )
