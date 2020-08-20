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

    def validate(self):
        NotImplementedError()
    

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
        self.validate()
        self.set_msg()

    def validate(self):
    # Move Order requirements:
        #   -provinces are adjacent OR
        #   -both provinces are Coastal and can be connected by water
        #   -unit type must correspond with the destination(armies can't move to water, fleets can't move to land)
        #    note line above is already checked by is_adjacent I think
        # note: black sea is only water province that is not connected to all other water provinces
        typ = self.unit.typ
        unit = self.unit
        prov = self.province
        if not unit.province.is_adjacent(prov,unit):
            if typ == UnitType.FLEET:
                raise DiplomacyError()
            if not (isinstance(unit.province, CoastProvince) or isinstance(unit.province, TwoCoastProvince)): 
                raise DiplomacyError()
            if not (isinstance(prov, CoastProvince) or isinstance(prov, TwoCoastProvince)): # Can be convoyed
                raise DiplomacyError()
        return

    def set_msg(self):
        self.msg = self.msgBase() + "-" + self.province.abr.capitalize()
        return

class Support(Order):
    supported:ProvinceBase
    
    def __init__(self, unit:Unit, supported:ProvinceBase):
        super().__init__(unit)
        self.supported = supported

    def validate(self):
        NotImplementedError()
    
    def set_msg(self):
        NotImplementedError()

    def support_msg(self):
        self.msg = self.msgBase() + " S " + self.supported.abr.capitalize()
        return

class SupportHold(Support):
    def __init__(self, unit:Unit, supported:ProvinceBase):
        super().__init__(unit, supported)
        self.validate()
        self.set_msg()

    def validate(self):
        # Support Hold must be adjacent to supported unit
        if not self.unit.province.is_adjacent(self.supported,self.unit):
            raise DiplomacyError()

    def set_msg(self):
        self.msg = self.support_msg()
        return
    
class SupportMove(Support):
    target:ProvinceBase
    def __init__(self, unit:Unit,supported:ProvinceBase, target:ProvinceBase):
        super().__init__(unit, supported)
        self.target = target
    def validate(self):
        #Support Move must be adjacent to target province
        if not self.unit.province.is_adjacent(self.target, self.unit):
            raise DiplomacyError()
    def set_msg(self):
        self.msg = self.support_msg() + "-" _ self.target.abr.capitalize()

class Convoy(Order):
    start:ProvinceBase
    end:ProvinceBase
    def __init__(self, unit:Unit, c_start:ProvinceBase, c_end:ProvinceBase):
        super().__init__(unit)
        self.start = c_start
        self.end = c_end
        self.validate()
        self.set_msg()

    def validate(self):
        # Convoy Order Requirements:
            # Only fleets can convoy
            # Start and end must be coastal
            # TODO: Black sea separated from others
        if not self.unit.typ == UnitType.FLEET:
            raise DiplomacyError()
        if not (isinstance(self.start, CoastProvince) or isinstance(self.start, TwoCoastProvince)):
            raise DiplomacyError()
        if not (isinstance(self.end, CoastProvince) or isinstance(self.end, TwoCoastProvince)):
            raise DiplomacyError()

    def set_msg(self):
        self.msg = self.msgBase() + " C " + self.start.abr.capitalize() + "-" + self.end.abr.capitalize()