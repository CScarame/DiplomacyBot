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

    @commands.command()
    async def timer(self, ctx, timeInput):
        try:
            try:
                time = int(timeInput)
            except:
                convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
                time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
            if time > 86400:
                await ctx.send("I can\'t do timers over a day long")
                return
            if time <= 0:
                await ctx.send("Timers don\'t go into negatives :/")
                return
            if time >= 3600:
                message = await ctx.send(f"Timer: {time//3600} hours {time%3600//60} minutes {time%60} seconds")
            elif time >= 60:
                message = await ctx.send(f"Timer: {time//60} minutes {time%60} seconds")
            elif time < 60:
                message = await ctx.send(f"Timer: {time} seconds")
            while True:
                try:
                    currentTime = datetime.datetime.now()
                    time -= 1
                    if time >= 3600:
                        await message.edit(content=f"Timer: {time//3600} hours {time %3600//60} minutes {time%60} seconds")
                    elif time >= 60:
                        await message.edit(content=f"Timer: {time//60} minutes {time%60} seconds")
                    elif time < 60:
                        await message.edit(content=f"Timer: {time} seconds")
                    if time <= 0:
                        await message.edit(content="Ended!")
                        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
                        break
                    timeDiff = datetime.datetime.now() - currentTime
                    print(timeDiff)
                    await asyncio.sleep((1000.0-timeDiff)/1000)
                except:
                    break
        except:
            await ctx.send(f"Alright, first you gotta let me know how I\'m gonna time **{timeInput}**....")