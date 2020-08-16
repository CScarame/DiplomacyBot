#############
## Diplomacy.py
## Author: Chris Scaramella
## Date: 1/15/2020
#############
## This cog is designed to include all of the information necessary to 
## run a Diplomacy game.
#############

import discord
from discord.ext import commands

import json
from Diplomacy.worldmap import WorldMap

import difflib, string

def setup(bot):
    bot.add_cog(Diplomacy_Game(bot))

class Diplomacy_Game(commands.Cog):
    def __init__(self,bot):
        with open("Saves/provinces.json",'r') as prov_file:
            P = json.load(prov_file)
        with open("Saves/countries.json",'r') as coun_file:
            GS = json.load(coun_file)
        W = WorldMap()
        W.deserialize(P,GS)

        self.Game = W
        self.bot = bot

    @commands.command(help="Get information about a province or country")
    async def info(self,ctx, *, info_name):
        if info_name.lower() in self.Game.Provinces:
            msg = '`' + self.Game.Provinces[info_name.lower()].info() + '`' + "\n"
        elif info_name in self.Game.Countries:
            msg = '`' + self.Game.Countries[info_name].info() + '`' + "\n"
        else:
            library = list(self.Game.Provinces.keys()) + list(self.Game.Countries.keys())
            possible_matches = difflib.get_close_matches(info_name,library)
            if not possible_matches:
                msg = ("Not sure what you're asking about.")
            else:
                msg = "Did you mean:\n"
                msg = msg + "\n".join(possible_matches)
        await ctx.send(msg)

    @commands.command(help="Generate a map of the current world")
    async def map(self, ctx):
        mapfile = discord.File(self.Game.saveImage())
        await ctx.send(file=mapfile)