#############
## Basic.py
## Author: Chris Scaramella
## Date: 1/15/2020
#############

import discord
from discord.ext import commands

import Diplomacy

import json
import datetime
import asyncio
import subprocess

def setup(bot):
    bot.add_cog(Basic(bot))

class Basic(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(help="Say hello to the bot.")
    async def hi(self,ctx):
        await ctx.send("Hi!")

    @commands.command(help="The bot will wait for a new minute before answering")
    async def minute(self, ctx):
        currentTime = datetime.datetime.today()
        futureTime = currentTime.replace(second=0,microsecond=0) + datetime.timedelta(minutes=1)
        while futureTime > currentTime:
            currentTime = datetime.datetime.today()
            await asyncio.sleep(1)
        await ctx.send("A new minute!")