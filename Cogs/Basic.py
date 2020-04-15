#############
## Basic.py
## Author: Chris Scaramella
## Date: 1/15/2020
#############

import discord
from discord.ext import commands

import Diplomacy

import json

def setup(bot):
    bot.add_cog(Basic(bot))

class Basic(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(help="Say hello to the bot.")
    async def hi(self,ctx):
        await ctx.send("Hi!")