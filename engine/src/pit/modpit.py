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
import utils.jsonUtils.pitpal_json_schema_utils as Jsu


class modpit(bt.basepit):
    def __init__(
        self, index, seeds, xtype, mod, notify, prev=None, back=None, active=True
    ):
        super().__init__(index, seeds, prev, back, active)
        x = xtype(index, seeds, prev, back, active)
        self.mod = mod
        self.notify = notify
        self.storage = x.storage
        self.core = x

    def __bool__(self):
        return self.active

    def __iter__(self):
        return self

    def __next__(self):
        return self.core.next()

    def __getitem__(self, index: int):
        return self.core[index]

    def __copy__(self):
        # Create a new instance with the same top-level values
        # Nested 'items' will still point to the same list object
        if self.value == 0:
            raise cm.IllegalOperation("Copy failed: The object is empty.")
        a = type(self)(-1, self.seeds, self.prev, self.link, self.active)
        self.value = 0
        return a

    def __add__(self, a):
        ret = True
        if not isinstance(self, bt.basepit):
            raise cm.IllegalOperation("addition failed: mismatch object type ")
        ret = self.core + a
        if self.core.value == self.mod:
            self.core.value = 0
            self.notify(self.mod)
        return ret

    def __int__(self):
        return int(self.core)

    def __setitem__(self, index: int, value: int):
        self.core[index] = value

    def get(self, side):
        return self.core.get(side)

    def isCapture(self):
        return self.capture
