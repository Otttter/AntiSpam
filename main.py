import discord
import asyncio
import configparser
import os

#
# Any issues feel free to message my discord Otter#7070
#

# Config template
cfgT = """[bot]
token: tokenhere
prefix: prefixhere
"""

# Pre-shit
token = ""
prefix = ""

usrBlacklist = list()

# Blacklist shit
if not os.path.exists("blacklist.txt"):
    tmpF = open("blacklist.txt", "w")
    tmpF.write("put common users here")
    tmpF.close()
    print("The blacklist file has been created, please put usernames that are common in the spammed groups on each line in the file")
    input("Press Enter to exit")
    exit(7)
else:
    tmpF = open("blacklist.txt", "r")
    fLines = tmpF.readlines()
    
    for line in fLines:
        usrBlacklist.append(str(line))
    
    print("Blacklist loaded!")

# Config shit 
if not os.path.exists("config.ini"):
    tmpF = open("config.ini", "w")
    tmpF.write(cfgT)
    print("Config was not found so a new one was created! Please fill in the required fields and relaunch!")
    input("Press Enter to exit")
    exit(6)
else:
    print("Config found, grabbing settings")
    cfgHandler = configparser.ConfigParser()
    cfgHandler.read("config.ini")
    token  = str(cfgHandler.get("bot", "token" ))
    prefix = str(cfgHandler.get("bot", "prefix"))
    print("Config loaded successfully! Proceeding.")
    
    

client = discord.Client()

@client.event
async def on_ready():
    print("Token Verification Successful! Bot is running!") # Tell the user the script is actually running.

@client.event
async def on_message(message):
    if message.author == client.user:
        cmd = str(message.content).split(' ')
        if cmd[0] == prefix + "execute":
            await message.delete()
            count = 0
            for channel in client.private_channels:
                if isinstance(channel, discord.GroupChannel):
                    if channel.id != message.channel.id: # If the message was sent in a group chat, dont leave it.
                        for blUsr in usrBlacklist:
                            for usr in channel.recipients: # Credit to Botings#2199 for showing me something that I couldn't find in the api
                                if blUsr == usr.name:
                                    count = count + 1
                                    print("Left a group: " + str(channel.name) + " | " + str(channel.id)) # Print group ID in console.               
                                    await channel.leave()
            await message.channel.send("``You left a total of [" + str(count) + "] group chats!``")
            await client.close() # Updated because they changed it for some reason

client.run(token, bot=False)
input("Press enter to exit") # Allow user to actually fucking read the data before the script closes.
