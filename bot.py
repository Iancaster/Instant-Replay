
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
letters = list(string.ascii_lowercase)
countryFlags = {'Ascension Island' : '🇦🇨', 'Andorra' : '🇦🇩', 'United Arab Emirates' : '🇦🇪', 'UAE' : '🇦🇪', 'U.A.E.' : '🇦🇪',
                'Afghanistan' : '🇦🇫', 'Antigua & Barbuda' : '🇦🇬', 'Antigua' : '🇦🇬', 'Barbuda' : '🇦🇬', 'Anguilla' : '🇦🇮',
                'Albania' : '🇦🇱', 'Armenia' : '🇦🇲', 'Angola' : '🇦🇴', 'Antarctica' : '🇦🇶', 'Argentina' : '🇦🇷', 
                'American Samoa' : '🇦🇸', 'Samoa' : '🇦🇸', 'Austria' : '🇦🇹', 'Australia' : '🇦🇺', 'Aruba' : '🇦🇼', 
                'Aland Islands' : '🇦🇽', 'Azerbaijan' : '🇦🇿' , 'Bosnia and Herzegovina' : '🇧🇦', 'Bosnia' : '🇧🇦',
                'Herzegovina' : '🇧🇦', 'Barbados' : '🇧🇧', 'Bangladesh' : '🇧🇩', 'Belgium' : '🇧🇪', 'Burkina Faso' : '🇧🇫',
                'Bulgaria' : '🇧🇬', 'Bahrain' : '🇧🇭', 'Burundi' : '🇧🇮', 'Benin' : '🇧🇯', 'St. Barthelemy' : '🇧🇱',
                'Saint Barthelemy' : '🇧🇱', 'Bermuda' : '🇧🇲', 'Brunei' : '🇧🇳', 'Bolivia' : '🇧🇴', 'Carribean Netherlands' : '🇧🇶',
                'Brazil' : '🇧🇷', 'Bahamas' : '🇧🇸', 'Bhutan' : '🇧🇹', 'Bouvet Island' : '🇧🇻', 'Botswana' : '🇧🇼',
                'Belarus' : '🇧🇾', 'Belize' : '🇧🇿', 'Canada' : '🇨🇦', 'Cocos Islands' : '🇨🇨', 'Keeling Islands' : '🇨🇨',
                'Congo - Kinshasa' : '🇨🇩', 'Central African Republic' : '🇨🇫', 'CAE' : '🇨🇫', 'C.A.E.' : '🇨🇫',
                'Congo - Brazzaville' : '🇨🇬', 'Switzerland' : '🇨🇭', "Cote d'lvoire" : '🇨🇮', 'Cook Islands' : '🇨🇰',
                'Chile' : '🇨🇱', 'Cameroon' : '🇨🇲', 'China' : '🇨🇳', 'Colombia' : '🇨🇴', 'Clipperton Island' : '🇨🇵',
                'Costa Rica' : '🇨🇷', 'Cuba' : '🇨🇺', 'Cape Verde' : '🇨🇻', 'Curacoa' : '🇨🇼', 'Christmas Island' : '🇨🇽',
                'Cyprus' : '🇨🇾', 'Czechia' : '🇨🇿', 'Germany' : '🇩🇪', 'Diego Garcia' : '🇩🇬', 'Djibouti' : '🇩🇯',
                'Denmark' : '🇩🇰', 'Dominica' : '🇩🇲', 'Dominican Republic' : '🇩🇴', 'Algeria' : '🇩🇿', 'Ceuta and Melilla' : '🇪🇦',
                'Ceuta' : '🇪🇦', 'Melilla' : '🇪🇦', 'Ecuador' : '🇪🇨', 'Estonia' : '🇪🇪', 'Egypt' : '🇪🇬', 'Western Sahara': '🇪🇭',
                'Sahara' : '🇪🇭', 'Eritrea' : '🇪🇷', 'Spain' : '🇪🇸', 'Ethiopia' : '🇪🇹', 'European Union' : '🇪🇺', 'EU' : '🇪🇺',
                'E.U.' : '🇪🇺', 'Finland' : '🇫🇮', 'Fiji' : '🇫🇯', 'Falkland Islands' : '🇫🇰', 'Micronesia' : '🇫🇲',
                'Faroe Islands' : '🇫🇴', 'France' : '🇫🇷', 'Gabon' : '🇬🇦', 'United Kingdom' : '🇬🇧', 'UK' : '🇬🇧', 'U.K.' : '🇬🇧',
                'Britian' : '🇬🇧', 'Grenada' : '🇬🇩', 'Georgia' : '🇬🇪', 'French Guiana' : '🇬🇫', 'Guiana' : '🇬🇫', 'Guernsey' : '🇬🇬',
                'Ghana' : '🇬🇭', 'Gibraltar' : '🇬🇮', 'Greenland' : '🇬🇱', 'Gambia' : '🇬🇲', 'Guinea' : '🇬🇳',
                'Guadeloupe' : '🇬🇵', 'Equatorial Guinea' : '🇬🇶', 'Greece' : '🇬🇷', 'South Georgia and South Sandwich Islands' : '🇬🇸',
                'South Georgia' : '🇬🇸', 'South Sandwich Islands' : '🇬🇸', 'Sandwich Islands' : '🇬🇸', 'Guatemala' : '🇬🇹',
                'Guam' : '🇬🇺', 'Guinea-Bissau' : '🇬🇼', 'Guinea Bissau' : '🇬🇼', 'Guyana' : '🇬🇾', 'Hong Kong SAR China' : '🇭🇰',
                'Hong Kong' : '🇭🇰', 'Heard and McDonald Islands' : '🇭🇲', 'Heard' : '🇭🇲', 'McDonald Islands' : '🇭🇲',
                'Honduras' : '🇭🇳', 'Croatia' : '🇭🇷', 'Haiti' : '🇭🇹', 'Hungary' : '🇭🇺', 'Best Country Ever' : '🇭🇺',
                'Canary Islands' : '🇮🇨', 'Indonesia' : '🇮🇩', 'Ireland' : '🇮🇪', 'Israel' : '🇮🇱', 'Worst "Country" Ever' : '🇮🇱',
                'Isle of Man' : '🇮🇲', 'India' : '🇮🇳', 'British India Ocean Territory' : '🇮🇴', 'Iraq' : '🇮🇶',
                'Iran' : '🇮🇷', 'Iceland' : '🇮🇸', 'Italy' : '🇮🇹', 'Jersey' : '🇯🇪', 'Jamaica' : '🇯🇲', 'Jordan' : '🇯🇴',
                'Japan' : '🇯🇵', 'Kenya' : '🇰🇪', 'Kyrgyzstan' : '🇰🇬', 'Cambodia' : '🇰🇭', 'Kiribati' : '🇰🇮',
                'Comoros' : '🇰🇲', 'St. Kitts and Nevis' : '🇰🇳', 'St. Kitts' : '🇰🇳', 'Saint Kitts' : '🇰🇳',
                'Nevis' : '🇰🇳', 'North Korea' : '🇰🇵', 'DPRK' : '🇰🇵', 'D.P.R.K.' : '🇰🇵', 'South Korea' : '🇰🇷',
                'SK' : '🇰🇷', 'S.K.' : '🇰🇷', 'Kuwait' : '🇰🇼', 'Cayman Islands' : '🇰🇾', 'Kazahkstan' : '🇰🇿', 
                'Laos' : '🇱🇦', 'Lebanon' : '🇱🇧', 'St. Lucia' : '🇱🇨', 'Saint Lucia' : '🇱🇨', 'Liechtenstein' : '🇱🇮',
                'Sri Lanka' : '🇱🇰', 'Liberia' : '🇱🇷', 'Lesotho' : '🇱🇸', 'Lithuania' : '🇱🇹', 'Luxembourg' : '🇱🇺',
                'Latvia' : '🇱🇻', 'Libya' : '🇱🇾', 'Morocco' : '🇲🇦', 'Monaco' : '🇲🇨', 'Moldova' : '🇲🇩', 
                'Montenegro' : '🇲🇪', 'St. Martin' : '🇲🇫', 'Saint Martin' : '🇲🇫', 'Madagascar' : '🇲🇬',
                'Marshall Islands' : '🇲🇭', 'North Macedonia' : '🇲🇰', 'Macedonia' : '🇲🇰', 'Mali' : '🇲🇱',
                'Myanmar' : '🇲🇲', 'Burma' : '🇲🇲', 'Mongolia' : '🇲🇳', 'Macao SAR China' : '🇲🇴', 'Macao' : '🇲🇴',
                'Northern Mariana Islands' : '🇲🇵', 'Martinique' : '🇲🇶', 'Mauritania' : '🇲🇷', 'Montserrat' : '🇲🇸',
                'Malta' : '🇲🇹', 'Mauritius' : '🇲🇺', 'Maldives' : '🇲🇻', 'Malawi' : '🇲🇼', 'Mexico' : '🇲🇽', 
                'Malaysia' : '🇲🇾', 'Mozambique' : '🇲🇿', 'Namibia' : '🇳🇦', 'New Caledonia' : '🇳🇨', 'Caledonia' : '🇳🇨',
                'Niger' : '👨🏿', 'Norfolk Island' : '🇳🇫', 'Nigeria' : '🇳🇬', 'Nicaragua' : '🇳🇮', 'Netherlands' : '🇳🇱',
                'Norway' : '🇳🇴', 'Nepal' : '🇳🇵', 'Nauru' : '🇳🇷', 'Niue' : '🇳🇺', 'New Zealand' : '🇳🇿', 'Oman' : '🇴🇲',
                'Panama' : '🇵🇦', 'Peru' : '🇵🇪', 'French Polynesia' : '🇵🇫', 'Polynesia' : '🇵🇫', 'Papua New Guinea' : '🇵🇬',
                'Philippines' : '🇵🇭', 'Pakistan' : '🇵🇰', 'Poland' : '🇵🇱', 'St. Pierre and Miquelon' : '🇵🇲', 
                'Saint Pierre' : '🇵🇲', 'Miquelon' : '🇵🇲', 'Pitcairn Islands' : '🇵🇳', 'Puerto Rico' : '🇵🇷',
                'Palestinian Territories' : '🇵🇸', 'Palestine' : '🇵🇸', 'Portugal' : '🇵🇹', 'Palau' : '🇵🇼', 
                'Paraguay' : '🇵🇾', 'Qatar' : '🇶🇦', 'Reunion' : '🇷🇪', 'Romania' : '🇷🇴', 'Serbia' : '🇷🇸',
                'Russia' : '🇷🇺', 'Rwanda' : '🇷🇼', 'Saudi Arabia' : '🇸🇦', 'Solomon Islands' : '🇸🇧', 
                'Seychelles' : '🇸🇨', 'Sudan' : '🇸🇩', 'Sweden' : '🇸🇪', 'Singapore' : '🇸🇬', 'St. Helena' : '🇸🇭',
                'Saint Helena' : '🇸🇭', 'Slovenia' : '🇸🇮', 'Slav-enia' : '🇸🇮', 'Svalbard and Jan Mayen' : '🇸🇯',
                'Svalbard' : '🇸🇯', 'Jan Mayen' : '🇸🇯', 'Slovakia' : '🇸🇰', 'Slav-akia' : '🇸🇰', 'Sierra Leone' : '🇸🇱',
                'San Marino' : '🇸🇲', 'Senegal' : '🇸🇳', 'Somalia' : '🇸🇴', 'Suriname' : '🇸🇷', 'South Sudan' : '🇸🇸',
                'Sao Tome and Principe' : '🇸🇹', 'Sao Tome' : '🇸🇹', 'Principe' : '🇸🇹', 'El Salvador' : '🇸🇻',
                'Sint Maarten' : '🇲🇫', 'Syria' : '🇸🇾', 'Eswatini' : '🇸🇿', 'Tristan Da Cunha' : '🇹🇦',
                'Turks and Caicos Islands' : '🇹🇨', 'Turks' : '🇹🇨', 'Caicos Islands' : '🇹🇨',
                'Chad' : '🇹🇩', 'French Southern Territories' : '🇹🇫', 'Togo' : '🇹🇬', 'Thailand' : '🇹🇭',
                'Tajikstan' : '🇹🇯', 'Tokelau' : '🇹🇰', 'Timor-Leste' : '🇹🇱', 'Turkmenistan' : '🇹🇲',
                'Tunisia' : '🇹🇳', 'Tonga' : '🇹🇴', 'Turkey' : '🇹🇷', 'Trinidad and Tobago' : '🇹🇹',
                'Trinidad' : '🇹🇹', 'Tabago' : '🇹🇹', 'Tuvalu' : '🇹🇻', 'Taiwan' : '🇹🇼', 'Tanzania' : '🇹🇿',
                'Ukraine' : '🇺🇦', 'Uganda' : '🇺🇬', 'US Outlying Islands' : '🇺🇲', 'U.S. Outlying Islands' : '🇺🇲',
                'United Nations' : '🇺🇳', 'UN' : '🇺🇳', 'U.N.' : '🇺🇳', 'United States of America' : '🇺🇸',
                'United States' : '🇺🇸', 'USA' : '🇺🇸', 'US' : '🇺🇸', 'U.S.A.' : '🇺🇸', 'U.S.' : '🇺🇸', 'America' : '🇺🇸',
                'Uruguay' : '🇺🇾', 'Uzbekistan' : '🇺🇿', 'Vatican City' : '🇻🇦', 'Vatican' : '🇻🇦', 
                'St. Vincent and Grenadines' : '🇻🇨', 'St. Vincent' : '🇻🇨', 'Saint Vincent' : '🇻🇨',
                'Grenadines' : '🇻🇨', 'Venezuela' : '🇻🇪', 'British Virgin Islands' : '🇻🇬',
                'US Virgin Islands' : '🇻🇮', 'U.S. Virgin Islands' : '🇻🇮', 'Vietnam' : '🇻🇳',
                'Vanuatu' : '🇻🇺', 'Wallis and Futuna' : '🇼🇫', 'Wallace and Futaba' : '🇼🇫',
                'Wallis' : '🇼🇫', 'Futuna' : '🇼🇫', 'Samoa' : '🇼🇸', 'Kosovo' : '🇽🇰', 'Yemen' : '🇾🇪',
                'Mayotte' : '🇾🇹', 'South Africa' : '🇿🇦', 'SA' : '🇿🇦', 'S.A.' : '🇿🇦', 'Zambia' : '🇿🇲',
                'Zimbabwe' : '🇿🇼', 'England' : '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'Scotland' : '🏴󠁧󠁢󠁳󠁣󠁴󠁿', 'Wales' : '🏴󠁧󠁢󠁷󠁬󠁳󠁿', 'Texas' : '🏴󠁵󠁳󠁴󠁸󠁿'
                }
