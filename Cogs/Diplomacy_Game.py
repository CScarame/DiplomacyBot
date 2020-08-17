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
from Diplomacy.game import Game

import difflib, string

def setup(bot):
    bot.add_cog(Diplomacy_Game(bot))

class Diplomacy_Game(commands.Cog):
    def __init__(self,bot):
        G = Game("Saves/provinces.json","Saves/countries.json")
        self.Game = G
        self.bot = bot

    @commands.command(help="Get information about a province or country")
    async def info(self,ctx, *, info_name):
        Provinces = self.Game.World.Provinces
        Countries = self.Game.World.Countries
        if info_name.lower() in Provinces:
            msg = '`' + Provinces[info_name.lower()].info() + '`' + "\n"
        elif info_name in Countries:
            msg = '`' + Countries[info_name].info() + '`' + "\n"
        else:
            library = list(Provinces.keys()) + list(Countries.keys())
            possible_matches = difflib.get_close_matches(info_name,library)
            if not possible_matches:
                msg = ("Not sure what you're asking about.")
            else:
                msg = "Did you mean:\n"
                msg = msg + "\n".join(possible_matches)
        await ctx.send(msg)

    @commands.command(help="Generate a map of the current world")
    async def map(self, ctx):
        mapfile = discord.File(self.Game.World.saveImage())
        await ctx.send(file=mapfile)
    @commands.command(help="Show current orders")
    async def orders(self,ctx):
        msg = "`"
        Countries = self.Game.World.Countries
        for coun in Countries:
            msg = msg + Countries[coun].name + "\n"
            msg = msg + self.Game.readOrders(coun) + "\n"
        msg = msg + "`"
        await ctx.send(msg)
