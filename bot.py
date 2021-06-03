
##Import-ant Libraries
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
import os
from os import path, environ
import json
import dateparser

##Variables
client = commands.Bot(command_prefix='Ir.', case_insensitive=True)
helpMessages = {
    'help' : "Aliases: `H`.\nA dual-purpose command. Can be used on its own to bring up \
        the main menu, or if you write a command after it, like you did here, it will display documentation.",
    'tutorial' : "Aliases: `Guide`.\nShows you some resources for learning the commands, including how \
        to access the additional documentation you're reading right now.",
    'commandslist' : "Aliases: `Commands`.\nLists out every command the bot has access to, and \
        provides a brief description of what each one does. Neatly categorized, too.",
    'support' : "Aliases: None\nGives you my contact in case you want to say a word or report a bug.",
    'options' : "Aliases: `Settings`.\nAllows anyone in the server to view some surface-level \
        information about the server's current settings.",
    'pauseMenu' : "Aliases: `PauseState`.\nViews the server's current pause state. This means \
        it'll allow people to replay fom it if it's unpaused (or vice versa if it *is* paused.",
    'pause' : "Aliases: `P`.\nPauses the server from being replayed.",
    'unpause' : "Aliases: `UP`.\nUnpauses the server, allowing replays.",
    'whitelist' : "Aliases: `WL`.\nView the whitelist, or 'what channels are allowed to be played \
        while every other channel is not'.",
    'blacklist' : "Aliases: `BL`.\nViews the blacklist. Channels here are blocked from being replayed, \
        but if there's a whitelist, channels on that list will override whatever is written on this one.",
    'whitelistadd' : "Aliases: `WLAdd`, `WL+`, `Whitelist+`.\nAdds a channel to the whitelist based on \
        the mention an admin provides. Using `whitelistadd #mention` allows you to skip the prompt \
        and cut straight to adding a channel.",
    'blacklistadd' : "Aliases: `BLAdd`, `BL+`, `Blacklist+`.\nAdds a channel to the blacklist based on \
        the mention an admin provides. Using `blacklistadd #mention` allows you to skip the prompt \
        and cut straight to adding a channel.",
    'whitelistremove' : "Aliases: `WLRemove`, `WL-`, `Whitelist-`.\nRemoves a channel from the list. \
        Using `whitelistremove #mention` allows you to skip the prompt and cut straight to removing a channel.",
    'blacklistremove' : "Aliases: `BLRemove`, `BL-`, `Blacklist-`.\nRemoves a channel from the list. \
        Using `whitelistremove #mention` allows you to skip the prompt and cut straight to removing a channel.",
    'replay' : "Aliases: `Play`, `Read`, `Reread`, `Watch`, `Rewatch`, `Rerun`, `Rewind`.\nBegins \
        the replay process. There's a lot of aliases for this one, so feel free to use whichever you like best."
}
##Setup
print ("Allow me a moment to wake up...")
client.remove_command("help")

##Events
@client.event
async def on_ready():
    print(f'{client.user} is alive!')
    await client.change_presence(activity=discord.Game(name='Ir.help for help.'))
    for i in client.guilds:
        await addServerVars(i)

@client.event
async def on_guild_channel_delete(channel):

    data = await readServerInfo(channel.guild.id)

    id = str(channel.id)

    if id in data['options']['whitelist']:
        data['options']['whitelist'].remove(id)
    if id in data['options']['blacklist']:
        data['options']['blacklist'].remove(id)

    await writeServerInfo(channel.guild.id,data)

    return

@client.event
async def on_guild_join(guild):
    await addServerVars(guild)

@client.event
async def on_guild_remove(guild):
    os.remove('serverData/'+ str(guild.id) + '.txt')


##Internal Functions
async def listenReactFunc(channel,userID,messageID,timeoutTime,blind):
    try:
        if blind: 
            return await client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id != client.user.id 
            and payload.channel_id == channel.id and payload.message_id == messageID, timeout=timeoutTime)
        else: 
            return await client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == userID
             and payload.channel_id == channel.id and payload.message_id == messageID, timeout=timeoutTime)
    except asyncio.TimeoutError:
        return

async def writeServerInfo(id, data):

    json_file = open('serverData/'+ str(id) + '.txt', 'w', encoding="utf-8")
    json_file.seek(0)
    json.dump(data, json_file, ensure_ascii=False, indent=4)
    json_file.close()

    return

async def readServerInfo(id):

    file = open('serverData/'+ str(id) + '.txt', 'r+', encoding="utf-8")
    data = json.load(file)
    file.close()

    return data

async def addServerVars(guild):

    id = guild.id

    if path.exists('serverData/'+ str(id) + '.txt'):
        pass

    else:
        now = datetime.now()
        data = {}

        data['serverDetails'] = {
            'Name' : str(guild.name),
            'ID' : str(id),
            'Entry Submission DTG' : now.strftime("%m/%d/%Y, %H:%M:%S")
        }
        data['options'] = {
            'paused' : 'False',
            'whitelist' : [],
            'blacklist' : []
        }

        file = open('serverData/'+ str(id) + '.txt', 'w')
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.close()
        print('Made data for server name ' + str(guild.name) + '.')
    
    return

async def notAnAdmin(channel,member):

    embed = discord.Embed(
    title = 'Not an Admin!',
    color = discord.Color(000000)
    ) 
    
    embed.add_field(name = 'Sorry!', value = 'You have to be an admin to do that, ' + member.name)
    embed.set_footer(text = 'This message will self destruct in five...four...')
    finalembed = await channel.send(embed=embed)

    await asyncio.sleep(5)
    await finalembed.delete()

async def deleteSelf(finalembed,channel):

    try: #Excuse itself and remove the message
        await finalembed.delete()
        exiting = await channel.send("No reaction recieved in the last minute. Closing...")
        await asyncio.sleep(5)
        await exiting.delete()
    except: #The message is already gone
        pass

async def promptFunc(channel,title,description,origin,*args):

    embed = discord.Embed(
    title = title,
    description = description,
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'Press the ↩️ to go back, or the ❌ to exit.')
    finalembed = await channel.send(embed=embed)
    
    try: #Add reactions, if message hasn't been closed out yet
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌')
    except: #Message is already gone
        return

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,None,finalembed.id,60,True)
    if rawReaction:
        reaction = str(rawReaction.emoji)
        await finalembed.delete()
        #Act based on reaction
        if reaction == '↩️' and origin != None:
            await origin(*args)
        elif reaction == '↩️':
            await helpFunc(channel)
        else:
            pass
    else:
        await deleteSelf(finalembed,channel)
    return

async def checkForGuild(channel):

    if channel.type != discord.ChannelType.text:
        await promptFunc(channel,'Woah, there.',"You can only access server commands if you're in a text channel in that server. Sorry.",None,None)
        return False
    else:
        return True

async def createReplayPrompt(channel,acceptedChannel,time,paused):

    message = (await acceptedChannel.history(after=time,limit=1).flatten())[0]

    embed = discord.Embed(
    title = 'Initializing...',
    description = 'Please wait while I add reactions.',
    color = discord.Color(000000)
    ) 
    
    finalembed = await channel.send(embed=embed)

    reactions = ['⬅️']
    if paused:
        reactions.append('▶️')        
    else:
        reactions.append('⏸️')
    reactions.extend(['➡️', '❌'])

    asyncio.create_task(addReactions(finalembed,reactions))

    deleteMessage = asyncio.create_task(replayDeleteMessageFunc(finalembed))
    await replayMessageFunc(message,finalembed,paused,deleteMessage)
    
    return 

