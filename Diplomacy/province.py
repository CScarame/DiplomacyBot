#############
# Diplomacy province.py
# Chris Scaramella
# Province Base and subclasses
#############


import os, numpy
from PIL import Image
from typing import List, Union, Optional, Tuple, Dict

from Diplomacy.types import Location, Color, UnitType

class ProvinceBase:
    """Base class for a piece of land or water that can be controlled.

    Includes name, abbreviation, power status"""
    # Identifying Information and Links
    name:str
    abr:str
    power:Optional['Country']
    control:Optional['Country']

    def __init__(self,abr):
        self.abr = abr

        # Set initial values
        self.name = ''
        self.power = None
        self.control = None
        # Read in the province's image data.
        if abr == 'con':
            abr = 'con_'
        if "{}.png".format(abr) in os.listdir("Images/Provinces"):
            self.image = Image.open("Images/Provinces/{}.png".format(abr))
        else:
            self.image = None
        if "{}_p.png".format(abr) in os.listdir("Images/Powers"):
            self.power_image = Image.open("Images/Powers/{}_p.png".format(abr))
        else:
            self.power_image = None
    def set_data(self,data):
        self.name = data['name']
    def adj_serialize(self,adj):
        out_list = list()
        for prov in adj:
            out_list.append(prov.abr)
        return out_list
    def color_image(self,noneColor:Color):
        """Color the image"""
        if self.image == None:
            return
        data = numpy.array(self.image)
        if self.control == None:
            data[..., :-1] = noneColor
        else:
            data[..., :-1] = self.control.color.data()
        self.image = Image.fromarray(data)
        return
    def color_power(self,noneColor:Color):
        """Color the power, but only if the province is a power"""
        if not self.is_power():
            return
        data = numpy.array(self.power_image)
        if self.power == None:
            data[..., :-1] = noneColor
        else:
            data[..., :-1] = self.power.color.data()
        self.power_image = Image.fromarray(data)
        return
    
    # Helper Functions
    def is_power(self):
        if self.power_image is None:
            return False
        else:
            return True
    def set_power(self):
        if self.control == self.power:
            return
        self.power = self.control
    def produce(self):
        if self.is_power():
            output = list()
            if isinstance(self, LandProvince) or isinstance(self, CoastProvince) or isinstance(self,TwoCoastProvince):
                output.append(UnitType.ARMY)
            if isinstance(self, WaterProvince) or isinstance(self, CoastProvince) or isinstance(self,TwoCoastProvince):
                output.append(UnitType.FLEET)
            return output
        else:
            return None
    def print(self):
        print("Province: {p.name}".format(p=self))
    # {name}({abr}) is a {type of province} {if not water, who controls it}
    # {If power center, who controls that power center?}
    def info(self):
        msg = '{0.name} ({0.abr}) is a '.format(self)
        if isinstance(self, LandProvince):
            msg += 'a land-locked province'
        elif isinstance(self, WaterProvince):
            msg += 'a water province'
        elif isinstance(self, CoastProvince):
            msg += 'a costal proivnce'
        elif isinstance(self, TwoCoastProvince):
            msg += 'a province with two coasts'
        if self.control == None:
            msg += ' that is currently not controlled by any world power.'
        else:
            msg += ' that is currently controlled by {}.'.format(self.control.name)
        if self.is_power():
            if self.power == None:
                msg += '  It contains a power center that is currently unoccupied.'
            else:
                msg += ' It contains a power center that is currently controlled by {}.'.format(self.power.name)
        return msg

class LandProvince(ProvinceBase):
    """Class used for a province that is land locked.
    
    Includes land adjacencies and position where armies appear."""
    land_adjacent:List['Province']
    land_location:Location

    def __init__(self,abr):
        super(LandProvince,self).__init__(abr)
        self.land_location = Location((0,0))
        self.land_adjacent = list()
        if(self.is_power()):
            self.produce = [UnitType.ARMY]
    def set_data(self,data, P):
        super(LandProvince,self).set_data(data)
        self.land_location = Location(data['land_location'])
        for abr in data['land_adjacent']:
            self.land_adjacent.append(P[abr])
        return
    def is_adjacent(self,prov:ProvinceBase,unit:'Unit'):
        if unit.typ == UnitType.ARMY:
            if prov in self.land_adjacent:
                return True
        elif unit.typ == UnitType.FLEET:
            return False
        return False
    def serialize(self):
        out_dict = dict()
        out_dict['name'] = self.name
        out_dict['form'] = self.form()
        out_dict['land_location'] = self.land_location.print()
        out_dict['land_adjacent'] = self.adj_serialize(self.land_adjacent)
        return out_dict
    def form(self):
        return 'LAND'