helpMessages = {'HELP' : 'Aliases: H\nViews the main menu, so to speak; the starting point for all the other commands.',
                'ADMINHELP' : 'Aliases: AHelp, Admin\nViews some of the more nuanced commands that administrators may use.',
                'COUNTRYMENU' : "Aliases: Countries\nViews country-specific commands.\n'Country' just means 'the value associated with the reaction, title, role, and channel.'",
                'REACTIONMENU' : "Aliases: Reactions\nViews reaction-specific commands.\n'Reaction' just means 'the emoji that uniquely represents a country and is used as a button.'",
                'TITLEMENU' : "Aliases: \nViews role-specific commands.\n'Title' just means 'the name used for the ruler of a country, instead of using that country's name.'",
                'SETUP' : "Aliases: FirstTime\nRuns a small guide intended to help users quickly add countries to an otherwise empty list. Self-explanatory once you get it going.",
                'RESET' : "Aliases: Clear\nExecutes a dramatic last resort that clears all information. Country, reaction, title and channel information is erased. Options go back to the defaults.",
                'CLAIMS' : "Aliases: Claim, CountryClaims\nDisplays which countries are taken and free, and allows for players to claim (or unclaim) their own, depending on permissions granted.",
                'COUNTRYLIST' : "Aliases: List\nDisplays all countries, ten per page. This will also display the associated reaction for them, where '🏳️' represents having no reaction.",
                'COUNTRYMAKER' : "Aliases: NewCountry, New, AddCountry\nRuns a prompt relay designed to rapidly add new countries. If the country appears as written in the UNICODE documentation for emoji flags, the reaction is automatically assigned.",
                'REMOVECOUNTRY' : "Aliases: Remove, RemoveCountries\nRuns a prompt relay designed to rapidly remove countries. This will also remove the role and channel, depending on your preferences.",
                'RENAMECOUNTRY' : "Aliases: Rename, RenameCountries\nRuns a prompt relay designed to rapidly add new countries. This will rename the channel.",
                'REMOVEREACTION' : "Aliases: RemoveReactions\nRemoves the associated reaction for a country and replaces it with a '🏳️' emoji. Countries without a flag *can't* be used in Lss!claims.",
                'UPDATEREACTIONS' : "Aliases: UpdateReaction\nRuns a prompt relay designed to rapidly add or edit country's reactions.",
                'ASSIGNREACTIONS' : "Aliases: AssignReaction\nRuns a prompt relay designed to rapidly add reactions to countries without one already.",
                'TITLELIST' : "Aliases: Titles\nDisplays all countries with a title, and shows you their associated title name, ten per page.",
                'RETITLE' : "Aliases: Title\nRuns a prompt relay designed to rapidly add or edit country's title.",
                'REMOVETITLE' : "Aliases: RemoveTitles\nRuns a prompt relay designed to rapidly remove titles. This will also rename the role to be the same as the country name, as per standard.",
                'SERVERS' : "Aliases: ServerCount\nTells you how many servers this bot is running on. Just, you know, if you were curious.",
                'OPTIONS' : "Aliases: Settings\nAllows you to tailor the bot's behavior to your taste.",
                'COMMANDS' : "Aliases: CommandList, CommandsList\nDisplays every single command.",
                'DIPLO' : "Aliases: Diplomacy\nCreates a private channel where only the roles specified may see or speak in it."
                }


##Setup
print ("Allow me a moment to wake up...")
client.remove_command("help")


##Events
@client.event
async def on_ready():
    print(f'{client.user} is alive!')
    await client.change_presence(activity=discord.Game(name='Lss!help for help.'))
    for i in client.guilds:
        await addServerVars(i)

@client.event
async def on_guild_join(guild):
    await addServerVars(guild)
    pass

@client.event
async def on_guild_remove(guild):
    if os.path.exists('serverData/'+ str(guild.id) + '.txt'):
        os.remove('serverData/'+ str(guild.id) + '.txt')
    else:
        return

@client.event
async def on_member_remove(member):

    guild = member.guild
    data = await readServerInfo(member.guild.id)

    if str(member.id) in data['players'].keys():
        countryName = data['players'][str(member.id)]
        del data['players'][str(member.id)]
        await writeServerInfo(guild.id, data)
        if  data['options']['countryChannelDeletion'] == 'unclaiming.':
            await removeChannel(guild,countryName)