async def addReactions(finalEmbed,reactions):

    try:
        for reaction in reactions:
            await finalEmbed.add_reaction(reaction)
    except:
        #Message has been deleted
        pass
    
    return

async def playNext(message,finalEmbed,deleteMessage):

    try:
        newMessage = (await message.channel.history(after=message.created_at,limit=1).flatten())[0]
    except:
        await asyncio.sleep(60)
        await replayNoMessageFunc(message,finalEmbed,True,deleteMessage)
        
    if newMessage.author == client.user:
        await asyncio.sleep(60)
        await replayNoMessageFunc(message,finalEmbed,True,deleteMessage)
    
    waitTime = (newMessage.created_at - message.created_at) / 2
    await asyncio.sleep(waitTime.total_seconds())
    await replayMessageFunc(newMessage,finalEmbed,False,deleteMessage)

    return


##Commands
@client.command(aliases=['h'])
async def help(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    words = ctx.message.content.split()

    if len(words) == 1:
        await helpFunc(ctx.channel)
    if words[1].lower() in helpMessages:
        await promptFunc(ctx.channel,words[1][0].upper() + words[1][1:].lower() + ' Documentation',helpMessages[words[1].lower()],helpFunc,ctx.channel)
    else:
        await promptFunc(ctx.channel,'Come again?',"I can tell that you tried to access documentation about a command, \
        but I can't actually tell what that command is. be sure that you made no typos.",helpFunc,ctx.channel)
        print(words[1])

    return

async def helpFunc(channel):

    embed = discord.Embed(
    title = 'Help Menu',
    description = 'Call with the full Ir.(command), or just click a reaction.',
    color = discord.Color(000000)
    ) 
    
    embed.add_field(name = ':question:  Tutorial', value = 'Walks you through what this does exactly, and how to use it.')
    embed.add_field(name = ':pencil:  Options', value = 'View the server settings.')
    embed.add_field(name = ':heart_decoration:  Support', value = 'Show the bot and its creator some love!')
    embed.add_field(name = 'Get your own IR bot?', value = "[Sure.](https://discord.com/oauth2/authorize?client_id=846523188262469672&scope=bot&permissions=76864)")
    finalembed = await channel.send(embed=embed)
    
    reactions = ['❓','📝','💟','❌']
    asyncio.create_task(addReactions(finalembed,reactions))

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,None,finalembed.id,60,True)
    if rawReaction:
        reaction = str(rawReaction.emoji)
        await finalembed.delete()
        #Act based on reaction
        if reaction == '❓':
            await tutorialFunc(channel)
        if reaction == '📝':
            await optionsFunc(channel)
        if reaction == '💟':
            await promptFunc(channel,'Aw, thanks.','If you want to thank me or tell me about some glitch in the bot, \
            you can contact me at David Lancaster#1532. Either is appreciated.',helpFunc,channel)
        else:
            pass
    else:
        await deleteSelf(finalembed,channel)
    
    return

@client.command(aliases=['guide'])
async def tutorial(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    await tutorialFunc(ctx.channel)
    return

async def tutorialFunc(channel):

    embed = discord.Embed(
    title = 'Tutorial Menu',
    description = 'Call with the full Ir.(command), or just click a reaction.',
    color = discord.Color(000000)
    ) 
    
    embed.add_field(name = ':notepad_spiral:  CommandList', value = 'A full list of every command and a brief description of each.')
    embed.add_field(name = ':grey_question:  CommandHelp', value = 'Shows you how to use Ir.help to get specific info about a command.')
    embed.add_field(name = ':man_teacher:  Examples', value = 'Gives you some examples on usage and possible applications.')
    finalembed = await channel.send(embed=embed)
    
    reactions = ['🗒️','❔','👨‍🏫','↩️','❌']
    asyncio.create_task(addReactions(finalembed,reactions))

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,None,finalembed.id,60,True)
    if rawReaction:
        reaction = str(rawReaction.emoji)
        await finalembed.delete()
        #Act based on reaction
        if reaction == '🗒️':
            await commandsFunc(channel)
        if reaction == '❔':
            await promptFunc(channel,'Using Ir.help',"You can use the command to bring up the main menu, yes, but it \
            has a second purpose. Typing a command after `Ir.help` will allow you to read information about that command \
            itself, like this:\n\n`Ir.help whitelist`\n\nIt will tell you about its pupose as well as 'aliases', \
            different ways to call that command. `help`, for instance, has the alias `h`, so you can use `Ir.h` whenever \
            you would want to call the whole thing. Aliases are usally faster to type and easier to remember, but \
            may not make as much sense as their full-length counterparts, like how `wl+` is an alias for `whitelistadd`. \
            With that in mind, if you want to view the documentation for a command, be sure you use the full-length version \
            and not an alias! It won't understand you otherwise. If you're having trouble remembering what it is, \
            you can review every command with `Ir.commandslist`, or just go back to the last menu and click the :notepad_spiral: .",
            tutorialFunc,channel)
        if reaction == '👨‍🏫':
            pass
        if reaction == '↩️':
            pass
        else:
            pass
    else:
        await deleteSelf(finalembed,channel)
    
    return


