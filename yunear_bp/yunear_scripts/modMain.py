# -*- coding: utf-8 -*-

from .yunear.core import Yunear
from .yunear.event_bus import EventBus

from .common import const


@Yunear(const.mod_name, const.version)
class YunearMod(EventBus):
    pass