@client.event
async def on_raw_reaction_add(pl):

    if pl.user_id == client.user.id:
        return

    reaction = str(pl.emoji)
    channel = client.get_channel(pl.channel_id)
    message = await channel.fetch_message(pl.message_id)
    embed = message.embeds[0]
    guild = client.get_guild(pl.guild_id)
    user = pl.member

    await message.remove_reaction(reaction,user)
       
    if type(embed) == discord.embeds.Embed :
             
        if embed.title == 'Country Claims':

            bottoms = embed.footer.text.split(', ')
            data = await readServerInfo(guild.id)

            #Close Claims
            if reaction == '❌':
                await message.delete()
                return
            if reaction == '➡️':
                await message.delete()
                if len(data['countries']) == (int(bottoms[0]) + int(bottoms[2]) + int(bottoms[1]) + int(bottoms[3])):
                    await claimsFunc(channel,0,0)
                else:
                    await claimsFunc(channel,int(bottoms[0])+int(bottoms[2]),int(bottoms[1])+int(bottoms[3]))
                return

            #Get country name from reaction
            for key, value in data['countries'].items():
                if value == reaction:
                    countryName = key
                    break

            #Get role name/ title name using country name
            if countryName in  data['titles'].keys():
                roleName =  data['titles'][countryName]
            else:
                roleName = countryName

            #Get role object from role/title name
            try:
                clickedRole = next(filter(lambda x: x.name == roleName, guild.roles))
            except:
                return
    
            #Check if user has any country role
            hasCountryRole = user.id in data['players'].keys()


            if countryName in data['players'].values():
                #Country has a leader

                if data['players'][str(user.id)] == countryName:
                    #User is the leader.

                    if data['options']['playerUnclaim'] == 'by clicking on their own flag in Lss!claims.' or user.permissions_in(channel).administrator == True:
                        #This leader may step down voluntarily.

                        await user.remove_roles(clickedRole)
                        del data['players'][str(pl.member.id)]
                        await writeServerInfo(guild.id, data)
                        steppedDown = await channel.send("You've voluntarily stepped down from your position of power, " + user.name + '.')
                        await asyncio.sleep(5)
                        await message.edit(embed = (await claimsEmbed(channel,int(bottoms[0]),int(bottoms[1])))[0])
                        await steppedDown.delete()
                        if  data['options']['countryChannelDeletion'] == 'unclaiming.':
                            await removeChannel(guild,countryName)
                        else:
                            pass
                        return

                    else:
                        #This leader may not step down voluntarily.

                        unable = await channel.send("Only an admin may unclaim your nation for you, " + user.name + '.')
                        await asyncio.sleep(5)
                        await message.edit(embed = (await claimsEmbed(channel,int(bottoms[0]),int(bottoms[1])))[0])
                        await unable.delete()
                        return
                else:
                    #User is not the leader.

                    if user.permissions_in(channel).administrator == True:
                        #User is an admin.

                        for i in clickedRole.members:
                            await i.remove_roles(clickedRole)
                            data['players'].remove[str(i.id)]
                        await writeServerInfo(guild.id, data)

                        removed = await channel.send("Forcefully abdicated " + countryName + "'s ruler.")
                        await asyncio.sleep(5)
                        await message.edit(embed = (await claimsEmbed(channel,int(bottoms[0]),int(bottoms[1])))[0])
                        await removed.delete()
                        if data['options']['countryChannelDeletion'] == 'unclaiming.':
                            await removeChannel(guild,countryName)
                    else:
                        #User is not an admin.
                        
                        unable = await channel.send("Only admins can force a player to step down from their country's leaderships position, " + user.name + '.')
                        await asyncio.sleep(5)
                        await message.edit(embed = (await claimsEmbed(channel,int(bottoms[0]),int(bottoms[1])))[0])
                        await unable.delete()
                        return
            else:
                #Country is empty

                if str(pl.member.id) in data['players']:
                    #Player has a different country already.

                    unable = await channel.send("You cannot lead two separate nations, " + user.name + '.')
                    await asyncio.sleep(5)
                    await message.edit(embed = (await claimsEmbed(channel,int(bottoms[0]),int(bottoms[1])))[0])
                    await unable.delete()
                    return

                else:
                    #Good match! Claim the country.

                    await user.add_roles(clickedRole)
                    reign = await channel.send("May your reign be prosperous, " + user.name + '.')
                    data['players'].update({str(pl.member.id): countryName})
                    await writeServerInfo(guild.id, data)
                    await asyncio.sleep(5)
                    await message.edit(embed = (await claimsEmbed(channel,int(bottoms[0]),int(bottoms[1])))[0])
                    await reign.delete()
                    if data['options']['countryChannelCreation'] == 'claiming.':
                        await createChannel(guild,countryName,clickedRole)
            return


##Commands
@client.command(aliases=['servercount'])
async def servers(ctx):
    await ctx.message.delete()
    message = await ctx.send('Currently running on ' + str(len(client.guilds)) + ' servers.')
    await asyncio.sleep(10)
    await message.delete()

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

@client.command(aliases=['ahelp','admin'])
async def adminHelp(ctx):
    await ctx.message.delete()
    await adminHelpFunc(ctx.channel,ctx.author)

@client.command(aliases=['firsttime'])
async def setup(ctx):
    await ctx.message.delete()
    await setupFunc(ctx.channel,ctx.author)

@client.command(aliases=['newcountry','new','addcountry'])
async def countryMaker(ctx):
    await ctx.message.delete()
    await countryMakerFunc(ctx.channel,ctx.author,None,False,False)

@client.command(aliases=['countries'])
async def countryMenu(ctx):
    await ctx.message.delete()
    await countryMenuFunc(ctx.channel,ctx.author) 

@client.command(aliases=['list'])
async def countryList(ctx):
    await ctx.message.delete()   
    await countryListFunc(ctx.channel,ctx.author,countryMenuFunc,1)
    
@client.command(aliases=['renamecountries','rename'])
async def renameCountry(ctx):
    await ctx.message.delete()   
    await renameCountryFunc(ctx.channel,ctx.author,False)

@client.command(aliases=['removecountries','remove'])
async def removeCountry(ctx):
    await ctx.message.delete()   
    await removeCountryFunc(ctx.channel,ctx.author,False)

@client.command(aliases=['reactions'])
async def reactionMenu(ctx):
    await ctx.message.delete()
    await reactionMenuFunc(ctx.channel,ctx.author)
    
@client.command(aliases=['removereactions'])
async def removeReaction(ctx):
    await ctx.message.delete()   
    await removeReactionFunc(ctx.channel,ctx.author,False)

@client.command(aliases=['updatereaction'])
async def updateReactions(ctx):
    await ctx.message.delete()   
    await updateReactionFunc(ctx.channel,ctx.author,False)

@client.command(aliases=['assignreaction'])
async def assignReactions(ctx):
    await ctx.message.delete()   
    await assignReactionsFunc(ctx.channel,ctx.author,False,False)

@client.command(aliases=['titlesmenu'])
async def titleMenu(ctx):
    await ctx.message.delete()   
    await titleMenuFunc(ctx.channel,ctx.author)

@client.command(aliases=['titles'])
async def titleList(ctx):
    await ctx.message.delete()   
    await titleListFunc(ctx.channel,ctx.author,1) 

@client.command(aliases=['title'])
async def retitle(ctx):
    await ctx.message.delete()   
    await retitleFunc(ctx.channel,ctx.author,'',False) 

@client.command(aliases=['removetitles'])
async def removeTitle(ctx):
    await ctx.message.delete()   
    await removeTitleFunc(ctx.channel,ctx.author,False) 

@client.command(aliasese=['clear'])
async def reset(ctx):
    await ctx.message.delete()   
    await resetFunc(ctx.channel,ctx.author) 

@client.command(aliases=['claim','countryclaims'])
async def claims(ctx):
    await ctx.message.delete()   
    await claimsFunc(ctx.channel,0,0) 

@client.command(aliases=['settings'])
async def options(ctx):
    await ctx.message.delete()   
    await optionsFunc(ctx.channel,ctx.author) 

@client.command(aliases=['commandlist','commandslist'])
async def commands(ctx):
    await ctx.message.delete()   
    await commandsFunc(ctx.channel,ctx.author) 

@client.command(aliases=['diplomacy'])
async def diplo(ctx):    
    await ctx.message.delete()
    await diploFunc(ctx.channel,ctx.author,ctx.message)

## Functions

#Used Internally
async def diploFunc(channel,user,message):
    
    if await checkPerm(channel,user) == False:
        return
    
    data = await readServerInfo(channel.guild.id)
    words = list(x.lower() for x in message.content.split(' '))

    if len(words) == 1:
        await promptFunc(channel,user,('Diplomacy Creation'),'You gotta tell me what countries you want to be involved!\nProper usage example: Lss!diplo Russia Germany America','This message will delete itself in 30 seconds.','❌')
        return
    
    else:

        foundRoleNames = []
        unfoundRoles = []
        foundRoleObjects = []

        for i in range(1,len(words)):
             #Get role names/ title names using country name
            if words[i] in list(x.lower() for x in data['titles'].keys()):           
                foundRoleNames.append(data['titles'][words[i]])
            if words[i] in list(x.lower() for x in data['countries']):                
                foundRoleNames.append(words[i])
            else:
                unfoundRoles.append(words[i])

        for i in foundRoleNames:
            #Find roles for leader roles (countries or titles)
            try:
                foundRoleObjects.append(next(filter(lambda x: x.name.lower() == i, channel.guild.roles)))
                print('Found role object for: ' + i)
            except:
                foundRoleNames.pop(i)
                unfoundRoles.append(i)
    
        if foundRoleObjects:
                
            try:
                diploCategory = next(filter(lambda x: x.name == 'Diplomacy', channel.guild.categories))
                #Diplomacy Category is made
                pass
            except:
                #Make one
                overwrites = {
                
                channel.guild.me: discord.PermissionOverwrite(read_messages=True),
                channel.guild.default_role: discord.PermissionOverwrite(read_messages=False)
                }    
                diploCategory = await channel.guild.create_category(name='Diplomacy',overwrites=overwrites)
            
            #Find name
            chatName = words[1]
            for i in range(2,len(words)):
                chatName += ' ' + words[i]

            diploChannel = await channel.guild.create_text_channel(name=chatName,category=diploCategory,type=discord.ChannelType.text)
            overwrites = {channel.guild.me: discord.PermissionOverwrite(read_messages=True),
            channel.guild.default_role: discord.PermissionOverwrite(read_messages=False)
            }

            for i in foundRoleObjects: 
                #Allow found roles to read the chat
                overwrites.update({i : discord.PermissionOverwrite(read_messages=True)})
            
            await diploChannel.edit(overwrites=overwrites)
            

            verdict = 'Successfully made ' + diploChannel.mention + '!\n'

        else:
            verdict = "Couldn't make the chat.\n"



    successPortion = ''
    failurePortion = ''

    if foundRoleObjects:
        successPortion = 'Successfully added ' + foundRoleNames[0]
        for i in range(1,len(foundRoleNames)):
            successPortion += ', ' + foundRoleNames[i]
        successPortion += '! '
    
    if unfoundRoles:
        failurePortion = 'Failed to find roles for '+ unfoundRoles[0]
        for i in range(1,len(unfoundRoles)):
            failurePortion += ', ' + unfoundRoles[i]
        failurePortion += ".\nDouble check that you didn't make typos, and that you spelled every country name exactly as it appears in Lss!countrylist."

    await promptFunc(channel,user,'Diplomacy Creation',(verdict + successPortion + failurePortion),('This message will delete itself in 30 seconds.'),'❌')
        
async def listenReactFunc(channel,userID,timeoutTime):
    try:
        return await client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == userID and payload.channel_id == channel.id, timeout=timeoutTime)
    except asyncio.TimeoutError:
        return

async def promptFunc(channel,user,title,description,footer,*reactions):

    embed = discord.Embed(
    title = title,
    description = description,
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = footer)
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    for reaction in reactions:
        try:
            await finalembed.add_reaction(reaction)
        except:
            return

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,user.id,30)
    if rawReaction:
        reaction = str(rawReaction.emoji)

    #Act based on reaction
    if rawReaction != None:
        await finalembed.delete()
        return reaction
    else:
        await finalembed.delete()
        exiting = await channel.send("No reaction recieved in the last 30 seconds. Closing...")
        await asyncio.sleep(5)
        await exiting.delete()

async def checkPerm(channel,user):
    if user.permissions_in(channel).administrator == False:
        noPerm = await channel.send('Sorry, but you need to be an administrator to do that, ' + user.name + '.')
        await asyncio.sleep(3)
        await noPerm.delete()
        return False
    else:
        return True