@client.command()
async def support(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    await promptFunc(ctx.channel,'Aw, thanks.','If you want to thank me or tell me about some glitch in the bot, \
        you can contact me at David Lancaster#1532. Either is appreciated.',helpFunc,ctx.channel)
    return


@client.command(aliases=['Commands'])
async def commandslist(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    await commandsFunc(ctx.channel)
    return

async def commandsFunc(channel):

    embed = discord.Embed(
    title = 'Commands List',
    description = 'Every command in the bot. All commands begin with "Ir." *(1)* = Must be in a server, *(2)* = Must be an administrator.',
    color = discord.Color(000000)
    ) 
    
    embed.add_field(name = 'General Help', value = """
    **Help:** Shows you the main menu, or gives you detailed info on a specific command (see Ir.CommandHelp). \n\
    **Tutorial:** A menu to help you learn the ins and outs of the Instant Replay Bot. \n\
    **CommandsList:** What you're looking at right now.\n\
    **Support:** Say hi or tell me what needs fixing.\
    """)

    embed.add_field(name = 'Settings', value = """
    **Options:** *(1).* A topical survey of the whitelist, blacklist, or the server's pause status. \n\
    **PauseMenu:** *(1).* Views whether or not the server is allowing replays, or if it's 'paused.' \n\
    **Pause:** *(1), (2).* Pauses the server. Ir.unpause does the opposite.\
    """)
    
    embed.add_field(name = 'Channel Lists', value = """
    (The same format is used for blacklists as it is for whitelists.) \n
    **Whitelist:** *(1).* Views the server's whitelist. \n\
    **WhitelistAdd:** *(1), (2).* Adds a channel to the server's whitelist.\n\
    **WhitelistRemove:** *(1), (2).* Removes a channel from the server's whitelist.\
    """)
    
    embed.add_field(name = 'Replay', value = """
    (There's only one command for this, but it triggers multiple steps.)
    **Replay:** Starts the channel replay process. The bot will ask you some questions about what you want to see.\n\
    **Identify Server:** If called in a channel, it'll replay from the current server. Otherwise, it'll ask for an invite, to know where to replay from.\n\
    **Add Channel:** Add a channel to the replay queue. You can #mention it or give its name.\n\
    **List Channels:** Gives you a list of all the channels about to be replayed from the given server.\n\
    **Remove Channel:** Takes a channel off the list, if it was added by accident.\n\
    **Add Time:** Clarify how far back the channel should be rewound, using either a date and/or time, or some duration.\n\
    **List Times:** Gives you a list of what times the channels will be rewound (you can rewind each seperately).\n\
    **Replay Message:** The actual replay. You can pause or unpause automatic progression of messages, and skip forward or backwards.\n\
    """)

    finalembed = await channel.send(embed=embed)
    
    reactions = ['↩️','❌']
    asyncio.create_task(addReactions(finalembed,reactions))

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,None,finalembed.id,600,True)
    if rawReaction:
        reaction = str(rawReaction.emoji)
        await finalembed.delete()
        #Act based on reaction
        if reaction == '↩️':
            await tutorialFunc(channel)
        else:
            pass
    else:
        try: #Excuse itself and remove the message
            await finalembed.delete()
            exiting = await channel.send("No reaction recieved in the last ten minutes. Closing...")
            await asyncio.sleep(5)
            await exiting.delete()
        except: #The message is already gone
            pass
    
    return

@client.command(aliases=['settings'])
async def options(ctx):
    
    if await checkForGuild(ctx.channel) == False:
        return

    await ctx.message.delete()
    await optionsFunc(ctx.channel) 

async def optionsFunc(channel):

    if await checkForGuild(channel) == False:
        return

    embed = discord.Embed(
    title = 'IR Settings',
    color = discord.Color(000000)
    ) 
    
    data = await readServerInfo(channel.guild.id)
    reactions = []

    if data['options']['paused'] == 'False':
        ra = '**allowed.**'
        reactions.append('⏸️')
        embed.add_field(name = 'Pause', value = reactions[0] + ' Replaying channels on this server is ' + ra)
        if not data['options']['whitelist'] and not data['options']['blacklist']:
            reactions.extend(['🔳', '🔲'])
            allowed = " **All** channels are available for replaying! Click on the :white_square_button: \
                to create a whitelist, or :black_square_button: to create a blacklist."
            embed.add_field(name = 'No Limits!', value = ':white_check_mark:' + allowed)
        if data['options']['whitelist']:
            reactions.append('🔳')
            allowed = ' **' + str(len(data['options']['whitelist'])) + '** channel(s) can be replayed at will.'
            embed.add_field(name = 'Whitelist', value = ':white_square_button:' + allowed)
        if data['options']['blacklist']:
            reactions.append('🔲')
            allowed = ' **' + str(len(data['options']['blacklist'])) + '** channel(s) cannot be replayed.'
            embed.add_field(name = 'Blacklist', value = ':black_square_button:' + allowed)
    else:
        ra = '**paused.**'
        reactions.append('▶️')
        embed.add_field(name = 'Unpause', value = reactions[0] + ' Replaying channels on this server is ' + ra)
    reactions.extend(['↩️', '❌'])
    

    embed.set_footer(text = 'Click a reaction to view the options for that setting.')
    finalembed = await channel.send(embed=embed)

    asyncio.create_task(addReactions(finalembed,reactions))

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,None,finalembed.id,60,True)
    if rawReaction:
        reaction = str(rawReaction.emoji)
        await finalembed.delete()
        #Act based on reaction
        if reaction == '⏸️' or reaction == '▶️':
            await pauseMenuFunc(channel)
        if reaction == '📝':
            await optionsFunc(channel)
        if reaction == '🔳':
            await channelListFunc(channel,'white')
        if reaction == '🔲':
            await channelListFunc(channel,'black')
        if reaction == '↩️' :
            await helpFunc(channel)
        else:
            pass
    else:
        await deleteSelf(finalembed,channel)
    return

@client.command(aliases=['pauseState'])
async def pauseMenu(ctx):

    if await checkForGuild(ctx.channel) == False:
        return

    await ctx.message.delete()
    await pauseMenuFunc(ctx.channel)
    return

async def pauseMenuFunc(channel):

    if await checkForGuild(channel) == False:
        return
    
    embed = discord.Embed(
    title = 'IR Pause Menu',
    color = discord.Color(000000)
    ) 
    
    data = await readServerInfo(channel.guild.id)
    reactions = []

    if data['options']['paused'] == 'False':
        reactions.append('⏸️')
        pauseTitle = 'Currently Unpaused'
        pauseText = "In other words, you're free to replay! This is the standard for most servers."
    else:
        reactions.append('▶️')
        pauseTitle = 'Currently Paused'
        pauseText = "An administrator has temporarily paused replaying on this server (probably just until they get the details sorted)."

    embed.add_field(name = pauseTitle, value = pauseText)
    embed.set_footer(text = 'Only admins may actually pause or unpause a server.')
    finalembed = await channel.send(embed=embed)

    reactions.extend(['↩️','❌'])
    asyncio.create_task(addReactions(finalembed,reactions))

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,None,finalembed.id,60,True)
    if rawReaction:
        reaction = str(rawReaction.emoji)
        await finalembed.delete()
        #Act based on reaction
        if reaction == '⏸️':
            await newPauseState(channel,rawReaction.member,True)
        if reaction == '▶️':
            await newPauseState(channel,rawReaction.member,False)
        if reaction == '↩️' :
            await optionsFunc(channel)
        else:
            pass
    else:
        await deleteSelf(finalembed,channel)
    return

@client.command(aliases=['p'])
async def pause(ctx):

    if await checkForGuild(ctx.channel) == False:
        return

    await ctx.message.delete()
    await newPauseState(ctx.channel,ctx.author,True)
    return

@client.command(aliases=['up'])
async def unpause(ctx):

    if await checkForGuild(ctx.channel) == False:
        return

    await ctx.message.delete()
    await newPauseState(ctx.channel, ctx.author, False)
    return

async def newPauseState(channel,member,nowPaused):

    if await checkForGuild(channel) == False:
        return

    if member.permissions_in(channel).administrator == False:
        await notAnAdmin(channel,member)

    data = await readServerInfo(channel.guild.id)
    data['options']['paused'] = str(nowPaused)
    await writeServerInfo(channel.guild.id,data)

    embed = discord.Embed(
    title = 'Pause Setting Updated!',
    color = discord.Color(000000)
    ) 
    
    if nowPaused:
        pauseStateTitle = ' is now paused.'
        pauseStateInformation = 'No channels may be replayed. Remember to unpause later.'
    else:
        pauseStateTitle = ' has been unpaused again.'
        pauseStateInformation = 'Replaying on this server is once more made possible. Rejoice.'

    
    embed.add_field(name = channel.guild.name + pauseStateTitle, value = pauseStateInformation)
    embed.set_footer(text = 'Remember, you can switch back at any time.')
    finalembed = await channel.send(embed=embed)
    
    reactions = ['↩️','❌']
    asyncio.create_task(addReactions(finalembed,reactions))

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,None,finalembed.id,60,True)
    if rawReaction:
        reaction = str(rawReaction.emoji)
        await finalembed.delete()
        #Act based on reaction
        if reaction == '↩️':
            await optionsFunc(channel)
        else:
            pass
    else:
        await deleteSelf(finalembed,channel)
    return

