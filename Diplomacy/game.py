#############
# Diplomacy game.py
# Chris Scaramella
# 
#############

from typing import List, Dict

from Diplomacy.worldmap import WorldMap
from Diplomacy.types import Color, Coast, UnitType, ParseOrderError
from Diplomacy.province import ProvinceBase, LandProvince, WaterProvince, CoastProvince, TwoCoastProvince
from Diplomacy.country import Country
from Diplomacy.unit import Unit
from Diplomacy.turn import Turn

from Diplomacy.commands import Order, Hold, Move, Support, SupportHold, SupportMove, Convoy

import json

class Game:
    """A combination of the WorldMap and the commands that exist.

    Includes a WorldMap object that has all provinces, powers etc. and a list of Orders for each Country"""

    Orders:Dict[str,Order]
    World:WorldMap

    def __init__(self,ProvFile,CounFile):
        self.makeWorldMap(ProvFile,CounFile)
        self.initOrders()

    def makeWorldMap(self,ProvFile,CounFile):
        with open(ProvFile,'r') as prov_file:
            P = json.load(prov_file)
        with open(CounFile,'r') as coun_file:
            GS = json.load(coun_file)
        W = WorldMap()
        W.deserialize(P,GS)
        self.World = W

    def initOrders(self):
        orders = dict()
        for unit in self.World.Units:
            coun = unit.country.name
            if coun not in orders:
                orders[coun] = list()
            orders[coun].append(Hold(unit))
                
        self.Orders = orders
    def printOrders(self):
        for coun, order_list in self.Orders.items():
            print(coun)
            for order in order_list:
                print(order.msg)
    def readOrders(self,coun):
        output = ""
        if coun in self.Orders:
            orders = self.Orders[coun]
            for order in orders:
                output = output + order.msg + "\n"
        return output

    def readOrder(self,unit):
        for order in self.Orders:
            if order.unit == unit:
                return order.msg

    def matchUnit(self, coun:Country, typ:UnitType, prov:ProvinceBase):
        for i_unit in self.World.Units:
            if i_unit.match(coun, typ, prov):
                return i_unit
        return None

    def splitDashString(self, dash_str:str):
        parts = dash_str.split("-")
        first:ProvinceBase
        second:ProvinceBase
        if parts[0].lowercase() in self.World.Provinces.keys():
            first = self.World.Provinces[parts[0].lowercase()]
        else:
            return None
        if parts[1].lowercase() in self.World.Provinces.keys():
            second = self.World.Provinces[parts[1].lowercase()]
        else: return None
        return (first,second)

    #Examples:
        #Hold: A Lon Holds
        #Move: A Lon-Wal
        #SupportHold: A Lon S Wal
        #SupportMove: A Lon S Wal-Yor
        #Convoy: F Nth C A Lon-Hol
    def parseOrder(self,coun:Country, command_str:str):
        parts = command_str.split(None, 4)
        current_province:ProvinceBase
        unit:Unit
        typ:UnitType

        # Make sure there are enough words
        if len(parts) < 2:
            ParseOrderError()

        # Determine UnitType
        if parts[0].uppercase() == "A":
            typ = UnitType.ARMY
        elif parts[0].uppercase() == "F":
            typ = UnitType.FLEET
        else:
            ParseOrderError()
        
        # Check for Move Order
        if "-" in parts[1]:
            move_provs = self.splitDashString(parts[1])
            if move_provs == None:
                ParseOrderError()
            unit = self.matchUnit(coun, typ, move_provs[0])
            if unit == None:
                ParseOrderError()
            return Move(unit,move_provs[1])
        # Determine unit
        elif parts[1].lowercase() in self.World.Provinces.keys():
            current_province = self.World.Provinces[parts[1].lowercase()] # Pull current prov out
            unit = self.matchUnit(coun,typ,current_province)
            if unit == None:
                ParseOrderError()
        else:
            ParseOrderError()
        
        # Check for Hold Order
        if parts[2].lowercase() == "holds" or parts[2].lowercase() == "hold":
            return Hold(unit)
        elif parts[2].lowercase() == "s":
            ## SUPPORT COMMAND
            if "-" in parts[3]:
                move_provs = self.splitDashString(parts[3])
                if move_provs == None:
                    ParseOrderError()
                return SupportMove(unit,move_provs[0],move_provs[1])
            elif parts[3].lowercase() in self.World.Provinces.keys():
                return SupportHold(unit,self.World.Provinces[parts[3].lowercase()])
            else:
                ParseOrderError()
        elif parts[2].lowercase() == "c":
            ##CONVOY COMMAND
            if "-" in parts[3]:
                move_provs = self.splitDashString(parts[3])
                if move_provs == None:
                    ParseOrderError()
                return Convoy(unit,move_provs[0],move_provs[1])
            else:
                ParseOrderError()
        else:
            ParseOrderError()
        return

            
