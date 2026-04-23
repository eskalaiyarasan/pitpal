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
