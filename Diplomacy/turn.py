#############
# Diplomacy turn.py
# Chris Scaramella
# 
#############

from Diplomacy.types import DiplomacyError

class Turn:
    year:int
    season:str

    def __init__(self, year:int, season:str):
        if year < 1900:
            raise DiplomacyError('Tried to initiate an invalid turn (year)')
        elif season is not ('Spring' or 'Fall'):
            raise DiplomacyError('Tried to initialize an invalid turn (season)')
        self.year = year
        self.season = season

    def next(self):
        if self.season == 'Spring':
            self.season = 'Fall'
        if self.season == 'Fall':
            self.year += 1
            self.season = 'Spring'
        return
    
    def serialize(self):
        returnDict = dict()
        returnDict['year'] = self.year
        returnDict['season'] = self.season
        return returnDict
    def deserialize(self,data):
        self.year = data['year']
        self.season = data['season']
