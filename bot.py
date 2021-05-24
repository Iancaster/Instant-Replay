
##Import-ant Libraries
import discord
from discord.ext import commands
import datetime
import asyncio


##Variables
client = commands.Bot(command_prefix='Ir.', case_insensitive=True)

##Setup
print ("Allow me a moment to wake up...")
client.remove_command("help")

##Events
@client.event
async def on_ready():
    print(f'{client.user} is alive!')
    await client.change_presence(activity=discord.Game(name='Lss!help for help.'))

##Commands
@client.command(aliases=['h'])
async def help(ctx):
    await ctx.message.delete()
    words = ctx.message.content.split()


#Execute
#client.run(environ['discordToken'])
client.run('ODQ2NTIzMTg4MjYyNDY5Njcy.YKwwJw.W5uKvVX6fma3eKDiq1f_MjwsW1Q')