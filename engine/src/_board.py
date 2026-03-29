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
    def __init__(self, data: dict, event):
        self.jsu=Jsu.JSU(schema_file="engine/rules/schema/board.schema.json", json_data=data)
        if not self.jsu.validate():
            raise
        self.pits = int(data["pitsPerSide"]["Param"]["Value"])
        self.side = int(data["nSide"]["Param"]["Value"])
        self.seeds = int(data["nSeeds"]["Param"]["Value"])
        self.event = event
        typee = data["pitType"]
        self.total_seeds = self.pits * self.side * self.seeds
        if "specialPits" in data:
            special = int(data["specialPits"]])
            self.create_pits(typee , special)
        else:
            self.create_pits( typee)

    def mod_notify(self, index):
        self.event.set("mod", index)

    def create_pits(self, typee, special=[]):
        self.sidee=[]
        lastt = None
        prev = None
        back = None
        for i in range(self.side - 1, 0, -1):
            a=[]
            for j in range(self.pits -1 , 0 , -1):
                k = i * self.side + j
                now = None
                if k in special:
                    now = _kingzpit(k,prev, back)
                    self.total_seeds -= self.seeds
                elif "normalplus" in typee["Type"]:
                    mod=int(typee["Value"])
                    now = _modpit(k,self.seeds,mod , self.mod_notify,prev,back )
                else:
                    now = _pit(k,self.seeds,prev, back)
                back = now
                a.append(now)
                if lastt == None:
                    lastt = now
            self.sidee.append(a)
        if back != None:
            back.back = lastt
        self.board = back
        self.event.set("newboard",typee["Type"] , self.pits, self.side , self.seeds )
