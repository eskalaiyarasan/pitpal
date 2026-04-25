# factory method  for the board.

import engine.src.board.classic as classic
import engine.src.common as common
import config.interface.rule_config_database as rm

_board = None



def get_board():
    global _board
    if _board is None:
        raise common.IllegalConfiguration("No valid board found")
    return _board


def destroy():
    global _board
    if _board is None:
        return False
    _board = None
    return True


def init_board( config:rm.PitpalRuleConfig ):
    global _board
    typee = config.engine.algo
    if _board is not None:
        raise common.IllegalOperation("board is already created")
    if typee == "classic":
        _board = classic.Board.from_db(config)
    else:
        raise common.IllegalConfiguration("unknown board selected")
    return _board
