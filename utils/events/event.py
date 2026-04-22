import config.interface.event_config_database as ed

from utils.events.event_single import SingleEventClass
from utils.logging.pitpal_logger import PitPalLogger as pl

_data = None


def get_event():
    if _data is None:
        raise ValueError("event is none")
    return _data


def init_event(config: ed.PitpalEventConfig):
    param = config.param

    match param:
        case ed.SingleEventConfig():
            _data = SingleEventClass()
            pl.get_logger().info("Mode: Single. Running standalone engine logic.")

        case ed.RemoteEventConfig(ip=ip, port=port, auth=token):
            pl.get_logger().info(
                f"### work in progres # Mode: Remote. Connecting to {ip}:{port} using auth"
            )
            # Add your networking logic here

        case ed.LocalEventConfig(path=path, auth=token):
            pl.get_logger().info(
                f"### work in progres # Mode: Local. Writing events to filesystem at {path}"
            )

        case ed.CloudEventConfig(url=url, auth=token):
            pl.get_logger().info(
                f"### work in progres # Mode: Cloud. Streaming to {url} with token"
            )
            # Add your logic here

        case _:
            pl.get_logger().info("Unknown configuration type.")
