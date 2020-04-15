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
    async def info(self,ctx, *args):
        if not args:
            msg = "Use this command for more information about a certain province or country.  For a list of provinces and countries, use **!all**"
            await ctx.send(msg)
        msg = ""
        for arg in args:
            if arg.lower() in self.Game.Provinces:
                msg = msg + '`' + self.Game.Provinces[arg.lower()].info() + '`' + "\n"
            elif arg in self.Game.Countries:
                msg = msg + '`' + self.Game.Countries[arg].info() + '`' + "\n" 
        await ctx.send(msg)