@client.command(aliases=['wl'])
async def whitelist(ctx):

    if await checkForGuild(ctx.channel) == False:
        return

    await ctx.message.delete()
    await channelListFunc(ctx.channel,'white')
    return

@client.command(aliases=['bl'])
async def blacklist(ctx):

    if await checkForGuild(ctx.channel) == False:
        return

    await ctx.message.delete()
    await channelListFunc(ctx.channel,'black')
    return

async def channelListFunc(channel,color):

    if await checkForGuild(channel) == False:
        return
    
    data = await readServerInfo(channel.guild.id)

    if color == 'white':
        listName = 'whitelist'
        upperListName = 'Whitelist'
        listDescription = "Everything in this list is eligible for replaying. Everything that's *not* here, well..."
        fieldValue = "That is to say, this is where the whitelist *would* be, \
            if there was one made. If there's also no blacklist (and replaying isn't paused, either), then that means \
            every channel can be replayed!"
        fieldName = 'Allowed channels...'
    else:
        listName = 'blacklist'
        upperListName = 'Blacklist'
        listDescription = "Channels listed here can't be replayed. Everything else, though, should be fair game."
        fieldValue = "Well, that is, this is where you'd put it, if there \
            was a blacklist made for this server. Since there's not, there's a good chance that all channels are \
            free to be replayed, unless there's a whitelist."
        fieldName = 'Prohibited channels...'


    embed = discord.Embed(
    title = 'Replay ' + upperListName + ' for ' + channel.guild.name,
    description = listDescription,
    color = discord.Color(000000)
    ) 

    reactions = ['✏️']

    if len(data['options'][listName]) == 0:
            embed.add_field(name = 'No ' + listName + '!', value = fieldValue)

    else:
        
        listChannels = ''
        for i in data['options'][listName]:
            listChannels += '<#' + i + '>\n'
        embed.add_field(name = fieldName, value = listChannels)
        reactions.append('🚮')

    reactions.extend(['↩️', '❌'])

    embed.set_footer(text = 'Admins can add or remove channels using the reactions at the bottom.')
    finalembed = await channel.send(embed=embed)
    
    asyncio.create_task(addReactions(finalembed,reactions))

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,None,finalembed.id,60,True)
    if rawReaction:
        reaction = str(rawReaction.emoji)
        await finalembed.delete()
        #Act based on reaction
        if reaction == '✏️':
            await channelListAddFunc(channel,rawReaction.member,color)
        if reaction == '🚮':
            await channelListRemoveFunc(channel,rawReaction.member,color)
        if reaction == '↩️':
            await optionsFunc(channel)
        else:
            pass
    else:
        await deleteSelf(finalembed,channel)
    return

@client.command(aliases=['wl+','whitelist+','wladd'])
async def whitelistadd(ctx):
    if await checkForGuild(ctx.channel) == False:
        return

    words = ctx.message.content.split()
    await ctx.message.delete()

    if len(words) == 1:
        await channelListAddFunc(ctx.channel,ctx.author,'white')

    else:
        listChannel = words[1][2:20]
        color = 'white'
        listName = 'whitelist'

        data = await readServerInfo(ctx.guild.id)

        try:
            if (await client.fetch_channel(listChannel)).type != discord.ChannelType.text:
                await promptFunc(ctx.channel,'Nice try.','<#' + listChannel + "> is a channel, but it's not a text channel \
                (so it can't be replayed anyways). This bot only handles text channels.",channelListAddFunc,ctx.channel,ctx.author,color)
                return
        except:
            await promptFunc(ctx.channel,'Channel not found!',"Couldn't add a channel that doesn't exist. \
                Double check that there's no typos.",channelListAddFunc,ctx.channel,ctx.author)
            return
        
        if listChannel in data['options'][listName]:
            await promptFunc(ctx.channel,'Wait a minute...','<#' + listChannel + '> is already on the list!',channelListAddFunc,ctx.channel,ctx.author,color)
            return
        
        data['options'][listName].append(listChannel)
        await writeServerInfo(ctx.guild.id,data)
        await promptFunc(ctx.channel,'Success!','Added <#' + listChannel + '> to the ' + listName + '.',channelListAddFunc,ctx.channel,ctx.author,color)

    return

@client.command(aliases=['bl+','blacklist+','bladd'])
async def blacklistadd(ctx):

    if await checkForGuild(ctx.channel) == False:
        return

    words = ctx.message.content.split()
    await ctx.message.delete()

    if len(words) == 1:
        await channelListAddFunc(ctx.channel,ctx.author,'black')

    else:
        listChannel = words[1][2:20]
        color = 'black'
        listName = 'blacklist'

        data = await readServerInfo(ctx.guild.id)

        try:
            if (await client.fetch_channel(listChannel)).type != discord.ChannelType.text:
                await promptFunc(ctx.channel,'Nice try.','<#' + listChannel + "> is a channel, but it's not a text channel \
                (so it can't be replayed anyways). This bot only handles text channels.",channelListAddFunc,ctx.channel,ctx.author,color)
                return
        except:
            await promptFunc(ctx.channel,'Channel not found!',"Couldn't add a channel that doesn't exist. \
                Double check that there's no typos.",channelListAddFunc,ctx.channel,ctx.author)
            return
        
        if listChannel in data['options'][listName]:
            await promptFunc(ctx.channel,'Wait a minute...','<#' + listChannel + '> is already on the list!',channelListAddFunc,ctx.channel,ctx.author,color)
            return
        
        data['options'][listName].append(listChannel)
        await writeServerInfo(ctx.guild.id,data)
        await promptFunc(ctx.channel,'Success!','Added <#' + listChannel + '> to the ' + listName + '.',channelListAddFunc,ctx.channel,ctx.author,color)

    return

async def channelListAddFunc(channel,member,color):

    if await checkForGuild(channel) == False:
        return

    if member.permissions_in(channel).administrator == False:
        await notAnAdmin(channel,member)
    
    data = await readServerInfo(channel.guild.id)

    if color == 'white':
        listName = 'whitelist'
        upperListName = 'Whitelist'
    else:
        listName = 'blacklist'
        upperListName = 'Blacklist'


    embed = discord.Embed(
    title = 'Add Channel to ' + upperListName,
    description = 'Just #mention a channel.',
    color = discord.Color(000000)
    ) 

    embed.set_footer(text = 'This message will delete itself in 60 seconds.')
    finalembed = await channel.send(embed=embed)
    
    
    reactions = ['↩️','❌']
    asyncio.create_task(addReactions(finalembed,reactions))
    
    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id != client.user.id
     and payload.channel_id == channel.id and payload.message_id == finalembed.id, timeout=60)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id != client.user.id
                    and message.channel.id == channel.id, timeout=60))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
    except:
        await deleteSelf(finalembed,channel)
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        await finalembed.delete()
        reaction = str(result.emoji)
        if reaction == '↩️':     
            await channelListFunc(channel,color)
        else:
            pass
            
    if resultType == 'message':
        await finalembed.delete()
        listChannel = result.content[2:20]
        await result.delete()

        try:
            if (await client.fetch_channel(listChannel)).type != discord.ChannelType.text:
                await promptFunc(channel,'Nice try.','<#' + listChannel + "> is a channel, but it's not a text channel \
                (so it can't be replayed anyways). This bot only handles text channels.",channelListAddFunc,channel,member,color)
                return
        except:
            await promptFunc(channel,'Channel not found!',"Couldn't add a channel that doesn't exist. \
                Double check that there's no typos.",channelListAddFunc,channel,member)
            return
        
        if listChannel in data['options'][listName]:
            await promptFunc(channel,'Wait a minute...','<#' + listChannel + '> is already on the list!',channelListAddFunc,channel,member,color)
            return
        
        data['options'][listName].append(listChannel)
        await writeServerInfo(channel.guild.id,data)
        await promptFunc(channel,'Success!','Added <#' + listChannel + '> to the ' + listName + '.',channelListAddFunc,channel,member,color)

    return

