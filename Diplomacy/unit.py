#############
# Diplomacy unit.py
# Chris Scaramella
# 
#############


import numpy
from PIL import Image
from typing import Optional

from Diplomacy.types import UnitType, Coast, Location, Color
from Diplomacy.province import ProvinceBase, LandProvince, WaterProvince, CoastProvince, TwoCoastProvince
from Diplomacy.country import Country




class Unit:
    """An Army or Fleet that is owned by a country

    Has a position on the map."""
    province:ProvinceBase # Where the unit is
    coast:Optional[Coast] # #If unit is on a twocoastprovince, which coast are they on?
    country:Country # Which country the unit is owned by.
    typ:UnitType

    #image

    def __init__(self,province, country, typ):
        self.province = province
        self.coast = None
        self.typ = typ
        self.country = country
        country.units.append(self)
        if typ == UnitType.ARMY:
            self.image = Image.open("Images/Units/Army.png")
        else:
            self.image = Image.open("Images/Units/Fleet.png")
        self.color_image()

    def color_image(self):
        data = numpy.array(self.image)
        data[numpy.all(data == 255,2)] = self.country.color.data() + (255,)
        self.image = Image.fromarray(data)
        return
    # Returns location information for this unit
    def location(self):
        if self.typ == UnitType.ARMY:
            if isinstance(self.province, LandProvince) or isinstance(self.province, CoastProvince):
                return self.province.land_location
        elif self.typ == UnitType.FLEET:
            if isinstance(self.province, WaterProvince) or isinstance(self.province, CoastProvince):
                return self.province.water_location
            elif isinstance(self.province, TwoCoastProvince):
                if self.coast == Coast.NORTH:
                    return self.province.north_location
                elif self.coast == Coast.SOUTH:
                    return self.province.south_location
        return Location(0,0)
    # Returns all adjacent provinces to this unit
    def adjacent(self):
        if self.typ == UnitType.ARMY:
            return self.province.land_adjacent
        elif self.typ == UnitType.FLEET:
            if isinstance(self.province, WaterProvince) or isinstance(self.province, CoastProvince):
                return self.province.water_adjacent
            elif isinstance(self.province, TwoCoastProvince):
                if self.coast == Coast.NORTH:
                    return self.province.north_adjacent
                elif self.coast == Coast.SOUTH:
                    return self.province.south_adjacent
        return list()
    def print(self):
        if self.typ == UnitType.ARMY:
            typ_str = "Army"
        elif self.typ == UnitType.FLEET:
            typ_str = "Fleet"
        print("{:>20} {:>5}: {:>3}".format(self.country.name,typ_str,self.province.abr))