async def createChannel(guild,countryName,countryRole):
    
    channelNames = list(i.name for i in guild.channels)
    if countryName.lower() in channelNames:
        return

    for i in guild.categories:
        if i.name == 'Countries':
            countryCat = i
            overwrites = {
            countryRole: discord.PermissionOverwrite(read_messages=True),
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
            }    

            try:
                channel = await guild.create_text_channel(name=countryName,category=countryCat,type=discord.ChannelType.text,overwrites=overwrites)
            finally:
                return
    

    overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    guild.me: discord.PermissionOverwrite(read_messages=True)
    }
    try:
        countryCat = await guild.create_category(name='Countries',overwrites=overwrites)
    except:
        pass

    overwrites = {
        countryRole: discord.PermissionOverwrite(read_messages=True),
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }    
    try:
        channel = await guild.create_text_channel(name=countryName,category=countryCat,type=discord.ChannelType.text)
        await channel.edit(sync_permissions=True,overwrites=overwrites)
    except:
        pass

async def removeChannel(guild,countryName):
    for i in guild.channels:
        if i.name == (countryName).lower():
            await i.delete()

async def addServerVars(guild):

    id = guild.id

    if path.exists('serverData/'+ str(id) + '.txt'):
        return

    else:
        now = datetime.now()
        data = {}

        data['serverDetails'] = {
            'Name' : str(guild.name),
            'ID' : str(id),
            'Entry Submission DTG' : now.strftime("%m/%d/%Y, %H:%M:%S")
        }
        data['titles'] = {}
        data['countries'] = {}
        data['players'] = {}
        data['options'] = {
            'countryChannelCreation' : 'creation.',
            'countryChannelDeletion' : 'deletion.',
            'playerUnclaim' : 'by having an Admin click their flag in Lss!claims.'
        }

        file = open('serverData/'+ str(id) + '.txt', 'w')
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.close()
        print('Made data for server name ' + str(guild.name) + '.')
        return

async def readServerInfo(id):

    file = open('serverData/'+ str(id) + '.txt', 'r+', encoding="utf-8")
    data = json.load(file)
    file.close()

    return data

async def writeServerInfo(id, data):

    json_file = open('serverData/'+ str(id) + '.txt', 'w', encoding="utf-8")
    json_file.seek(0)
    json.dump(data, json_file, ensure_ascii=False, indent=4)
    json_file.close()

    return

#Main Menus
async def helpFunc(channel,user):

    data = await readServerInfo(channel.guild.id)

    embed = discord.Embed(
    title = ('Help Menu for ' + str(user).split('#')[0]),
    description = 'Call with the full Lss!(command), or just click a reaction.',
    color = discord.Color(000000)
    ) 
    
    if len(data['countries']) == 0:
        embed.add_field(name = ':arrow_forward:  Setup', value = 'Performs the first-time setup with you.')
        claimsPresent = False
    else:
        embed.add_field(name = ':man_raising_hand:  Claims', value = 'Opens up the signature country claiming prompt.')
        claimsPresent = True
    embed.add_field(name = ':earth_americas:  CountryMenu', value = 'Add, edit, or remove the countries.*')
    embed.add_field(name = ':speech_left:  ReactionMenu', value = 'Edit the reaction buttons for each country.*')
    embed.add_field(name = ':prince:  TitleMenu', value = "Change the country's ruler titles.*")
    embed.add_field(name = ':question:  AdminHelp', value = 'Calls up a cool menu just for admins.')
    embed.add_field(name = "Get your own bot?", value = "[Sure.](https://top.gg/bot/727015243246600193)")
    embed.set_footer(text = '*More in-depth than the Setup version.')
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        if claimsPresent:
            await finalembed.add_reaction('🙋‍♂️')
        else:
            await finalembed.add_reaction('➡️')
        await finalembed.add_reaction('🌎')
        await finalembed.add_reaction('🗨️')
        await finalembed.add_reaction('🤴')
        await finalembed.add_reaction('❓')
        await finalembed.add_reaction('❌')
    except:
        return

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,user.id,60)
    if rawReaction:
        reaction = str(rawReaction.emoji)

    #Act based on reaction
    if rawReaction != None:
        if reaction == '➡️':
            await finalembed.delete()
            await setupFunc(channel,user)
        if reaction == '🙋‍♂️' and claimsPresent:
            await finalembed.delete()
            await claimsFunc(channel,0,0)
        if reaction == '🌎':
            await finalembed.delete()
            await countryMenuFunc(channel,user)
        if reaction == '🗨️':
            await finalembed.delete()
            await reactionMenuFunc(channel,user)
        if reaction == '🤴':
            await finalembed.delete()
            await titleMenuFunc(channel,user)
        if reaction == '❓' :
            await finalembed.delete()
            await adminHelpFunc(channel,user)
        else:
            await finalembed.delete()
    else:
        await finalembed.delete()
        exiting = await channel.send("No reaction recieved in the last minute. Closing...")
        await asyncio.sleep(5)
        await exiting.delete()
        return

async def adminHelpFunc(channel,user):
    
    if await checkPerm(channel,user) == False:
        return

    embed = discord.Embed(
    title = ('Admin Help Menu for ' + str(user).split('#')[0]),
    description = 'Call with the full Lss!(command), or just click a reaction.',
    color = discord.Color(000000)
    ) 
    
    embed.add_field(name = ':united_nations:  CountryList', value = "View all countries and their info.")
    embed.add_field(name = ':notebook_with_decorative_cover:  Commands', value = 'A full list of *every* command.')
    embed.add_field(name = ':wrench:  Options', value = 'Opens the options menu.')
    embed.add_field(name = ':wastebasket:  Reset', value = 'Clears all Lss info and Diplomacy chats.')
    embed.add_field(name = ':grey_question:  Help', value = 'Brings you back to the general help menu.')
    embed.add_field(name = "Get your own bot?", value = "[Sure.](https://top.gg/bot/727015243246600193)")
    finalembed = await channel.send(embed=embed)
    
    try:
        await finalembed.add_reaction('🇺🇳')
        await finalembed.add_reaction('📔')
        await finalembed.add_reaction('🔧')
        await finalembed.add_reaction('🗑️')
        await finalembed.add_reaction('❔')
        await finalembed.add_reaction('❌')
    except:
        return

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,user.id,60)
    if rawReaction:
        reaction = str(rawReaction.emoji)

    #Act based on reaction
    if rawReaction != None:
        if reaction == '🇺🇳':
            await finalembed.delete()
            await countryListFunc(channel,user,adminHelpFunc,1)
        if reaction == '📔':
            await finalembed.delete()
            await commandsFunc(channel,user)
        if reaction == '🔧':             
            await finalembed.delete()
            await optionsFunc(channel,user)
        if reaction == '🗑️':
            await finalembed.delete()
            await resetFunc(channel,user)
        if reaction == '❔': 
            await finalembed.delete()
            await helpFunc(channel,user)
        else:
            await finalembed.delete()
    else:
        await finalembed.delete()
        exiting = await channel.send("No reaction recieved in the last minute. Closing...")
        await asyncio.sleep(5)
        await exiting.delete()
        return

async def countryMenuFunc(channel,user):
    embed = discord.Embed(
    title = ('Country Menu for ' + str(user).split('#')[0]),
    description = 'Call with the full Lss!(command), or just click a reaction.',
    color = discord.Color(000000)
    ) 
    
    embed.add_field(name = ':united_nations:  CountryList', value = 'View a complete list of every country and its reaction.')
    embed.add_field(name = ':put_litter_in_its_place:  RemoveCountry', value = 'Remove a country.')
    embed.add_field(name = ':writing_hand:  RenameCountry', value = "Change a country's name.")
    embed.add_field(name = ':arrow_forward:  CountryMaker', value = "Go to the country-making prompt.")
    embed.add_field(name = ':grey_question:  Help', value = "Brings you to the general help menu.")
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('🇺🇳')
        await finalembed.add_reaction('🚮')
        await finalembed.add_reaction('✍️')
        await finalembed.add_reaction('▶️')
        await finalembed.add_reaction('❔')
        await finalembed.add_reaction('❌')
    except:
        return

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,user.id,60)
    if rawReaction:
        reaction = str(rawReaction.emoji)

    #Act based on reaction
    if rawReaction != None:
        if reaction == '🇺🇳':
            await finalembed.delete()
            await countryListFunc(channel,user,countryMenuFunc,1)
        if reaction == '🚮':
            await finalembed.delete()
            await removeCountryFunc(channel,user,False)
        if reaction == '✍️':
            await finalembed.delete()
            await renameCountryFunc(channel,user,False)
        if reaction == '▶️':
            await finalembed.delete()
            await countryMakerFunc(channel,user,None,False,False)
        if reaction == '❔' :
            await finalembed.delete()
            await helpFunc(channel,user)
        else:
            await finalembed.delete()
    else:
        await finalembed.delete()
        exiting = await channel.send("No reaction recieved in the last minute. Closing...")
        await asyncio.sleep(5)
        await exiting.delete()
        return
    
async def reactionMenuFunc(channel,user):

    data = await readServerInfo(channel.guild.id)

    unnamedCount = 0
    for key, value in data['countries'].items():
        if value == '🏳️':
            unnamedCount += 1
    if unnamedCount == 1:
        unnamed = 'ATTENTION: You have a country without a corresponding reaction assigned to it!\n'
    elif unnamedCount > 1:
        unnamed = 'ATTENTION: You have ' + str(unnamedCount) + ' countries without a corresponding reaction assigned to them!\n'
    else:
        unnamed = ''

    embed = discord.Embed(
    title = ('Reaction Menu for ' + str(user).split('#')[0]),
    description = unnamed + 'Call with the full Lss!(command), or just click a reaction.',
    color = discord.Color(000000)
    ) 
    
    embed.add_field(name = ':united_nations:  CountryList', value = 'View a complete list of every country and its reaction.')
    embed.add_field(name = ':put_litter_in_its_place:  RemoveReaction', value = "Remove a country's reaction.*")
    embed.add_field(name = ':writing_hand:  UpdateReaction', value = "Change a country's reaction.")
    embed.add_field(name = ':arrow_forward:  AssignReaction', value = "Go to the reaction-assigning prompt.")
    embed.add_field(name = ':grey_question:  Help', value = "Brings you to the general help menu..")
    embed.set_footer(text = "*Countries without unique reactions won't be available in Lss!claims.")
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('🇺🇳')
        await finalembed.add_reaction('🚮')
        await finalembed.add_reaction('✍️')
        await finalembed.add_reaction('▶️')
        await finalembed.add_reaction('❔')
        await finalembed.add_reaction('❌')
    except:
        return

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,user.id,60)
    if rawReaction:
        reaction = str(rawReaction.emoji)

    #Act based on reaction
    if rawReaction != None:
        if reaction == '🇺🇳':
            await finalembed.delete()
            await countryListFunc(channel,user,reactionMenuFunc,1)
        if reaction == '🚮':
            await finalembed.delete()
            await removeReactionFunc(channel,user,False)
        if reaction == '✍️':
            await finalembed.delete()
            await updateReactionFunc(channel,user,False)
        if reaction == '▶️':
            await finalembed.delete()
            await assignReactionsFunc(channel,user,False,False)
        if reaction == '❔' :
            await finalembed.delete()
            await helpFunc(channel,user)
        else:
            await finalembed.delete()
    else:
        await finalembed.delete()
        exiting = await channel.send("No reaction recieved in the last minute. Closing...")
        await asyncio.sleep(5)
        await exiting.delete()
        return

