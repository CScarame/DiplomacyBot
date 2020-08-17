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
    

class Hold(Order):
    def __init__(self, unit):
        super().__init__(unit)
        self.set_msg()
    def set_msg(self):
        self.msg = ""
        if self.unit.typ == UnitType.ARMY:
            self.msg = self.msg + "A "
        elif self.unit.typ == UnitType.FLEET:
            self.msg = self.msg + "F "
        self.msg = self.msg + self.unit.province.abr.capitalize()
        self.msg = self.msg + " holds"
        return

class Move(Order):
    province:ProvinceBase
    def __init__(self, unit:Unit, prov:ProvinceBase):
        if not self.unit.province.is_adjacent(prov,unit):
            raise DiplomacyError()
        else:
            self.unit = unit
            self.province = prov
    
class Support(Order):
    target:ProvinceBase
    supported:ProvinceBase
    def __init__(self, unit:Unit, target:ProvinceBase, supported:ProvinceBase):
        if not self.unit.province.is_adjacent(target,unit):
            raise DiplomacyError()