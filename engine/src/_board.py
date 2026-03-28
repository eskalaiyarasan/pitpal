#!/usr/bin/env python3
# Copyright (C) 2026 Pitpal
#
# This file is part of PitPal.
#
# PitPal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# either version 3 of the License, or (at your option) any later version.
#
# PitPal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PitPal. If not, see <https://www.gnu.org/licenses/>.
#    Author    :  Kalaiyarasan Es
#    File name :  pitpal/engine/src/_board.py
#    Date      :  02/03/2026
#######################################################################

import utils.jsonUtils.pitpal_json_schema_utils as Jsu

class IllegalOperation(Exception):
    pass


class _pit:
    def __init__(self, index, seeds ,prev=None,back=None,active=True):
        self.active= active
        self.index = index
        self.value = seeds
        self.prev = prev
        self.link = back
        self.reset = seeds
        self.capture=False

    def __bool__(self):
        return self.active

    def __iter__(self):
        return self

    def __next__(self):
        if not self.active:
            return None
        else:
            link = self.link
            while not link.active:
                if link.link  is None:
                    return None
                elif link == self:
                    return self
                else:
                    link = link.link
            return link

    def __getitem__(self, index: int ):
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
            raise IllegalOperation("Copy failed: The object is empty.")
        a = type(self)( -1 , self.seeds, self.prev, self.link , self.active )
        self.value = 0
        return a


    def __add__(self, a: _pit):
        ret = True
        if a is not None and self.active:
            if a.value > 0:
                self.capture=False
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

    def __setitem__(self,index: int, value: int):
        link = self.__getitem( index)
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
        return self.capture:

class _kingzpit(_pit):
    def __init__(self, index ,prev=None,back=None,active=True):
        super().__init__(index,0,prev,back,active)

    def __copy__(self):
        raise IllegalOperation(f"KingzPit{self.index} selection not allowed")

    def __add__(self, a: _pit):
        ret = True
        if a is not None and self.active:
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

class _modpit(_pit):
    def __init__(self, index ,seeds, mod, notify,prev=None,back=None,active=True):
        super().__init__(index,seeds,prev,back,active)
        self.mod = mod
        self.notify=notify()
    
    def __add__(self, a: _pit):
        ret = True
        if a is not None and self.active:
            if a.value > 0:
                self.capture=False
                self.value += 1
                if(self.mod == self.value):
                    self.value = 0
                    self.notify(self.mod)
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

    
    
    


class _classic_board:
    def __init__(self, data):
        self.jsu=Jsu.JSU(schema_file="engine/rules/schema/board.schema.json", json_data=data)
        if not self.jsu.validate():
            raise 
        pits = int(data["pitsPerSide"]["Param"]["Value"])
        side = int(data["nSide"]["Param"]["Value"])
        seeds = int(data["nSeeds"]["Param"]["Value"])
        if "specialPits" in data:
            special = int(data["specialPits"]])
            self.create_pits(special)
        else:
            self.create_pits();

    def create_pits(self, special=[])
        self.total_seeds = pits * side * seeds
        self.side=[]
        first = None
        back = None
        for i in range(side-1, 0, -1):
            a=[]
            for j in range(pits -1 , 0 , -1):
                k = i*side + j
                now = None
                if k in special:
                    now = _kingzpit(k,prev.back)
                else:
                    now = _pit(k,seeds,prev, back)
                back = now
                a.append(now)
                if first == None:
                    first = now
            self.side.append(a)
        back.back = first
        self.pits = back