class WaterProvince(ProvinceBase):
    """Class used for a province that is water.

    Includes water adjacencies and positions where fleets appear."""
    water_adjacent:List['Province']
    water_location:Location

    def __init__(self, abr):
        super(WaterProvince,self).__init__(abr)
        self.water_location = Location((0,0))
        self.water_adjacent = list()
        if(self.is_power()):
            self.produce = [UnitType.FLEET]
    def set_data(self,data, P):
        super(WaterProvince,self).set_data(data)
        self.water_location = Location(data['water_location'])
        for abr in data['water_adjacent']:
            self.water_adjacent.append(P[abr])
        return
    def is_adjacent(self,prov:ProvinceBase,unit:'Unit'):
        if unit.typ == UnitType.ARMY:
            return False
        elif unit.typ == UnitType.FLEET:
            if prov in self.water_adjacent:
                return True
        return False
    def serialize(self):
        out_dict = dict()
        out_dict['name'] = self.name
        out_dict['form'] = self.form()
        out_dict['water_location'] = self.water_location.print()
        out_dict['water_adjacent'] = self.adj_serialize(self.water_adjacent)
        return out_dict
    def form(self):
        return 'WATER'
class CoastProvince(ProvinceBase):
    """Used for a costal province with only one coast.

    Includes land AND water adjacencies, and land and water locations"""
    land_adjacent:List['Province']
    land_location:Location
    water_adjacent:List['Province']
    water_location:Location

    def __init__(self,abr):
        super(CoastProvince,self).__init__(abr)
        self.land_location = Location((0,0))
        self.land_adjacent = list()
        self.water_location = Location((0,0))
        self.water_adjacent = list()
        if(self.is_power()):
            self.produce = [UnitType.ARMY, UnitType.FLEET]
    def set_data(self,data, P):
        super(CoastProvince,self).set_data(data)
        self.land_location = Location(data['land_location'])
        for abr in data['land_adjacent']:
            self.land_adjacent.append(P[abr])
        self.water_location = Location(data['water_location'])
        for abr in data['water_adjacent']:
            self.water_adjacent.append(P[abr])
        return
    def is_adjacent(self,prov:ProvinceBase,unit:'Unit'):
        if unit.typ == UnitType.ARMY:
            if prov in self.land_adjacent:
                return True
        if unit.typ == UnitType.FLEET:
            if prov in self.water_adjacent:
                return True
        return False
    def serialize(self):
        out_dict = dict()
        out_dict['name'] = self.name
        out_dict['form'] = self.form()
        out_dict['land_location'] = self.land_location.print()
        out_dict['land_adjacent'] = self.adj_serialize(self.land_adjacent)
        out_dict['water_location'] = self.water_location.print()
        out_dict['water_adjacent'] = self.adj_serialize(self.water_adjacent)
        return out_dict
    def form(self):
        return "COAST"
class TwoCoastProvince(ProvinceBase):
    """Used for a coastal province with two coasts.

    Includes land AND north AND south adjacencies, and locations for each"""
    land_adjacent:List['Province']
    land_location:Location
    north_adjacent:List['Province']
    north_location:Location
    south_adjacent:List['Province']
    south_location:Location

    def __init__(self,abr):
        super(TwoCoastProvince,self).__init__(abr)
        self.land_location = Location((0,0))
        self.land_adjacent = list()
        self.north_location = Location((0,0))
        self.north_adjacent = list()
        self.south_location = Location((0,0))
        self.south_adjacent = list()
        if(self.is_power()):
            self.produce = [UnitType.ARMY, UnitType.FLEET]
    def set_data(self,data, P):
        super(TwoCoastProvince,self).set_data(data)
        self.land_location = Location(data['land_location'])
        for abr in data['land_adjacent']:
            self.land_adjacent.append(P[abr])
        self.north_location = Location(data['north_location'])
        for abr in data['north_adjacent']:
            self.north_adjacent.append(P[abr])
        self.south_location = Location(data['south_location'])
        for abr in data['south_adjacent']:
            self.south_adjacent.append(P[abr])
        return
    def is_adjacent(self,prov:ProvinceBase,unit:'Unit'):
        if unit.typ == UnitType.ARMY:
            if prov in self.land_adjacent:
                return True
        if unit.typ == UnitType.FLEET:
            if prov in self.north_adjacent or prov in self.south_adjacent:
                return True
        return False
    def serialize(self):
        out_dict = dict()
        out_dict['name'] = self.name
        out_dict['form'] = self.form()
        out_dict['land_location'] = self.land_location.print()
        out_dict['land_adjacent'] = self.adj_serialize(self.land_adjacent)
        out_dict['north_location'] = self.north_location.print()
        out_dict['north_adjacent'] = self.adj_serialize(self.north_adjacent)
        out_dict['south_location'] = self.south_location.print()
        out_dict['south_adjacent'] = self.adj_serialize(self.south_adjacent)
        return out_dict
    def form(self):
        return "TWO_COAST"
