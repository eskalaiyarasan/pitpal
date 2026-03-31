from utils.events.event_base import BaseEventClass

from utils.events.event_local import LocalEventClass
from utils.events.event_single import SingleEventClass

_data = None


def get_event():
    return _data


def init_event(a: str, args: dict):
    if "local" in a:
        _data = LocalEventClass(args["local"])
    else:
        _data = SingleEventClass()
    return _data