async def titleMenuFunc(channel,user):
    embed = discord.Embed(
    title = ('Title Menu for ' + str(user).split('#')[0]),
    description = 'Call with the full Lss!(command), or just click a reaction.',
    color = discord.Color(000000)
    ) 
    
    embed.add_field(name = ':crown:  TitleList', value = 'View all special titles.')
    embed.add_field(name = ':put_litter_in_its_place:  RemoveTitle', value = "Remove a country's title.")
    embed.add_field(name = ':writing_hand:  Retitle', value = "Add or change a country's title.")
    embed.add_field(name = ':grey_question:  Help', value = "Brings you to the general help menu.")
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('👑')
        await finalembed.add_reaction('🚮')
        await finalembed.add_reaction('✍️')
        await finalembed.add_reaction('❔')
        await finalembed.add_reaction('❌')
    except:
        return

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,user.id,60)
    if rawReaction:
        reaction = str(rawReaction.emoji)

    #Act based on reaction
    if rawReaction != None:
        if reaction == '👑':
            await finalembed.delete()
            await titleListFunc(channel,user,1)
        if reaction == '🚮':
            await finalembed.delete()
            await removeTitleFunc(channel,user,False)
        if reaction == '✍️':
            await finalembed.delete()
            await retitleFunc(channel,user,'',False)
        if reaction == '❔' :
            await finalembed.delete()
            await helpFunc(channel,user)
        else:
            await finalembed.delete()
    else:
        await finalembed.delete()
        exiting = await channel.send("No reaction recieved in the last minute. Closing...")
        await asyncio.sleep(5)
        await exiting.delete()
        return

#Help Commands
async def setupFunc(channel,user):

    if await checkPerm(channel,user) == False:
        return

    data = await readServerInfo(channel.guild.id)

    #First Message
    reaction = await promptFunc(channel,user,('Setup for ' + str(user).split('#')[0]),('Hello! This section will perform the first-time setup for the ' + str(channel.guild)
                    + ' server.'),('To continue, react with the green checkmark within 30 seconds.'),'✅','❌')
    if reaction == '✅':
        pass
    else:
        return

    #Second Message
    reaction = await promptFunc(channel,user,'Heads up.', ("This setup was designed to be quick, so Lss!prefixes aren't used. "
                                             "It'll listen to everything you say until you leave or close it, so try not to be " 
                                             "distracted by anyone--go in a private channel if you have to."),('To continue, '
                                             'react with the green checkmark within 30 seconds.'),'✅','❌')
    if reaction == '✅':
        pass
    else:
        return

    await setupCountries(channel,user)

    data = await readServerInfo(channel.guild.id)

    unreactedCountries = 0
    for value in data['countries'].values():
        if value == '🏳️':
            unreactedCountries += 1

    if unreactedCountries == 0:
        reaction = await promptFunc(channel,user,'What luck!', "Every country you've added just now has a reaction flag (emoji) auto"
                                             "matically assigned to it by the bot. That means we can skip this next step.",
                                             ('To continue, react with the green checkmark within 30 seconds.'),'✅','❌')
        if reaction == '✅':
            pass
        else:
            return
    else:
        reaction = await promptFunc(channel,user,'Hmm.', "You'll need to go through and assign reactions to any countries without "
                                             "them already, which we'll do in this next step. (Most mainstream countries have this done automatically).",
                                             ('To continue, react with the green checkmark within 30 seconds.'),'✅','❌')
        if reaction == '✅':
            pass
        else:
            return

        await setupReactions(channel,user)

    reaction = await promptFunc(channel,user,'Country Titles', "In the future, you can go through and add special titles for a country's ruler. "
                                             "This is if you want the person who chooses USA to have the title of, say, 'President'.",
                                             ('To continue, react with the green checkmark within 30 seconds.'),'✅','❌')
    if reaction == '✅':
        pass
    else:
        return

    reaction = await promptFunc(channel,user,'All done!', "If you go back to the Lss!help menu, you'll see there's a new option called "
                                             "Lss!claims. You can come back here anytime, but feel free to try out that new feature!",
                                             ("To exit, react with anything within 30 seconds, or don't."),'❔','❌')
    if reaction == '❔':
        await helpFunc(channel,user)
    else:
        return

async def setupCountries(channel,user):
    
    if await checkPerm(channel,user) == False:
        return

    await countryMakerFunc(channel,user, None,False,True)
    reaction = await promptFunc(channel,user,'Add another country?',"If you'd like to, just press the green arrow. "
                                              "If not, then exit out here and the setup will progress.",'To continue, '
                                              'say anything or react with the green checkmark within 30 seconds.','✅','❌')
    if reaction == '✅':
        await setupCountries(channel,user)
    else:
        return

async def setupReactions(channel,user):

    if await checkPerm(channel,user) == False:
        return

    await assignReactionsFunc(channel,user,False,True)
    
    data = await readServerInfo(channel.guild.id)

    unreactedCountries = 0
    for value in data['countries'].values():
        if value == '🏳️':
            unreactedCountries += 1

    if unreactedCountries == 0:
        reaction = await promptFunc(channel,user,'All good here!',"Alright, every country now has their own reaction assigned.",'To continue, '
                                                'react with the green checkmark within 30 seconds.','✅','❌')
        return
    else:
        reaction = await promptFunc(channel,user,'Add another reaction?',"You still have more to assign. Know that any countries without a reaction assigned "
                                                "to them won't show on Lss!claims.",'To continue, '
                                                'react with the green checkmark within 30 seconds.','✅','❌')
        if reaction == '✅':
            await setupReactions(channel,user)
        else:
            return

async def claimsEmbed(channel,bottomFree,bottomTaken):

    data = await readServerInfo(channel.guild.id)

    #Define Variables
    freeCountries = []
    takenCountries = []
    unassignedCountries = 0
    allCountries = data['countries']
    allCountryKeys = data['countries'].keys()
    allTitles = data['titles']
    allRoleNames = (i.name for i in channel.guild.roles)
    allRoles = list(channel.guild.roles)
    allRelevantRoles = {}
    displayedFree = ''
    displayedTaken = ''
    newFreeBottom = 0
    newTakenBottom = 0

    #Sort free vs. taken
    for i in data['countries'].keys():
        if i in data['players'].values():
            takenCountries.append(i)
        else:
            freeCountries.append(i)
    
    #Get displayed countries
    totalRemaining = len(freeCountries[bottomFree:]) + len(takenCountries[bottomTaken:])
    if len(freeCountries[bottomFree:]) >= len(takenCountries[bottomTaken:]):
        smaller = takenCountries[bottomTaken:]
        smallerOne = 'Taken'
        bigger = freeCountries[bottomFree:]
    else: 
        smaller = freeCountries[bottomFree:]
        smallerOne = 'Free'
        bigger = takenCountries[bottomTaken:]
    
    #Trim initially bigger list down to size
    trimming = totalRemaining - 18
    if trimming <= 0:
        pass
    else:
        if smallerOne == 'Taken':
            trim = (len(freeCountries[bottomFree:]) - trimming)
        else:
            trim = (len(takenCountries[bottomTaken:]) - trimming)
        
        if trim >= 9:
            bigger = bigger[:trim]
        else:
            bigger = bigger[:9]

    #Trim initially smaller list down to size
    totalRemaining = len(bigger) + len(smaller)
    trimming = totalRemaining - 18
    if trimming <= 0:
        pass
    else:
        smaller = smaller[:9]
    
    if smallerOne == 'Taken':
        for i in bigger:
            if allCountries[i] == '🏳️':
                displayedFree += i + ' has no flag assigned!\n'
            else:
                displayedFree += i + ': ' + allCountries[i] + '\n'
            newFreeBottom += 1
        for i in smaller:
            if allCountries[i] == '🏳️':
                displayedTaken += i + ' has no flag assigned!\n'
            else:
                displayedTaken += i + ': ' + allCountries[i] + '\n'
            newTakenBottom += 1
    else:
        for i in smaller:
            if allCountries[i] == '🏳️':
                displayedFree += i + ' has no flag assigned!\n'
            else:
                displayedFree += i + ': ' + allCountries[i] + '\n'
            newFreeBottom += 1
        for i in bigger:
            if allCountries[i] == '🏳️':
                displayedTaken += i + ' has no flag assigned!\n'
            else:
                displayedTaken += i + ': ' + allCountries[i] + '\n'
            newTakenBottom += 1

    if displayedFree == '':
        displayedFree = "There's no countries available to be claimed here."
    if displayedTaken == '':
        displayedTaken = "There's no countries claimed by players here."
    
    embed = discord.Embed(
    title = 'Country Claims',
    description = 'Click on a reaction to claim your nation. [Get your own Lss Bot.](https://discord.com/api/oauth2/authorize?client_id=727015243246600193&permissions=268446800&scope=bot)',
    color = discord.Color(000000)
    ) 
    
    embed.add_field(name = 'Available Nations', value = displayedFree),
    embed.add_field(name = 'Taken Nations', value = displayedTaken),
    embed.set_footer(text= str(bottomFree) + ', ' + str(bottomTaken) + ', ' + str(newFreeBottom) + ', ' + str(newTakenBottom))

    return embed,smallerOne,smaller,bigger,allCountries,bottomFree,newFreeBottom,bottomTaken,newTakenBottom