@client.command(aliases=['wl-','whitelist-','wlremove'])
async def whitelistremove(ctx):

    if await checkForGuild(ctx.channel) == False:
        return

    words = ctx.message.content.split()
    await ctx.message.delete()

    if len(words) == 1:
        await channelListRemoveFunc(ctx.channel,ctx.author,'white')

    else:
        listChannel = words[1][2:20]
        color = 'white'
        listName = 'whitelist'

        data = await readServerInfo(ctx.guild.id)

        try:
            if (await client.fetch_channel(listChannel)).type != discord.ChannelType.text:
                await promptFunc(ctx.channel,'Nice try.','<#' + listChannel + "> is a channel, but it's not a text channel \
                (so it can't be replayed anyways). This bot only handles text channels.",channelListRemoveFunc,ctx.channel,ctx.author,color)
                return
        except:
            await promptFunc(ctx.channel,'Channel not found!',"Couldn't remove a channel that doesn't exist. \
                Double check that there's no typos.",channelListRemoveFunc,ctx.channel,ctx.author)
            return
        
        if listChannel not in data['options'][listName]:
            await promptFunc(ctx.channel,'Wait a minute...','<#' + listChannel + "> isn't on the list! Maybe you removed it already?",channelListRemoveFunc,ctx.channel,ctx.author,color)
            return
        
        data['options'][listName].remove(listChannel)
        await writeServerInfo(ctx.channel.guild.id,data)
        await promptFunc(ctx.channel,'Success!','Removed <#' + listChannel + '> from the ' + listName + '.',channelListRemoveFunc,ctx.channel,ctx.author,color)

    return

@client.command(aliases=['bl-','blacklist-','blremove'])
async def blacklistremove(ctx):

    if await checkForGuild(ctx.channel) == False:
        return

    words = ctx.message.content.split()
    await ctx.message.delete()

    if len(words) == 1:
        await channelListRemoveFunc(ctx.channel,ctx.author,'black')

    else:
        listChannel = words[1][2:20]
        color = 'black'
        listName = 'blacklist'

        data = await readServerInfo(ctx.guild.id)

        try:
            if (await client.fetch_channel(listChannel)).type != discord.ChannelType.text:
                await promptFunc(ctx.channel,'Nice try.','<#' + listChannel + "> is a channel, but it's not a text channel \
                (so it can't be replayed anyways). This bot only handles text channels.",channelListRemoveFunc,ctx.channel,ctx.author,color)
                return
        except:
            await promptFunc(ctx.channel,'Channel not found!',"Couldn't remove a channel that doesn't exist. \
                Double check that there's no typos.",channelListRemoveFunc,ctx.channel,ctx.author)
            return
        
        if listChannel not in data['options'][listName]:
            await promptFunc(ctx.channel,'Wait a minute...','<#' + listChannel + "> isn't on the list! Maybe you removed it already?",channelListRemoveFunc,ctx.channel,ctx.author,color)
            return
        
        data['options'][listName].remove(listChannel)
        await writeServerInfo(ctx.channel.guild.id,data)
        await promptFunc(ctx.channel,'Success!','Removed <#' + listChannel + '> from the ' + listName + '.',channelListRemoveFunc,ctx.channel,ctx.author,color)

    return

async def channelListRemoveFunc(channel,member,color):

    if await checkForGuild(channel) == False:
        return

    if member.permissions_in(channel).administrator == False:
        await notAnAdmin(channel,member)
    
    data = await readServerInfo(channel.guild.id)

    if color == 'white':
        listName = 'whitelist'
        upperListName = 'Whitelist'
    else:
        listName = 'blacklist'
        upperListName = 'Blacklist'


    embed = discord.Embed(
    title = 'Remove Channel from ' + upperListName,
    description = 'Just #mention a channel.',
    color = discord.Color(000000)
    ) 

    embed.set_footer(text = 'This message will delete itself in 60 seconds.')
    finalembed = await channel.send(embed=embed)
    
    reactions = ['↩️','❌']
    asyncio.create_task(addReactions(finalembed,reactions))

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id != client.user.id
    and payload.channel_id == channel.id and payload.message_id == finalembed.id, timeout=60)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id != client.user.id
                    and message.channel.id == channel.id, timeout=60))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
    except:
        await deleteSelf(finalembed,channel)
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        await finalembed.delete()
        reaction = str(result.emoji)
        if reaction == '↩️':     
            await channelListFunc(channel,color)
        else:
            pass
            
    if resultType == 'message':
        await finalembed.delete()
        listChannel = result.content[2:20]
        await result.delete()

        try:
            if (await client.fetch_channel(listChannel)).type != discord.ChannelType.text:
                await promptFunc(channel,'Nice try.','<#' + listChannel + "> is a channel, but it's not a text channel \
                (so it can't be replayed anyways). This bot only handles text channels.",channelListRemoveFunc,channel,member,color)
                return
        except:
            await promptFunc(channel,'Channel not found!',"Couldn't remove a channel that doesn't exist. \
                Double check that there's no typos.",channelListRemoveFunc,channel,member)
            return
        
        if listChannel not in data['options'][listName]:
            await promptFunc(channel,'Wait a minute...','<#' + listChannel + "> isn't on the list! Maybe you removed it already?",channelListRemoveFunc,channel,member,color)
            return
        
        data['options'][listName].remove(listChannel)
        await writeServerInfo(channel.guild.id,data)
        await promptFunc(channel,'Success!','Removed <#' + listChannel + '> from the ' + listName + '.',channelListRemoveFunc,channel,member,color)

    return

@client.command(aliases=['read','reread','watch','rewatch','rerun','play','rewind'])
async def replay(ctx):

    words = ctx.message.content.split()

    try:
        await ctx.message.delete()
    except:
        pass

    if len(words) == 1:

        if ctx.channel.type == discord.ChannelType.text:
            await replayIdentifyGuildFunc(ctx.author,ctx.channel,ctx.guild)

        else:
            await replayIdentifyGuildFunc(ctx.author,ctx.channel,None)

    else:
        try:            
            inviteObject = await client.fetch_invite(words[1])
            guild = inviteObject.guild
            await replayIdentifyGuildFunc(ctx.author,ctx.channel,guild)
        except:
            await promptFunc(ctx.channel,'What was that?', "If you want to replay an specific server, \
                you have to send me a valid invite.",replayIdentifyGuildFunc,ctx.author,ctx.channel,None)
        
    return

