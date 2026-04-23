#!/usr/bin/env python3
# Copyright (C) 2026 Pitpal
#
# This file is part of PitPal.
#
#
# PitPal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
#    Author    :  Kalaiyarasan Es
#    File name :  pitpal/engine/src/_board.py
#    Date      :  02/03/2026
#######################################################################
import copy

import engine.src.board.abstractboard as abx
import engine.src.common as common
import engine.src.pit.basicpit as basic
import engine.src.pit.kingzpit as king
import engine.src.pit.modpit as modd
import utils.events.event as event
import utils.jsonUtils.pitpal_json_schema_utils as Jsu
import utils.logging.pitpal_logger as pl


def create_pit(index, seeds, typee, prev, back, special, notifyy):
    seeds = 0 if special else seeds

    if typee["Type"] == "normalPlus":
        value = typee["Value"]
        if special:
            return modd.modpit(index, seeds, king.kingzpit, value, notifyy, prev, back)
        else:
            return modd.modpit(index, seeds, basic.basicpit, value, notifyy, prev, back)
    elif special:
        return king.kingzpit(index, seeds, prev, back)
    else:
        return basic.basicpit(index, seeds, prev, back)


class Board(abx.baseboard):
    def __init__(self, pits_per_side, n_side, n_seeds, pit_type, special_pits=None):
        self.pits_per_side = pits_per_side
        self.n_side = n_side
        self.n_seeds = n_seeds
        self.pit_type = pit_type
        self.special_pits = special_pits if special_pits is not None else []
        self.logger = pl.PitPalLogger.get_logger()
        self.ippo = self.n_side
        self.anumathi = False
        self.ippo_guzhi = None
        self.thodair = False
        # Calculate Total Seeds based on your logic:
        # Total = (Total potential pits) - (special pits that start empty)
        # We multiply by nSeeds because special pits start with 0 instead of nSeeds.
        self.total_seeds = (n_side * pits_per_side * n_seeds) - (
            len(self.special_pits) * n_seeds
        )

        # Build the nested structure: sides -> pits
        try:
            self.event = event.get_event()
            self.sides = self._build_board()
            self.state = abx.State.READY
        except Exception as e:
            self.logger.fatal(f"Failed to create board: {e}")
            self.state = abx.State.ERR

    def _mod_notify(self, index, modv):
        self.logger.info(f"notify/board: mod notify {index} : {modv}")
        try:
            self.event.notify("mod", index, modv)
        except Exception as e:
            self.logger.error(f"notify/board: mod notify {index} : {modv}")

    def _build_board(self):
        board_structure = []
        pit_counter = 0
        first = None
        nextt = None

        for side_index in range(self.n_side):
            current_side = []
            for i in range(self.pits_per_side):
                # If the current pit index is in special_pits, it starts with 0 seeds
                special = True if pit_counter in self.special_pits else False
                k = side_index * self.n_side + i
                nextt = create_pit(
                    k,
                    self.n_seeds,
                    self.pit_type,
                    None,
                    nextt,
                    special,
                    self._mod_notify,
                )
                current_side.append(nextt)
                pit_counter += 1
                if first == None:
                    first = nextt
            board_structure.append(current_side)
        if pit_counter > 0:
            first.link = nextt
        return board_structure

    @classmethod
    def from_json(cls, data):
        """Builds the Board object from the JSON schema dictionary."""
        jsu = Jsu.JSU(
            schema_file="engine/rules/schema/board.schema.json", json_data=data
        )
        if not jsu.validate():
            raise common.IllegalConfiguration(f"bad board config: {data}")
            return None
        return cls(
            pits_per_side=data["pitsPerSide"],
            n_side=data["nSide"],
            n_seeds=data["nSeeds"],
            pit_type=data["pitType"],
            special_pits=data.get("specialPits", []),
        )

    def options(self, side):
        if (side < 0) or (side >= self.n_side) or (self.ippo == side):
            return None
        ret = []
        for guzhi in self.sides[side]:
            try:
                kaai = int(guzhi)
                if kaai > 0:
                    ret.append(guzhi.index)
            except Exception as e:
                continue
        if len(ret) == 0:
            self.state = abx.State.GAMEOVER
            return None
        self.ippo = side
        self.anumathi = True
        self.ippo_guzhi = None
        return ret

    def relay(self):
        ret = [False, None]
        if not self.thodair:
            return ret
        self.thodair = False
        try:
            self.ippo_guzhi = next(self.ippo_guzhi)
            ret = self._go()
        except Exception as e:
            self.logger.error(f"exception/relay:{self.ippo}:{e}")
            return [True, 0]
        return ret

    def _check_side(self, index):
        # check index is belong to side.
        for guzhi in self.sides[self.ippo]:
            if (index == guzhi.index) and (int(guzhi) > 0):
                self.ippo_guzhi = guzhi
                return True
        return False

    def move(self, index):
        self.thodair = False
        ret = super().move(index)
        if not (self.anumathi and ret[0]):
            return [False, None]
        try:
            if not self._check_side(index):
                ret = [False, None]
            else:
                ret = self._go()
        except Exception as e:
            self.logger.error(f"exception/move:{self.ippo}:{e}")
            return [True, 0]
        return ret

    def _go(self):
        kai = copy.copy(self.ippo_guzhi)
        rett = True
        while not rett:
            self.ippo_guzhi = next(self.ippo_guzhi)
            rett = self.ippo_guzhi + kai
        if self.ippo_guzhi.isCapture():
            ret = self.ippo_guzhi.get()
            if ret > 0:
                self.thodair = True
            else:
                self.thodair = False
            return [True, ret]
        else:
            self.thodair = False
            return [True, 0]
