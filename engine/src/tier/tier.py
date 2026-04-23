import engine.src.common as common
import engine.src.tier.pod as pod
import engine.src.tier.pro as pro

_tier = None


def get_tier():
    global _tier
    if _tier is None:
        raise common.IllegalConfiguration("No valid board found")
    return _tier


def destroy():
    global _tier
    if _tier is None:
        return False
    _tier = None
    return True


def init_tier(typee, config):
    global _tier
    if _tier is not None:
        raise common.IllegalOperation("board is already created")
    if typee == "pro":
        _tier = pro.tier.from_db(config)
    if typee == "pod":
        _tier = pod.tier.from_db(config)
    else:
        raise common.IllegalConfiguration("unknown board selected")
    return _tier