async def replayIdentifyGuildFunc(user,channel,guild):

    if guild == None:

        embed = discord.Embed(
        title = 'Replay a Server',
        description = 'Just send me an invite to the server you want to replay.',
        color = discord.Color(000000)
        ) 

        embed.set_footer(text = 'This message will delete itself in 60 seconds.')
        finalembed = await channel.send(embed=embed)
        
        reactions = ['↩️','❌']
        asyncio.create_task(addReactions(finalembed,reactions))

        #Wait for either reaction or reply
        pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id != client.user.id
        and payload.channel_id == channel.id and payload.message_id == finalembed.id, timeout=60)),
                        asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id != client.user.id
                        and message.channel.id == channel.id, timeout=60))]
        done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
        #Cancel whichever task would have come second
        for task in pending_tasks:
            task.cancel()
        #Return completed task result
        try: 
            result = (done_tasks.pop().result())
            if isinstance(result, discord.message.Message):
                resultType = 'message'
            if isinstance(result, discord.raw_models.RawReactionActionEvent):
                resultType = 'reaction'
        except:
            await deleteSelf(finalembed,channel)
            return
        

        #Act based on reaction
        if resultType == 'reaction':
            await finalembed.delete()
            reaction = str(result.emoji)
            if reaction == '↩️':     
                await helpFunc(channel)
            else:
                pass
            return
                
        if resultType == 'message':
            await finalembed.delete()
            try:
                await result.delete()
            except:
                pass
            try:            
                inviteObject = await client.fetch_invite(result.content)
                guild = inviteObject.guild
            except:
                await promptFunc(channel,'What was that?', "If you want to replay an specific server, you have to send me a valid invite.",replayIdentifyGuildFunc,user,channel,None)
                return

    try:
        guild.get_member(client.user.id)
    except:
        await promptFunc(channel,'Hm? ' + guild.name + '?', "I don't know what's going on in that server, I'm not actually in it...",helpFunc,channel)
        return

    if await guild.fetch_member(user.id) == None:
        await promptFunc(channel,'Nice try.', "Trying to sneak a peek into a server you're not actually in, eh?",helpFunc,channel)
        return
    
    data = await readServerInfo(guild.id)

    if data['options']['paused'] == 'True':
        await promptFunc(channel,'Not quite yet.', "Someone in " + guild.name + " paused replays for the server. You'll have to wait until it's unpaused again.",helpFunc,channel)
        return

    await replayAddChannelFunc(user,channel,guild,[],None)

    return

async def replayAddChannelFunc(user,channel,guild,acceptedChannels,offeredChannelText):

    if offeredChannelText == None:

        embed = discord.Embed(
        title = 'Add Channel to Replay',
        description = 'To add a new channel to the replay queue, just #mention it or say its name.',
        color = discord.Color(000000)
        ) 

        embed.set_footer(text = 'This message will delete itself in 60 seconds.')
        finalembed = await channel.send(embed=embed)
        
        reactions = ['↩️','❌']
        asyncio.create_task(addReactions(finalembed,reactions))
        

        #Wait for either reaction or reply
        pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id != client.user.id
        and payload.channel_id == channel.id and payload.message_id == finalembed.id, timeout=60)),
                        asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id != client.user.id
                        and message.channel.id == channel.id, timeout=60))]
        done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
        #Cancel whichever task would have come second
        for task in pending_tasks:
            task.cancel()
        #Return completed task result
        try: 
            result = (done_tasks.pop().result())
            if isinstance(result, discord.message.Message):
                resultType = 'message'
            if isinstance(result, discord.raw_models.RawReactionActionEvent):
                resultType = 'reaction'
        except:
            await deleteSelf(finalembed,channel)
            return
            

        #Act based on reaction
        if resultType == 'reaction':
            await finalembed.delete()
            reaction = str(result.emoji)
            if reaction == '↩️':     
                await replayListChannelsFunc(channel,guild,acceptedChannels)
            else:
                pass
            return
                
        if resultType == 'message':
            await finalembed.delete()
            try:
                await result.delete()
            except:
                pass
            offeredChannelText = result.content
            
    if offeredChannelText[0] == '<':
        try:
            offeredChannel = guild.get_channel(int(offeredChannelText[2:20]))
        except:
            await promptFunc(channel,"Bad #mention?","I can't find a channel that matches that in the server \
            you want. Be sure that it's a sound #mention for " + guild.name + '.',
            replayAddChannelFunc,(await client.fetch_user(result.author.id),channel,guild,acceptedChannels,None))
            return
    else:
        correctedChannelName = offeredChannelText.lower().replace(' ','-')
        offeredChannel = discord.utils.get(guild.channels, name= correctedChannelName)
        if offeredChannel == None:
            await promptFunc(channel,"What's its name again?","I can't find a channel named " + correctedChannelName
            + ' in ' + guild.name + ". Double check there's no typos and you're asking about the right server.",
            replayAddChannelFunc,(await client.fetch_user(result.author.id)),channel,guild,acceptedChannels,None)
            return       

    if offeredChannel.type != discord.ChannelType.text:
        await promptFunc(channel,'Nice try.',offeredChannel.mention + " is a channel, but it's not a text channel, \
        so it can't be replayed. This bot only handles text channels.",replayAddChannelFunc,(await client.fetch_user(result.author.id)),channel,guild,acceptedChannels,None)
        return
    
    if user.permissions_in(offeredChannel).read_messages == False:
        await promptFunc(channel,'Thought you were slick, huh?',offeredChannel.mention + " isn't a channel you can read normally, \
        so it's not a channel you can read here, either.",replayAddChannelFunc,user,channel,guild,acceptedChannels,None)
        return

    if offeredChannel in acceptedChannels:
        await promptFunc(channel,'Deja vu.',offeredChannel.mention + " is already queued for replay! \
        No need to add it twice.",replayListChannelsFunc,channel,guild,acceptedChannels)
        return

    data = await readServerInfo(guild.id)

    if data['options']['whitelist'] and str(offeredChannel.id) not in data['options']['whitelist']:
        await promptFunc(channel,'Not whitelisted!',"There's a whitelist in " + guild.name + ', and ' + offeredChannel.mention + " isn't on it. \
        Sorry, buster.",replayListChannelsFunc,channel,guild,acceptedChannels)
        return

    if str(offeredChannel.id) in data['options']['blacklist']:
        await promptFunc(channel,'Blacklisted!',"Sorry, but " + offeredChannel.mention + " is on the blacklist. \
        Maybe it'll be removed by an admin in " + guild.name + ' soon?',replayListChannelsFunc,channel,guild,acceptedChannels)
        return

    acceptedChannels.append(offeredChannel)
    await promptFunc(channel,'Success!','Added ' + offeredChannel.mention + ' to the list of queued channels.',replayAddChannelFunc,user,channel,guild,acceptedChannels,None)

    return

