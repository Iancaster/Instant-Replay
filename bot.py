
##Import-ant Libraries
import os
from os import path, environ
import discord
from discord import message
from discord.ext import commands
from datetime import datetime
import asyncio
import json
import math
import random
import string


##Variables
client = commands.Bot(command_prefix='Lss!', case_insensitive=True)

##Setup
print ("Allow me a moment to wake up...")


##Events
@client.event
async def on_ready():
    print(f'{client.user} is alive!')
    await client.change_presence(activity=discord.Game(name='Lss!help for help.'))
    for i in client.guilds:
        await addServerVars(i)

##Commands
@client.command(aliases=['h'])
async def help(ctx):
    await ctx.message.delete()
    words = ctx.message.content.split()

    if len(words) == 1:       
        await helpFunc(ctx.channel,ctx.author)
        return
    else:
        await promptFunc(ctx.channel,ctx.author,('Documentation for the ' + words[1] + ' command:'),helpMessages[words[1].upper()],'This message will delete itself in 30 seconds.','❌')
        return

## Functions

#Used Internally

#Execute
#client.run(environ['discordToken'])