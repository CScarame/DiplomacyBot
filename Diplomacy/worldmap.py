#############
# Diplomacy worldmap.py
# Chris Scaramella
# 
#############

import json, time
from typing import List, Dict
from PIL import Image

from Diplomacy.types import Color, Coast, UnitType
from Diplomacy.province import ProvinceBase, LandProvince, WaterProvince, CoastProvince, TwoCoastProvince
from Diplomacy.country import Country
from Diplomacy.unit import Unit
from Diplomacy.turn import Turn

BACKGROUND_IMAGE = "Images/Main.png"

class WorldMap:
    """The Diplomacy map, sufficiently detailed.

    Includes a List of Provinces that exist.  Useful for functions that affect all 
    provinces in the map, such as save functions or sweeping through all of them."""
    Provinces:Dict[str, ProvinceBase]
    Countries:Dict[str, Country]
    Units:List[Unit]

    turn:Turn

    #background
    noneColor:Color


    def __init__(self):
        self.Provinces = dict()
        self.Countries = dict()
        self.Units = list()
        self.turn = Turn(1900, 'Spring')
        self.setBackground(BACKGROUND_IMAGE,"eeeeee")

    def makeProvinces(self, P):
        for abr in P:
            if P[abr]['form'] == 'LAND':
                self.Provinces[abr] = LandProvince(abr)
            elif P[abr]['form'] == 'WATER':
                self.Provinces[abr] = WaterProvince(abr)
            elif P[abr]['form'] == 'COAST':
                self.Provinces[abr] = CoastProvince(abr)
            elif P[abr]['form'] == 'TWO_COAST':
                self.Provinces[abr] = TwoCoastProvince(abr)
        for abr, prov in zip(P,self.Provinces):
            self.Provinces[prov].set_data(P[abr],self.Provinces)
        return
    def saveProvinces(self):
        out_dict = dict()
        for abr, prov in self.Provinces.items():
            out_dict[abr] = prov.serialize()
        return out_dict
    def makeCountries(self, C):
        for coun in C:
            coun_temp = Country(coun)
            coun_temp.read_state(self.Provinces,C[coun])
            # Units
            for army in C[coun]['army']:
                temp_army = Unit(self.Provinces[army], coun_temp, UnitType.ARMY)
                self.Units.append(temp_army)
            for fleet, coast in zip(C[coun]['fleet'],C[coun]['coast']):
                temp_fleet = Unit(self.Provinces[fleet], coun_temp, UnitType.FLEET)
                if isinstance(temp_fleet.province, TwoCoastProvince):
                    if coast == 1:
                        temp_fleet.coast = Coast.NORTH
                    elif coast == 2:
                        temp_fleet.coast = Coast.SOUTH
                    temp_fleet.coast = Coast.SOUTH
                self.Units.append(temp_fleet)
            self.Countries[coun_temp.name] = coun_temp
    def saveCountries(self):
        out_dict = dict()
        for name, coun in self.Countries.items():
            out_dict[name] = coun.serialize()
        return out_dict
    def deserialize(self, P, GS):
        """Read in JSON file of provinces and countries."""
        # Make provinces
        self.makeProvinces(P)
        self.makeCountries(GS['Countries'])
        self.turn.deserialize(GS['Turn'])
    def serialize(self,out_name):
        SerialDict = dict()
        SerialDict['Countries'] = self.saveCountries()
        SerialDict['Turn'] = self.turn.serialize()
        with open(out_name,'w') as outfile:
            json.dump(SerialDict,outfile,sort_keys=True)
        return

    def setBackground(self,imagestr,colorstr):
        self.noneColor = Color(colorstr)
        self.background = Image.open(imagestr)
       
    def makeImage(self):
        bg = self.background
        for abr, prov in self.Provinces.items():
            if prov.image == None:
                continue
            if prov.control == None:
                prov.color_image(self.noneColor)
            else:
                prov.color_image(prov.control.color)
            bg.paste(prov.image,(0,0),prov.image)
            if prov.is_power():
                if prov.power == None:
                    prov.color_power(Color("ffffff"))
                else:
                    prov.color_power(prov.power.color)
                bg.paste(prov.power_image,(0,0),prov.power_image)
        for unit in self.Units:
            if unit.typ == UnitType.ARMY:
                bg.paste(unit.image,unit.province.land_location.data(),unit.image)
            elif unit.typ == UnitType.FLEET:
                if unit.coast == None:
                    bg.paste(unit.image,unit.province.water_location.data(),unit.image)
                elif unit.coast == Coast.NORTH:
                    bg.paste(unit.image,unit.province.north_location.data(),unit.image)
                elif unit.coast == Coast.SOUTH:
                    bg.paste(unit.image, unit.province.south_location.data(),unit.image)
        return bg

    def saveImage(self):
        filename = "Images/Temp/" + time.strftime("%Y%m%d-%H%M%S") + ".png"
        self.makeImage().save(filename, "PNG")
        return filename

    def print_names(self):
        for prov in self.Provinces:
            print("{p.abr:3}{p.name:>25}".format(p=self.Provinces[prov]))
    def print_adj(self):
        for prov in self.Provinces:
            adj_str = ""
            for adj in self.Provinces[prov].adjacent:
                adj_str += adj.abr
                adj_str += ' '
            adj_str = adj_str[0:-1]
            print('{}: {}'.format(self.Provinces[prov].abr,adj_str))
    def print(self):
        for prov in self.Provinces:
            self.Provinces[prov].print()
        for coun in self.Countries:
            coun.print()
