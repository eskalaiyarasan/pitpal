import engine.src.common as common
import engine.src.mode.one as one
import engine.src.mode.plus as plus
import engine.src.mode.power as power
import engine.src.mode.square as square

_mode = None


def get_mode():
    global _mode
    if _mode is None:
        raise common.IllegalConfiguration("No valid board found")
    return _mode


def destroy():
    global _mode
    if _mode is None:
        return False
    _mode = None
    return True


def init_mode(typee, config):
    global _mode
    if _mode is not None:
        raise common.IllegalOperation("mode is already created")
    elif typee == "one":
        _mode = one.mode.from_db(config)
    elif typee == "plus":
        _mode = plus.mode.from_db(config)
    elif typee == "square":
        _mode = square.mode.from_db(config)
    elif typee == "power":
        _mode = power.mode.from_db(config)
    else:
        raise common.IllegalConfiguration(f"unknown board selected mode = {typee}")
    return _mode