async def claimsFunc(channel,bottomFree,bottomTaken):
    
    finalembeds = await claimsEmbed(channel,bottomFree,bottomTaken)
    finalembed = await channel.send(embed = finalembeds[0])
    smallerOne = finalembeds[1]
    smaller = finalembeds[2]
    bigger = finalembeds[3]
    allCountries = finalembeds[4]
    bottomFree = finalembeds[5]
    newFreeBottom = finalembeds[6]
    bottomTaken = finalembeds[7]
    newTakenBottom = finalembeds[8]

    #Add reactions, starting with the free nations
    if smallerOne == 'Free': 
        for i in smaller:
            reaction = allCountries[i]
            if reaction != '🏳️':
                await finalembed.add_reaction(str(reaction))
        for i in bigger:
            reaction = allCountries[i]
            if reaction != '🏳️':
                await finalembed.add_reaction(str(reaction))
    else:
        for i in bigger:
            reaction = allCountries[i]
            if reaction != '🏳️':
                await finalembed.add_reaction(str(reaction))
        for i in smaller:
            reaction = allCountries[i]
            if reaction != '🏳️':
                await finalembed.add_reaction(str(reaction))

    #Determine arrows
    #len(freeCountries[bottomFree:]) + len(takenCountries[bottomTaken:])
    if newFreeBottom + newTakenBottom != len(allCountries):
        await finalembed.add_reaction('➡️')
    await finalembed.add_reaction('❌')    

#Admin Help Commands
async def countryListFunc(channel,user,origin,pageNumber):

    data = await readServerInfo(channel.guild.id)

    countryList = list(data['countries'].keys())
    reactionList = list(data['countries'].values())
    countries = ''
    countryListLength = len(countryList)
    maxPageSize = 10
    maximumPages = math.ceil(countryListLength/maxPageSize)
    currentRange = (pageNumber*maxPageSize)

    for i in range(currentRange-maxPageSize,min(countryListLength,currentRange)):
        if countryList[i] in data['players'].values():
            for key, value in data['players'].items():
                if value == countryList[i]:
                    playerID = key
            takenBy = ', taken by ' + (await client.fetch_user(playerID)).name + '.'
        else:
            takenBy = ''
        countries += (str(i+1) + '. ' + countryList[i] + ':   ' +  reactionList[i] + takenBy + '\n')
    
    if len(countries) == 0:
        lower = '0'
    else:
        lower = str(currentRange-maxPageSize+1)

    if len(countryList) == 1:
        countryWord = ' country'
    else:
        countryWord = ' countries'

    #Message
    embed = discord.Embed(
    title = ('Country List for ' + str(user).split('#')[0]),
    description = 'Currently displaying countries from ' + lower + ' to '
    + str(min(countryListLength,currentRange)) + ". There's "
    + str(countryListLength) + countryWord + ' total.\n' + countries,
    color = discord.Color(000000)
    ) 
    
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        if pageNumber > 1:
            await finalembed.add_reaction('⬅️')
        await finalembed.add_reaction('↩️')
        if pageNumber < maximumPages:
            await finalembed.add_reaction('➡️')
        await finalembed.add_reaction('❌')
    except:
        return

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,user.id,60)
    if rawReaction:
        reaction = str(rawReaction.emoji)

    #Act based on reaction
    if rawReaction != None:
        if reaction == '⬅️':
            await finalembed.delete()
            await countryListFunc(channel,user,origin,pageNumber-1)
        if reaction == '↩️':
            await finalembed.delete()
            await origin(channel,user)
        if reaction == '➡️' :
            await finalembed.delete()
            await countryListFunc(channel,user,origin,pageNumber+1)
        else:
            await finalembed.delete()
    else:
        await finalembed.delete()
        exiting = await channel.send("No reaction recieved in the last minute. Closing...")
        await asyncio.sleep(5)
        await exiting.delete()
        return

async def resetFunc(channel,user):
    
    if await checkPerm(channel,user) == False:
        return

    data = await readServerInfo(channel.guild.id)

    for i in channel.guild.roles:
        if i.name in data['countries'] or data['titles']:
            await i.delete()
            
    for i in channel.guild.channels:
        if i.name in list(x.lower().replace(' ','-') for x in data['countries'].keys()):
            await i.delete()

    try:
        possibleCountries = next(filter(lambda x: x.name == 'Countries', channel.guild.categories))
        await possibleCountries.delete()    
    except:
        pass

    try:
        possibleDiplo = next(filter(lambda x: x.name == 'Diplomacy', channel.guild.categories))
        for i in possibleDiplo.channels:
            await i.delete()
            await possibleDiplo.delete()
    except:
        pass

    
    if os.path.exists('serverData/'+ str(channel.guild.id) + '.txt'):
        os.remove('serverData/'+ str(channel.guild.id) + '.txt')
    await addServerVars(channel.guild)

    reaction = await promptFunc(channel, user, 'Info reset!', 'All information (roles, channels, countries, reactions, titles, options) has now been erased.', 'This message will delete itself in 30 seconds.','↩️','❌')
    if reaction == '↩️':
        await adminHelpFunc(channel,user)
    else:
        return

async def optionsFunc(channel,user):

    if await checkPerm(channel,user) == False:
        return

    embed = discord.Embed(
    title = ('Options Menu for ' + str(user).split('#')[0]),
    description = 'Just click a reaction.',
    color = discord.Color(000000)
    ) 
    
    data = await readServerInfo(channel.guild.id)
    cCC = data['options']['countryChannelCreation']
    cCD = data['options']['countryChannelDeletion']
    pU = data['options']['playerUnclaim']

    embed.add_field(name = 'Preferences:', value = ':writing_hand: Country channels are *created* on country **' + cCC + '**\n:wastebasket: Country channels are *deleted* on country **' +
                    cCD + '**\n:dagger: Players have their nations unclaimed **' + pU + '**')

    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('✍️')
        await finalembed.add_reaction('🗑️')
        await finalembed.add_reaction('🗡️')
        await finalembed.add_reaction('❓')
        await finalembed.add_reaction('❌')
    except:
        return

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,user.id,60)
    if rawReaction:
        reaction = str(rawReaction.emoji)

    #Act based on reaction
    if rawReaction != None:
        if reaction == '✍️':
            if cCC == 'creation.':
                data['options']['countryChannelCreation'] = 'claiming.'
                await writeServerInfo(channel.guild.id,data)
            if cCC== 'claiming.':
                data['options']['countryChannelCreation'] = "...actually, they aren't."
                await writeServerInfo(channel.guild.id,data)
            if cCC== "...actually, they aren't.":
                data['options']['countryChannelCreation'] = 'creation.'
                await writeServerInfo(channel.guild.id,data)

            await finalembed.delete()
            await optionsFunc(channel,user)
        if reaction == '🗑️':
            if cCD == 'unclaiming.':
                data['options']['countryChannelDeletion'] = 'deletion.'
                await writeServerInfo(channel.guild.id,data)
            if cCD== 'deletion.':
                data['options']['countryChannelDeletion'] = 'unclaiming.'
                await writeServerInfo(channel.guild.id,data)
            await finalembed.delete()
            await optionsFunc(channel,user)
        if reaction == '🗡️':
            if pU == 'by having an Admin click their flag in Lss!claims.':
                data['options']['playerUnclaim'] = 'by clicking on their own flag in Lss!claims.'
                await writeServerInfo(channel.guild.id,data)
            if pU== 'by clicking on their own flag in Lss!claims.':
                data['options']['playerUnclaim'] = 'by having an Admin click their flag in Lss!claims.'
                await writeServerInfo(channel.guild.id,data)
            await finalembed.delete()
            await optionsFunc(channel,user)
        if reaction == '❓' :
            await finalembed.delete()
            await adminHelpFunc(channel,user)
        else:
            try:
                await finalembed.delete()
            except:
                return
    else:
        await finalembed.delete()
        exiting = await channel.send("No reaction recieved in the last minute. Closing...")
        await asyncio.sleep(5)
        await exiting.delete()
        return

async def commandsFunc(channel,user):
    description = ('**Help**: The main menu.' +
                "\n**Help <command name>:** Tells you specific info for that command (i.e. Lss!help CountryList)." +
                '\n**AdminHelp**: Admin commands like Lss!reset.' +
                "\n**Setup:** First-time setup wizard." +
                "\n**Claims:** Displays the country-claiming and unclaiming prompt." +
                "\n**Diplo <Country 1> <Country 2> ...:** Creates a private chat for these countries." +
                '\n- - - - - -' +
                "\n**CountryMenu:** Country-specific menu." +
                "\n**CountryList:** Displays all countries." +
                "\n**CountryMaker:** For making new countries." +
                "\n**RemoveCountry:** Removes countries." +
                "\n**RenameCountry:** Renames countries." +
                '\n- - - - - -' +
                "\n**ReactionMenu:** Reaction (emoji)-specific menu." +
                "\n**RemoveReaction:** Removes reactions." +
                "\n**UpdateReaction:** Adds or edits reactions." +
                "\n**AssignReactions:** Adds reactions if missing." +
                '\n- - - - - -' +
                "\n**TitleMenu:** Title-specific menu." +
                "\n**TitleList:** Displays all titles." +
                "\n**Retitle:** Adds or edits titles." +
                "\n**RemoveTitle:** Removes titles.." +
                '\n- - - - - -' +
                "\n**Reset:** Clears and resets all server info." +
                "\n**Options:** Adjusts the settings for this server." +
                "\n**Commands:** Shows you this list." +
                "\n**Servers:** Displays server count.")

    reaction = await promptFunc(channel,user,('Commands Menu for ' + str(user).split('#')[0]),description,'Only the Lss!prefix is case-sensitive. Type Lss!help (command) for more details.','↩️','❌')
    if reaction == '↩️':
        await adminHelpFunc(channel,user)
    else:
        return

#Country Commands - Complete
async def countryMakerFunc(channel,user,country,flagFound,setup):
    
    if await checkPerm(channel,user) == False:
        return
    
    data = await readServerInfo(channel.guild.id)

    countryRoleExists = False

    if country:
        country = country.mention + ' added! '
    else:
        country = ''

    if flagFound:
        flagAdded = "The flag reaction for this country has been automatically assigned.\n"
    else:
        flagAdded = ''

    #Message
    embed = discord.Embed(
    title = ('Country Annex'),
    description = (str(country) + flagAdded + 'To add a new country, just say its name.\n'),
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'Press the back button to view the full options.')
    finalembed = await channel.send(embed=embed)

    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌') 
    except:
        return


    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == user.id and payload.channel_id == channel.id, timeout=30)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id == user.id and message.channel.id == channel.id, timeout=30))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
            pass
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
            pass

    except:
        await finalembed.delete()
        exiting = await channel.send("You haven't responded in a bit. Exiting...")
        await asyncio.sleep(5)
        await exiting.delete()
        return

        
    #Act based on reaction
    if resultType == 'reaction':
        reaction = str(result.emoji)
        if reaction == '↩️':
            await finalembed.delete()
            await countryMenuFunc(channel,user)
        else:
            await finalembed.delete()
            return
    
    if resultType == 'message':
        countryName = result.content
        if countryName in countryFlags:
            reaction = countryFlags[countryName]
            foundFlag = True
        else:
            reaction = '🏳️'
            foundFlag = False

        for i in channel.guild.roles:
            if i.name == countryName:
                countryRoleExists = True
                countryRole = i
                break
        if countryRoleExists == False:
            countryRole = await channel.guild.create_role(name = countryName,
            hoist = True, mentionable = True, color = discord.Colour.from_hsv(random.uniform(0, 1), .3, 1))

        data['countries'].update({countryName : reaction})
        if data['options']['countryChannelCreation'] == 'creation.':
            await createChannel(channel.guild,countryName,countryRole)
        await writeServerInfo(channel.guild.id,data)

        await finalembed.delete()
        await result.delete()
        if setup:
            return
        else:
            await countryMakerFunc(channel,user,countryRole,foundFlag,False)

