#############
# Diplomacy turn.py
# Chris Scaramella
# Set of possible commands that can be sent.
#############

from Diplomacy.types import UnitType, DiplomacyError
from Diplomacy.province import ProvinceBase, LandProvince, WaterProvince, CoastProvince, TwoCoastProvince
from Diplomacy.unit import Unit


class Order():
    unit:Unit
    msg:str
    def __init__(self, unit):
        self.unit = unit
    def msgBase(self):
        if self.unit.typ == UnitType.ARMY:
            return "A " + self.unit.province.abr.capitalize()
        elif self.unit.typ == UnitType.FLEET:
            return "F " + self.unit.province.abr.capitalize()
        else:
            return " "
    

class Hold(Order):
    def __init__(self, unit):
        super().__init__(unit)
        self.set_msg()
    def set_msg(self):
        self.msg = self.msgBase()+ " holds"
        return

class Move(Order):
    province:ProvinceBase
    def __init__(self, unit:Unit, prov:ProvinceBase):
        super().__init__(unit)
        self.province = prov
        self.set_msg()

    def set_msg(self):
        self.msg = self.msgBase() + "-" + self.province.abr.capitalize()
        return

    
class Support(Order):
    target:ProvinceBase
    supported:ProvinceBase
    def __init__(self, unit:Unit, target:ProvinceBase, supported:ProvinceBase):
        super().__init__(unit)
        self.target = target
        self.supported = supported
        self.set_msg()
    def set_msg(self):
        self.msg = self.msgBase() + " S " + self.supported.abr.capitalize() + self.target.abr.capitalize()
        return
