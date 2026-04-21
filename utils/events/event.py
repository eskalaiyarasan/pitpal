from config.interface.event_config_database import *

from utils.events.event_multi import LocalEventClass
from utils.events.event_single import SingleEventClass

_data = None


def get_event():
    return _data


def init_event(config: PitpalEventConfig):
    param = config.param

    match param:
        case SingleEventConfig(enabled=is_enabled):
            _data = SingleEventClass()
            if is_enabled:
                print("Mode: Single. Running standalone engine logic.")
            else:
                print("Mode: Single. Engine is disabled.")

        case RemoteEventConfig(ip=ip, port=port, auth=token):
            print(
                f"### work in progres # Mode: Remote. Connecting to {ip}:{port} using auth"
            )
            # Add your networking logic here

        case LocalEventConfig(path=path, auth=token):
            print(
                f"### work in progres # Mode: Local. Writing events to filesystem at {path}"
            )

        case CloudEventConfig(url=url, auth=token):
            print(f"### work in progres # Mode: Cloud. Streaming to {url} with token")
            # Add your logic here

        case _:
            print("Unknown configuration type.")
