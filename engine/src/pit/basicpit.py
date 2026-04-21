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


class basicpit(bt.basepit):
    def __init__(self, index, seeds, prev=None, back=None, active=True):
        super().__init__(index, seeds, prev, back, active)

    def __bool__(self):
        return self["active"]

    def __iter__(self):
        return self

    def __next__(self):
        if not self.active:
            return None
        else:
            link = self.link
            while not link.active:
                if link.link is None:
                    return None
                elif link == self:
                    return self
                else:
                    link = link.link
            return link

    def __getitem__(self, index: int):
        link = self
        while i != link.index:
            if link.link is None:
                return None
            elif link.link is self:
                return None
            else:
                link = link.link
        return link

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
                    a.value = self.value
                    self.value = 0
            else:
                self.capture = False
                raise ValueError("Cannot add a negative number")
            a.link = self.link
            a.prev = self.prev
            return ret

    def __int__(self):
        if self.active:
            return self.value
        else:
            raise ValueError("Cannot convert invalid state to int")

    def __setitem__(self, index: int, value: int):
        link = self[index]
        if link is not None:
            if value <= self.reset:
                link.active = True
                link.value = value
            else:
                link.active = False
                link.value = -1

    def get(self):
        if self.active:
            value = self.value
            self.value = 0
            self.capture = False
            return value
        return None

    def isCapture(self):
        return self.capture