async def renameCountryFunc(channel,user,rename): #when you rename a country, remember to check if there's a custom title for it and rename the key for it
    
    if await checkPerm(channel,user) == False:
        return

    data = await readServerInfo(channel.guild.id)

    if rename:
        rename = rename + ' renamed!\nTo rename another country'
    else:
        rename = 'First'

    #First message
    embed = discord.Embed(
    title = 'Rename Country',
    description = rename + ', type the name of the country you want to rename.',
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'This message will delete itself in 30 seconds.')
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌')
    except:
        return
    

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == user.id and payload.channel_id == channel.id, timeout=30)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id == user.id and message.channel.id == channel.id, timeout=30))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
            pass
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
            pass

    except:
        await finalembed.delete()
        exiting = await channel.send("You didn't respond in the time you were given. Exiting...")
        await asyncio.sleep(5)
        await exiting.delete()
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        reaction = str(result.emoji)
        if reaction == '↩️':     
            await finalembed.delete()
            await countryMenuFunc(channel,user)
        else:
            await finalembed.delete()
            
    if resultType == 'message':
        oldKey = result.content
        lowerCountries = {}
        for key, value in data['countries'].items():
            lowerCountries.update({key.lower() : value})
        try:
            value = lowerCountries[oldKey.lower()]
            await result.delete()
        except:
            await finalembed.delete()
            await result.delete()
            exiting = await channel.send("'" + result.content + "' doesn't exist. Add it as a country first.")
            await asyncio.sleep(5)
            await exiting.delete()
            await renameCountryFunc(channel,user,False)
            return


    #Check if message wasn't just closed out before continuing
    try:
        await channel.fetch_message(finalembed.id)
    except:
        return

    await finalembed.delete()

     #Second message
    embed = discord.Embed(
    title = 'Rename Country',
    description = 'Second, type what you want to rename ' + result.content + ' to.',
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'This message will delete itself in 30 seconds.')
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌')
    except:
        return
    

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == user.id and payload.channel_id == channel.id, timeout=30)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id == user.id and message.channel.id == channel.id, timeout=30))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
            pass
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
            pass

    except:
        await finalembed.delete()
        exiting = await channel.send("You didn't respond in the time you were given. Exiting...")
        await asyncio.sleep(5)
        await exiting.delete()
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        reaction = str(result.emoji)
        if reaction == '↩️':   
            await finalembed.delete()
            await countryMenuFunc(channel,user)
        if reaction == '❌':
            await finalembed.delete()
            
    if resultType == 'message':
        newKey = result.content.lower()
        await result.delete()


    #Check if message wasn't just closed out before continuing
    try:
        await channel.fetch_message(finalembed.id)
    except:
        return

    #Check that no country already exists with that name
    if result.content.lower() in lowerCountries:
        await finalembed.delete()
        exiting = await channel.send("You can't give a country a name that's already in use. Either delete the old country or come up with a new name for this one.")
        await asyncio.sleep(5)
        await exiting.delete()
        await renameCountryFunc(channel,user,False)
        return

    #Update to new values
    for i in data['countries'].keys():
        if i.lower() == oldKey.lower():
            del data['countries'][i]
            break
    data['countries'].update({result.content : value})
    await writeServerInfo(channel.guild.id,data)

    for i in channel.guild.roles:
        if i.name == oldKey:
            await i.edit(name=result.content)
    for i in channel.guild.channels:
        if i.name == oldKey.lower():
            await i.edit(name=result.content)
    await finalembed.delete()
    await renameCountryFunc(channel,user,oldKey)

async def removeCountryFunc(channel,user,delete):
    
    if await checkPerm(channel,user) == False:
        return

    data = await readServerInfo(channel.guild.id)

    if delete:
        delete = delete + ' removed!\nTo delete another country, type'
    else:
        delete = 'Type'

    #First message
    embed = discord.Embed(
    title = 'Remove Country',
    description = delete + ' the name of the country you want to remove.',
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'This message will delete itself in 30 seconds.')
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌')
    except:
        return
    

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == user.id and payload.channel_id == channel.id, timeout=30)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id == user.id and message.channel.id == channel.id, timeout=30))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
            pass
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
            pass

    except:
        await finalembed.delete()
        exiting = await channel.send("You didn't respond in the time you were given. Exiting...")
        await asyncio.sleep(5)
        await exiting.delete()
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        reaction = str(result.emoji)
        if reaction == '↩️':     
            await finalembed.delete()
            await countryMenuFunc(channel,user)
        else:
            await finalembed.delete()
            
    if resultType == 'message':
        deletedCountry = result.content
        await finalembed.delete()
        await result.delete()

        if deletedCountry in data['titles']:
            deletedRole = data['titles'][deletedCountry]
            del data['titles'][deletedCountry]
            await writeServerInfo(channel.guild.id,data)
        else:
            deletedRole = deletedCountry
        try:
            del data['countries'][deletedCountry]
            await writeServerInfo(channel.guild.id,data)
            for i in channel.guild.roles:
                if i.name == deletedRole:
                    try:
                        await i.delete()
                    except:
                        pass
                    break
            try:
                await removeChannel(channel.guild,deletedCountry.lower().replace(' ','-'))
            except:
                pass
        except:
            exiting = await channel.send("'" + deletedCountry + "' already doesn't exist in the Lss.")
            await asyncio.sleep(5)
            await exiting.delete()
            await removeCountryFunc(channel,user,False)
            return

        await removeCountryFunc(channel,user,deletedCountry)

#Reaction Commands - Complete
async def removeReactionFunc(channel,user,delete):
    
    if await checkPerm(channel,user) == False:
        return

    data = await readServerInfo(channel.guild.id)

    if delete:
        delete = delete + "'s reaction removed!\nTo delete another reaction, type"
    else:
        delete = 'Type'

    #First message
    embed = discord.Embed(
    title = 'Remove Reaction',
    description = delete + ' the name of the country whose reaction you want to remove.',
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'This message will delete itself in 30 seconds.')
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌')
    except:
        return
    

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == user.id and payload.channel_id == channel.id, timeout=30)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id == user.id and message.channel.id == channel.id, timeout=30))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
            pass
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
            pass

    except:
        await finalembed.delete()
        exiting = await channel.send("You didn't respond in the time you were given. Exiting...")
        await asyncio.sleep(5)
        await exiting.delete()
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        reaction = str(result.emoji)
        if reaction == '↩️':     
            await finalembed.delete()
            await reactionMenuFunc(channel,user)
        else:
            await finalembed.delete()
            
    if resultType == 'message':
        deletedCountry = result.content
        await finalembed.delete()
        await result.delete()
        try:
            data['countries'].update({deletedCountry : '🏳️'})
            await writeServerInfo(channel.guild.id,data)
        except:
            exiting = await channel.send("'" + deletedCountry + "' doesn't exist in the Lss.")
            await asyncio.sleep(5)
            await exiting.delete()
            await removeReactionFunc(channel,user,False)
            return

        await removeReactionFunc(channel,user,deletedCountry)

async def updateReactionFunc(channel,user,rename):
    
    if await checkPerm(channel,user) == False:
        return

    data = await readServerInfo(channel.guild.id)

    if rename:
        rename = rename + "'s reaction has been updated!\nTo update another country's reaction"
    else:
        rename = 'First'

    #First message
    embed = discord.Embed(
    title = 'Update Reaction',
    description = rename + ', type the name of the country whose reaction you want to update.',
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'This message will delete itself in 30 seconds.')
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌')
    except:
        return
    

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == user.id and payload.channel_id == channel.id, timeout=30)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id == user.id and message.channel.id == channel.id, timeout=30))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
            pass
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
            pass

    except:
        await finalembed.delete()
        exiting = await channel.send("You didn't respond in the time you were given. Exiting...")
        await asyncio.sleep(5)
        await exiting.delete()
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        reaction = str(result.emoji)
        if reaction == '↩️':     
            await finalembed.delete()
            await reactionMenuFunc(channel,user)
        else:
            await finalembed.delete()
            
    if resultType == 'message':
        if result.content in data['countries']:
            key = result.content
            await result.delete()
        else:
            await result.delete()
            exiting = await channel.send("'" + result.content + "' doesn't exist in the Lss.")
            await asyncio.sleep(5)
            await exiting.delete()
            await finalembed.delete()
            await updateReactionFunc(channel,user,'')
            return



    #Check if message wasn't just closed out before continuing
    try:
        await channel.fetch_message(finalembed.id)
    except:
        return
    
    await finalembed.delete()

    #Second message
    embed = discord.Embed(
    title = 'Update Reaction',
    description = 'Second, update ' + key + " by reacting with the desired emoji or speaking it (like `:flag_us:`.)",
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'This message will delete itself in 30 seconds.')
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌')
    except:
        return
    

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == user.id and payload.channel_id == channel.id, timeout=30)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id == user.id and message.channel.id == channel.id, timeout=30))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
            pass
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
            pass

    except:
        await finalembed.delete()
        exiting = await channel.send("You didn't respond in the time you were given. Exiting...")
        await asyncio.sleep(5)
        await exiting.delete()
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        reaction = str(result.emoji)
        if reaction == '↩️':   
            await finalembed.delete()
            await reactionMenuFunc(channel,user)
        if reaction == '❌':
            await finalembed.delete()
        else:
            value = result.emoji.name
            
    if resultType == 'message':
        
        if result.content[0] not in letters:
            value = result.content[0]
            await result.delete()
        else:
            exiting = await channel.send("'" + result.content + "' isn't a valid emoji reaction.")
            await result.delete()
            await asyncio.sleep(5)
            await exiting.delete()
            await finalembed.delete()
            await updateReactionFunc(channel,user,'')
            return


    #Check if message wasn't just closed out before continuing
    try:
        await channel.fetch_message(finalembed.id)
    except:
        return


    #Update to new values
    data['countries'].update({key : value})
    await writeServerInfo(channel.guild.id,data)
    await finalembed.delete()
    await updateReactionFunc(channel,user,key)

