#############
# Diplomacy types.py
# Chris Scaramella
# Basic Data types that are used in other parts of the package
#############

from enum import Enum, auto
from typing import NewType

class DiplomacyError(Exception):
    pass
class UnitType(Enum):
    """Each unit is an ARMY or a FLEET"""
    ARMY = auto()
    FLEET = auto()
class Coast(Enum):
    """For FLEETS that are in a two coast province, define which coast that unit is on."""
    NORTH = auto()
    SOUTH = auto()

class Location():
    x:int
    y:int
    def __init__(self,*args):
        if len(args) == 1:
            if type(args[0]) == str:
                self.parse(args[0])
                return
        elif len(args) == 2:
            if type(args[0]) == int and type(args[1]) == int:
                self.x = args[0]
                self.y = args[1]
                return
        self.x = 0
        self.y = 0
    def parse(self, str_in):
        loc = str_in.split('x')
        self.x = int(loc[0])
        self.y = int(loc[1])
    
    def print(self):
        loc_string = '{p.x}x{p.y}'.format(p=self)
        return loc_string
    
class Color():
    def __init__(self, *args):
        if len(args) == 1:
            if type(args[0]) == str and len(args[0]) == 6:
                self.parse(args[0])
                return
        elif len(args) == 3:
            if all(type(args) == int):
                self.r = args[0]
                self.g = args[1]
                self.b = args[2]
                return
        self.r = 0
        self.g = 0
        self.b = 0
    def parse(self, str_in):
        self.r = int(str_in[0:2],16)
        self.g = int(str_in[2:4],16)
        self.b = int(str_in[4:6],16)
        return
    def data(self):
        return (self.r,self.g,self.b)
    def print(self):
        r = hex(self.r[2:])
        g = hex(self.g[2:])
        b = hex(self.b[2:])
        return r+g+b


#Location = NewType('Location', (int,int)) #x,y coordinate location on map
#Color    = NewType('Color', (int, int, int)) # r,g,b color info

