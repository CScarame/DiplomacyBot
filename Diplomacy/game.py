#############
# Diplomacy game.py
# Chris Scaramella
# 
#############

from typing import List, Dict

from Diplomacy.worldmap import WorldMap
from Diplomacy.types import Color, Coast, UnitType
from Diplomacy.province import ProvinceBase, LandProvince, WaterProvince, CoastProvince, TwoCoastProvince
from Diplomacy.country import Country
from Diplomacy.unit import Unit
from Diplomacy.turn import Turn

from Diplomacy.commands import Order, Hold, Move, Support

import json

class Game:
    """A combination of the WorldMap and the commands that exist.

    Includes a WorldMap object that has all provinces, powers etc. and a list of Orders for each Country"""

    orders:Dict[str,Order]

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
                
        self.orders = orders
    def printOrders(self):
        for coun, order_list in self.orders.items():
            print(coun)
            for order in order_list:
                print(order.msg)
    def readOrders(self,coun):
        output = ""
        if coun in self.orders:
            orders = self.orders[coun]
            for order in orders:
                output = output + order.msg + "\n"
        return output

