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

import engine.src.common as cm
import engine.src.pit.basepit as bt
import engine.src.pit.basicpit as basic
import utils.jsonUtils.pitpal_json_schema_utils as Jsu


class kingzpit(basic.basicpit):
    def __init__(self, index, seeds, prev=None, back=None, active=True):
        super().__init__(index, 0, prev, back, active)
        self.share=[]

    def __copy__(self):
        raise cm.IllegalOperation(f"KingzPit{self.index} selection not allowed")

    def __add__(self, a):
        if not isinstance(a, bt.basepit):
            raise cm.IllegalOperation("addition failed: mismatch object type ")
        ret = True
        if self.active:
            if a.value > 0:
                self.capture = False
                self.value += 1
                a.value -= 1
            elif a.value == 0:
                if self.value == 0:
                    self.capture = True
                    ret = False
                else:
                    self.capture = False
                    ret = False
            else:
                raise ValueError("Cannot be a negative number")
            a.link = self.link
            a.prev = self.prev
            return ret
    def get(self, side):
        if not self.capture:
            return [False, 0]
        while len(self.share) <= side:
            self.share.append(0)
        self.share[side] += 1
        return [True, 0]
