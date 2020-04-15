#############
# Diplomacy country.py
# Chris Scaramella
# 
#############


from typing import List, Union, Optional, Tuple, Dict

from Diplomacy.province import ProvinceBase, LandProvince, WaterProvince, CoastProvince, TwoCoastProvince
from Diplomacy.types import Color, UnitType, Coast

class Country:
    """One of the 7 powers vying for control.

    Must have information over territories controlled, color used, list of units etc."""
    name:str
    color:Color
    home:List[ProvinceBase]
    provinces:List[ProvinceBase]
    powers:List[ProvinceBase]
    units:List['Unit']

    def __init__(self,name):
        self.name = name
        self.home = list()
        self.provinces = list()
        self.powers = list()
        self.units = list()
    # When this country loses a province
    def lose_province(self,prov):
        if prov in self.provinces:
            self.provinces.remove(prov)
            return True
        else:
            return False
    # When this country loses this power
    def lose_power(self,powe):
        if powe in self.powers:
            self.powers.remove(powe)
            return True
        else:
            return False
    # Used to check if the country controls any new provinces at end of turn
    def control_provinces(self):
        for unit in self.units:
            if unit.province not in self.provinces:
                if not isinstance(unit.province, WaterProvince):
                    # Remove province from old country list
                    unit.province.control.lose_poer(unit.province)
                    # Change province's country data
                    unit.province.power = self
                    # Add province to new country
                    self.powers.append(unit.province)
    # Used to check if the country controls any new powers at end of year
    def control_powers(self):
        for unit in self.units:
            if unit.province not in self.powers:
                if unit.province.is_power():
                    # Remove power from old country list
                    unit.province.control.lose_province(unit.province)
                    # Change province's country data
                    unit.province.control = self
                    # Add province to new country
                    self.provinces.append(unit.province)
 
    def read_state(self, Provinces, data):
        self.color = Color(data['color'])
        for prov in data['home']:
            self.home.append(Provinces[prov])
        for prov in data['power']:
            self.powers.append(Provinces[prov])
            Provinces[prov].power = self
        for prov in data['prov']:
            self.provinces.append(Provinces[prov])
            Provinces[prov].control = self
    def serialize(self):
        out_dict = dict()
        out_dict['color'] = self.color.print()
        out_dict['home'] = self.get_prov_list(self.home)
        out_dict['power'] = self.get_prov_list(self.powers)
        out_dict['prov'] = self.get_prov_list(self.provinces)
        army_list = list()
        fleet_list = list()
        coast_list = list()
        for unit in self.units:
            if unit.typ == UnitType.ARMY:
                army_list.append(unit.province.abr)
            if unit.typ == UnitType.FLEET:
                fleet_list.append(unit.province.abr)
                if unit.coast == None:
                    coast_list.append(0)
                elif unit.coast == Coast.NORTH:
                    coast_list.append(1)
                elif unit.coast == Coast.SOUTH:
                    coast_list.append(2)
        out_dict['army'] = army_list
        out_dict['fleet'] = fleet_list
        out_dict['coast'] = coast_list
        return out_dict
    def get_prov_list(self,data):
        out_list = list()
        for datum in data:
            out_list.append(datum.abr)
        return out_list
    def print(self):
        print("Country: {:>20}".format(self.name))
    def info(self):
        pow_str = str(len(self.powers))
        prov_str = str(len(self.provinces))
        msg = '{0} currently controls {1} provinces and {2} powers as follows:\n'.format(self.name, prov_str, pow_str)
        msg += 'Provinces:\t'
        for prov in self.provinces:
            msg += '{} ({})\t'.format(prov.name, prov.abr)
        msg += '\nPowers:\t'
        for powe in self.powers:
            msg += '{} ({})\t'.format(powe.name, powe.abr)
        return msg