async def replayListChannelsFunc(channel,guild,acceptedChannels):

    embed = discord.Embed(
    title = 'Replay Queue for ' + guild.name,
    description = 'The list of channels about to be replayed.',
    color = discord.Color(000000)
    ) 

    if not acceptedChannels:
        embed.add_field(name = 'Empty queue!', value = "You can't replay channels unless you queue them up first. Add some new ones to the list with ✏️.")
        reactions = ['✏️']
    else:
        queueList = ''
        for item in acceptedChannels:
            queueList += item.mention + '\n'
        embed.add_field(name = 'Channels', value = queueList)
        reactions = ['▶️','✏️','🚮']
        
    reactions.extend(['↩️', '❌'])
    embed.set_footer(text = "The next step is to determine from how long ago you want to rewind.")
    finalembed = await channel.send(embed=embed)
    
    asyncio.create_task(addReactions(finalembed,reactions))

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,None,finalembed.id,60,True)
    if rawReaction:
        reaction = str(rawReaction.emoji)
        await finalembed.delete()
        #Act based on reaction
        if reaction == '▶️':
            await replayRequestTimeFunc(channel,guild,acceptedChannels,[])
        if reaction == '✏️':
            await replayAddChannelFunc((await client.fetch_user(rawReaction.user_id)),channel,guild,acceptedChannels,None)
        if reaction == '🚮':
            await replayRemoveChannelFunc(channel,guild,acceptedChannels)
        if reaction == '↩️':
            await helpFunc(channel)
        else:
            pass
    else:
        await deleteSelf(finalembed,channel)
    
    return

async def replayRemoveChannelFunc(channel,guild,acceptedChannels):

    embed = discord.Embed(
    title = 'Remove Channel from Replay',
    description = 'Remove a channel by #mentioning it or saying its name.',
    color = discord.Color(000000)
    ) 

    embed.set_footer(text = 'This message will delete itself in 60 seconds.')
    finalembed = await channel.send(embed=embed)
    
    reactions = ['↩️','❌']
    asyncio.create_task(addReactions(finalembed,reactions))

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id != client.user.id
    and payload.channel_id == channel.id and payload.message_id == finalembed.id, timeout=60)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id != client.user.id
                    and message.channel.id == channel.id, timeout=60))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
    except:
        await deleteSelf(finalembed,channel)
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        await finalembed.delete()
        reaction = str(result.emoji)
        if reaction == '↩️':     
            await replayListChannelsFunc(channel,guild,acceptedChannels)
        else:
            pass
            
    if resultType == 'message':
            await finalembed.delete()
            try:
                await result.delete()
            except:
                pass
            offeredChannelText = result.content
            
    if offeredChannelText[0] == '<':
        try:
            offeredChannel = guild.get_channel(int(offeredChannelText[2:20]))
        except:
            await promptFunc(channel,"Bad #mention?","There's nothing like that in the server you want. \
            I can only remove channels in this queue properly mentioned from " + guild.name + '.',replayListChannelsFunc,channel,guild,acceptedChannels)
            return
    else:
        correctedChannelName = offeredChannelText.lower().replace(' ','-')
        offeredChannel = discord.utils.get(guild.channels, name= correctedChannelName)
        if offeredChannel == None:
            await promptFunc(channel,"You...what?","I can't find a channel named " + correctedChannelName
            + ' in ' + guild.name + ". Double check there's no typos and I can remove the right channel next time.",
            replayListChannelsFunc,channel,guild,acceptedChannels)
            return       

    if offeredChannel not in acceptedChannels:
        await promptFunc(channel,'Have we done this before?', offeredChannel + " isn't on the list! Maybe you removed it already?",replayListChannelsFunc,channel,guild,acceptedChannels)
        return
    
    acceptedChannels.remove(offeredChannel)
    await promptFunc(channel,'Success!','Removed ' + offeredChannel.mention + ' from the queue.',replayListChannelsFunc,channel,guild,acceptedChannels)

    return

async def replayRequestTimeFunc(channel,guild,acceptedChannels,acceptedTimes):

    currentChannel = acceptedChannels[len(acceptedTimes)]

    embed = discord.Embed(
    title = 'Add Time for Channel Replay',
    description = 'How far back should ' + currentChannel.mention + ' be rewound?',
    color = discord.Color(000000)
    ) 

    embed.add_field(name = 'Talk normally!', value = "I understand most ways of denoting time. This is by no means a complete list, but some examples are... \n\
        'Two days ago' \n\
        'Yesterday' \n\
        '1/31/01' \n\
        '4:20, PST :sunglasses:' \n\
        'Last week' \n\
        'Tuesday at 7:00 cst' \n\
        'September 04, 1904' \n\
        Just be sure to put your timezone in the message somewhere or convert to UTC first, since Discord doesn't tell bots what your timezone is. :(")
    embed.set_footer(text = 'This message will delete itself in 60 seconds.')
    finalembed = await channel.send(embed=embed)
    
    reactions = ['↩️','❌']
    asyncio.create_task(addReactions(finalembed,reactions))

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id != client.user.id
    and payload.channel_id == channel.id and payload.message_id == finalembed.id, timeout=60)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id != client.user.id
                    and message.channel.id == channel.id, timeout=60))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
    except:
        await deleteSelf(finalembed,channel)
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        await finalembed.delete()
        reaction = str(result.emoji)
        if reaction == '↩️':     
            await replayListTimeFunc(channel,guild,acceptedChannels,acceptedTimes)
        else:
            pass
        return
            
    if resultType == 'message':
        await finalembed.delete()
        try:
            await result.delete()
        except:
            pass
        await channel.trigger_typing()
        date = dateparser.parse(result.content,languages=['en'])

    if date == None:
        await promptFunc(channel,"Whoops.","I know I said I can understand most things, but maybe not *all* things. \
            Check back at the list for what I can most easily understand (whatever you just said doesn't qualify).",
            replayRequestTimeFunc,channel,guild,acceptedChannels,acceptedTimes)
        return

    if date > datetime.now():
        await promptFunc(channel,"This can't be right.","I can only replay messages from the past. If you said something like '7:00', be sure to add in 'Yesterday' somewhere in there.",replayRequestTimeFunc,channel,guild,acceptedChannels,acceptedTimes)
        return

    embed = discord.Embed(
    title = 'Add Time for Channel Replay',
    description = 'How far back should the channel be rewound?',
    color = discord.Color(000000)
    ) 

    embed.add_field(name = 'Is this right?', value = 'As I understand it, you want to rewind '
    + currentChannel.mention + date.strftime(" to %A, %B %d, %R %p. Does that sound about right?"))
    embed.set_footer(text = 'This message will delete itself in 60 seconds.')
    finalembed = await channel.send(embed=embed)
    
    reactions = ['✅','↩️','❌']
    asyncio.create_task(addReactions(finalembed,reactions))

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,None,finalembed.id,60,True)
    if rawReaction:
        reaction = str(rawReaction.emoji)
        await finalembed.delete()
        #Act based on reaction
        if reaction == '↩️':
            await replayListTimeFunc(channel,guild,acceptedChannels,acceptedTimes)
        if reaction == '✅':
            acceptedTimes.append(date)
            await promptFunc(channel,"Accepted!", currentChannel.mention + ' will replay from ' + date.strftime("%A, %B %d, %R %p.")
            ,replayListTimeFunc,channel,guild,acceptedChannels,acceptedTimes)
        if reaction == '❌':
            pass
        else:
            pass
    else:
        await deleteSelf(finalembed,channel)
    return