async def assignReactionsFunc(channel,user,assign,setup):
    
    if await checkPerm(channel,user) == False:
        return

    data = await readServerInfo(channel.guild.id)

    unreactedCountries = list()
    for key, value in data['countries'].items():
        if value == '🏳️':
            unreactedCountries.append(key)

    if assign is False:
        assigned = ''
    else:
        assigned = assign + " has been assigned! "


    if len(unreactedCountries) == 1:
        message = "There's only one country to assign a reaction to.\n"
    elif len(unreactedCountries) > 1:
        message = 'You have ' + str(len(unreactedCountries)) + ' countries to assign reactions to.\n'
    else:
        message = assigned + "\nEvery country has a reaction to it, so there's no need to stay here."
        embed = discord.Embed(
        title = 'Assign Reactions',
        description = message,
        color = discord.Color(000000)
        ) 
    
        embed.set_footer(text = 'This message will delete itself in 5 seconds.')
        finalembed = await channel.send(embed=embed)
        await asyncio.sleep(5)
        await finalembed.delete()
        await reactionMenuFunc(channel,user)
        return

    key = unreactedCountries[0]
    embed = discord.Embed(
    title = 'Assign Reactions',
    description = assigned + message + 'Assign a reaction to ' + key + " by reacting with the desired emoji or speaking it (like `:flag_us:`.)",
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'This message will delete itself in 30 seconds.')
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌')
    except:
        return

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == user.id and payload.channel_id == channel.id, timeout=30)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id == user.id and message.channel.id == channel.id, timeout=30))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
            pass
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
            pass

    except:
        await finalembed.delete()
        exiting = await channel.send("You didn't respond in the time you were given. Exiting...")
        await asyncio.sleep(5)
        await exiting.delete()
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        reaction = str(result.emoji)
        if reaction == '↩️':   
            await finalembed.delete()
            await reactionMenuFunc(channel,user)
        if reaction == '❌': 
            await finalembed.delete()
        else:
            value = result.emoji.name
            
    if resultType == 'message':
        if result.content[0] not in letters:
            value = result.content[0]
            await result.delete()
        else:
            await result.delete()
            exiting = await channel.send("'" + result.content + "' isn't a valid emoji reaction.")
            await asyncio.sleep(5)
            await exiting.delete()
            await finalembed.delete()
            await assignReactionsFunc(channel,user,False,False)
            return


    #Check if message wasn't just closed out before continuing
    try:
        await channel.fetch_message(finalembed.id)
    except:
        return


    #Update to new values
    data['countries'].update({key : value})
    await writeServerInfo(channel.guild.id,data)
    await finalembed.delete()
    if setup:
        return
    else:
        await assignReactionsFunc(channel,user,key,False)

#Title Commands - Complete
async def titleListFunc(channel,user,pageNumber):

    data = await readServerInfo(channel.guild.id)

    titlesCountries = list(data['titles'].keys())
    titlesRoles = list(data['titles'].values())
    titles = ''
    titlesCountriesLength = len(titlesCountries)
    maxPageSize = 10
    maximumPages = math.ceil(titlesCountriesLength/maxPageSize)
    currentRange = (pageNumber*maxPageSize)
    for i in range(currentRange-maxPageSize,min(titlesCountriesLength,currentRange)):
        titles += (str(i+1) + '. ' + titlesCountries[i] + ':   ' +  titlesRoles[i] + '\n')
    
    if len(titles) == 0:
        lower = '0'
    else:
        lower = str(currentRange-maxPageSize+1)

    #Message
    embed = discord.Embed(
    title = ('Country Title List for ' + str(user).split('#')[0]),
    description = 'Currently displaying country titles from ' + lower + ' to ' + str(min(titlesCountriesLength,currentRange)) + ". There's " + str(titlesCountriesLength) + ' titles total.\n' + titles,
    color = discord.Color(000000)
    ) 
    
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        if pageNumber > 1:
            await finalembed.add_reaction('⬅️')
        await finalembed.add_reaction('↩️')
        if pageNumber < maximumPages:
            await finalembed.add_reaction('➡️')
        await finalembed.add_reaction('❌')
    except:
        return

    #Recieve reactions, and assign to reaction if user responded
    rawReaction = await listenReactFunc(channel,user.id,60)
    if rawReaction:
        reaction = str(rawReaction.emoji)

    #Act based on reaction
    if rawReaction != None:
        if reaction == '⬅️':
            await finalembed.delete()
            await countryListFunc(channel,user,titleListFunc,pageNumber-1)
        if reaction == '↩️':
            await finalembed.delete()
            await titleMenuFunc(channel,user)
        if reaction == '➡️' :
            await finalembed.delete()
            await countryListFunc(channel,user,titleListFunc,pageNumber+1)
        else:
            await finalembed.delete()
    else:
        await finalembed.delete()
        exiting = await channel.send("No reaction recieved in the last minute. Closing...")
        await asyncio.sleep(5)
        await exiting.delete()
        return

async def retitleFunc(channel,user,country,role):
    
    if await checkPerm(channel,user) == False:
        return
    
    data = await readServerInfo(channel.guild.id)

    if role:
        newRole = 'The title for someone in charge of ' + country + ' is now ' + str(role) + '!\nTo set the title for another country'
    else:
        newRole = 'First'

    #First message
    embed = discord.Embed(
    title = 'Re-title Country',
    description = newRole + ', type the name of the country you want to give a new title.',
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'This message will delete itself in 30 seconds.')
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌')
    except:
        return
    

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == user.id and payload.channel_id == channel.id, timeout=30)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id == user.id and message.channel.id == channel.id, timeout=30))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
            pass
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
            pass

    except:
        await finalembed.delete()
        exiting = await channel.send("You didn't respond in the time you were given. Exiting...")
        await asyncio.sleep(5)
        await exiting.delete()
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        reaction = str(result.emoji)
        if reaction == '↩️':     
            await finalembed.delete()
            await titleMenuFunc(channel,user)
        else:
            await finalembed.delete()
            
    if resultType == 'message':
        countryName = result.content
        if countryName in data['countries']:
            await result.delete()
        else:
            await finalembed.delete()
            await result.delete()
            exiting = await channel.send("'" + result.content + "' doesn't exist. Add it as a country first.")
            await asyncio.sleep(5)
            await exiting.delete()
            await retitleFunc(channel,user,'',False)
            return


    #Check if message wasn't just closed out before continuing
    try:
        await channel.fetch_message(finalembed.id)
    except:
        return

    await finalembed.delete()


     #Second message
    embed = discord.Embed(
    title = 'Re-title Country',
    description = 'Second, type what you want to assign ' + countryName + "'s title to.",
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'This message will delete itself in 30 seconds.')
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌')
    except:
        return
    

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == user.id and payload.channel_id == channel.id, timeout=30)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id == user.id and message.channel.id == channel.id, timeout=30))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
            pass
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
            pass

    except:
        await finalembed.delete()
        exiting = await channel.send("You didn't respond in the time you were given. Exiting...")
        await asyncio.sleep(5)
        await exiting.delete()
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        reaction = str(result.emoji)
        if reaction == '↩️':   
            await finalembed.delete()
            await titleMenuFunc(channel,user)
        else:
            await finalembed.delete()
            
    if resultType == 'message':
        newRoleName = result.content
        await result.delete()


    #Check if message wasn't just closed out before continuing
    try:
        await channel.fetch_message(finalembed.id)
    except:
        return


    #Update to new values
    if countryName in data['titles'].keys():
        oldRoleName = data['titles'][countryName]
    else:
        oldRoleName = countryName

    for i in channel.guild.roles:
        if i.name == oldRoleName:
            await i.edit(name=newRoleName)
    data['titles'].update({countryName: newRoleName})
    await writeServerInfo(channel.guild.id,data)
    await finalembed.delete() 
    await retitleFunc(channel,user,countryName,newRoleName)

async def removeTitleFunc(channel,user,role):
    
    if await checkPerm(channel,user) == False:
        return
    
    data = await readServerInfo(channel.guild.id)

    if role:
        role = role + "'s title removed!\nTo delete another country's title, type"
    else:
        role = 'Type'

    #First message
    embed = discord.Embed(
    title = 'Remove Title',
    description = role + ' the name of the country whose title you want to remove.',
    color = discord.Color(000000)
    ) 
    
    embed.set_footer(text = 'This message will delete itself in 30 seconds.')
    finalembed = await channel.send(embed=embed)
    
    #Add reactions, if message hasn't been closed out yet
    try:
        await finalembed.add_reaction('↩️')
        await finalembed.add_reaction('❌')
    except:
        return
    

    #Wait for either reaction or reply
    pending_tasks = [asyncio.create_task(client.wait_for('raw_reaction_add', check=lambda payload: payload.user_id == user.id and payload.channel_id == channel.id, timeout=30)),
                    asyncio.create_task(client.wait_for('message', check = lambda message: message.author.id == user.id and message.channel.id == channel.id, timeout=30))]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    #Cancel whichever task would have come second
    for task in pending_tasks:
        task.cancel()
    #Return completed task result
    try: 
        result = (done_tasks.pop().result())
        if isinstance(result, discord.message.Message):
            resultType = 'message'
            pass
        if isinstance(result, discord.raw_models.RawReactionActionEvent):
            resultType = 'reaction'
            pass

    except:
        await finalembed.delete()
        exiting = await channel.send("You didn't respond in the time you were given. Exiting...")
        await asyncio.sleep(5)
        await exiting.delete()
        return
        

    #Act based on reaction
    if resultType == 'reaction':
        reaction = str(result.emoji)
        if reaction == '↩️':     
            await finalembed.delete()
            await titleMenuFunc(channel,user)
        else:
            await finalembed.delete()
            
    if resultType == 'message':
        deletedCountry = result.content
        await finalembed.delete()
        await result.delete()
        if deletedCountry in data['titles']:
            modifiedRoleName = data['titles'][deletedCountry]
            count = 0
            for count, role in enumerate(channel.guild.roles):
                if str(role.name) == str(modifiedRoleName):
                    await channel.guild.roles[count].edit(name = deletedCountry)
                count += 1
            del data['titles'][deletedCountry]
            await writeServerInfo(channel.guild.id,data)
        else:
            exiting = await channel.send("'" + deletedCountry + "' doesn't exist in the Lss.")
            await asyncio.sleep(5)
            await exiting.delete()
            await removeTitleFunc(channel,user,False)
            return

        await removeTitleFunc(channel,user,deletedCountry)


#Execute
client.run(environ['discordToken'])