async def replayListTimeFunc(channel,guild,acceptedChannels,acceptedTimes):

    channelTimesDict = {}

    embed = discord.Embed(
    title = 'Channel Replay Times',
    description = 'See when each channel will begin playback.',
    color = discord.Color(000000)
    ) 

    reactions = []

    if not acceptedTimes:
        embed.add_field(name = 'How far back?', value = "The next step is to set a time for the channels. \
        You only have to specify one time, which all channels will be rewound to--but you can keep \
        going and set a specific time for each channel, instead, if you'd like them out of sync.")
        reactions.append('✏️')
    else:
        timesList = ''
        reactions.append('▶️')
        for givenChannel, givenTime in zip(acceptedChannels,acceptedTimes):
            channelTimesDict.update({givenChannel : givenTime})
            timesList += givenChannel.mention + givenTime.strftime(": %A, %B %d, %I:%M %p.\n")
        if len(acceptedChannels) > len(acceptedTimes):
            timesList += givenTime.strftime("------------------- \
            \nThe following channels will also use the last input time of  %A, %B %d, %R %p.\n")
            for index in range(len(acceptedTimes),len(acceptedChannels)):
                timesList += acceptedChannels[index].mention + '\n'
                channelTimesDict.update({acceptedChannels[index] : acceptedTimes[-1]})
            reactions.append('✏️')
        embed.add_field(name = 'Current List', value = timesList)
    
    reactions.extend(['↩️', '❌'])
        
    embed.set_footer(text = 'This message will delete itself in 60 seconds.')

    finalembed = await channel.send(embed=embed)
    
    asyncio.create_task(addReactions(finalembed,reactions))

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,None,finalembed.id,60,True)
    if rawReaction:
        await finalembed.delete()
        reaction = str(rawReaction.emoji)
        if reaction == '▶️':
            for key, value in channelTimesDict.items():
                asyncio.create_task(createReplayPrompt(channel,key,value,False))
        if reaction == '✏️':
            await replayRequestTimeFunc(channel,guild,acceptedChannels,acceptedTimes)
        if reaction == '↩️':
            pass
        else:
            pass
    else:
        await deleteSelf(finalembed,channel)
    
    return

@client.command()
async def t(ctx):

    try:
        await ctx.message.delete()
    except:
        pass

    channel = ctx.channel
    guild = client.get_guild(846583238063685632)
    acceptedChannel = guild.get_channel(846583238063685635)
    otherChannel = guild.get_channel(848725825377402920)
    time = datetime.strptime('06/1/21 21:30:00', '%m/%d/%y %H:%M:%S')

    await replayListTimeFunc(channel,guild,[acceptedChannel],[time])

    return

async def replayMessageFunc(message,finalEmbed,paused,deleteMessage):
    
    deleteMessage.cancel()

    embed = discord.Embed(
    title = message.author.display_name,
    description = message.content,
    color = discord.Color(000000)
    ) 

    embed.set_footer(text=message.created_at.strftime("Sent on %A, %B %d, at %I:%M %p."),icon_url=message.author.avatar_url)
    try:
        await finalEmbed.edit(embed=embed)
    except:
        pass

    if not paused:
        playNextTask = asyncio.create_task(playNext(message,finalEmbed,deleteMessage))
    
    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(finalEmbed.channel,None,finalEmbed.id,600,True)
    deleteMessage = asyncio.create_task(replayDeleteMessageFunc(finalEmbed))
    if rawReaction:
        reaction = str(rawReaction.emoji)
        if finalEmbed.channel.type == discord.ChannelType.text:
            try:
                await finalEmbed.remove_reaction(reaction,rawReaction.member)
            except:
                pass
        #Act based on reaction
        if not paused:
            playNextTask.cancel()
        if reaction == '⬅️':
            try:
                message = (await message.channel.history(before=message.created_at,limit=1).flatten())[0]
            except:
                await replayNoMessageFunc(message,finalEmbed,paused,deleteMessage)
        if reaction == '▶️':
            await finalEmbed.clear_reactions()
            await asyncio.sleep(1)
            paused = False
            reactions = ['⬅️','⏸️','➡️','❌']
            asyncio.create_task(addReactions(finalEmbed,reactions))
        if reaction == '⏸️':
            await finalEmbed.clear_reactions()
            await asyncio.sleep(1)
            paused = True
            await finalEmbed.clear_reactions()
            reactions = ['⬅️','▶️','➡️','❌']
            asyncio.create_task(addReactions(finalEmbed,reactions))
        if reaction == '➡️':
            try:
                message = (await message.channel.history(after=message.created_at,limit=1).flatten())[0]
            except:
                await replayNoMessageFunc(message,finalEmbed,paused,deleteMessage)
        if reaction == '❌':
            deleteMessage.cancel()
            await finalEmbed.delete()
            return
        else:
            pass
        if message.author == client.user:
            await replayNoMessageFunc(message,finalEmbed,paused,deleteMessage)
        await replayMessageFunc(message,finalEmbed,paused,deleteMessage)
    else:
        pass

        pass

    return

async def replayDeleteMessageFunc(finalEmbed):
    await asyncio.sleep(10)
    try:
        await finalEmbed.delete()
        exiting = await finalEmbed.channel.send("No reaction recieved in the last ten minutes. Closing...")
        await asyncio.sleep(5)
        await exiting.delete()
    except:
        pass

async def replayNoMessageFunc(message,finalEmbed,paused,deleteMessage):
    
    deleteMessage.cancel()

    embed = discord.Embed(
    title = 'End of the line.',
    description = "I've run out of messages to show you. You're either all caught up, \
        if you were replaying, or you've rewound all the way, if you were going backwards.",
    color = discord.Color(000000)
    ) 

    #embed.set_thumbnail(url=embed.Empty)
    embed.set_footer(text=embed.Empty)
    try:
        await finalEmbed.edit(embed=embed)
    except:
        pass

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(finalEmbed.channel,None,finalEmbed.id,600,True)
    deleteMessage = asyncio.create_task(replayDeleteMessageFunc(finalEmbed))
    if rawReaction:
        reaction = str(rawReaction.emoji)
        if finalEmbed.channel.type == discord.ChannelType.text:
            try:
                await finalEmbed.remove_reaction(reaction,rawReaction.member)
            except:
                pass
        #Act based on reaction
        if reaction == '⬅️':
            try:
                message = (await message.channel.history(before=message.created_at,limit=1).flatten())[0]
            except:
                await replayNoMessageFunc(message,finalEmbed,paused,deleteMessage)
        if reaction == '▶️' or reaction == '⏸️':
            paused = not paused
            reactions = ['⬅️']
            if paused:
                reactions.append('▶️')        
            else:
                reactions.append('⏸️')
            reactions.extend(['➡️', '❌'])
        if reaction == '➡️':
            try:
                message = (await message.channel.history(after=message.created_at,limit=1).flatten())[0]
            except:
                await replayNoMessageFunc(message,finalEmbed,paused,deleteMessage)
        if reaction == '❌':
            deleteMessage.cancel()
            await finalEmbed.delete()
            return
        else:
            pass
        if message.author == client.user:
            await replayNoMessageFunc(message,finalEmbed,paused,deleteMessage)
        await replayMessageFunc(message,finalEmbed,paused,deleteMessage)
    else:
        pass

        pass

    return


#Execute
client.run(environ['discordToken'])