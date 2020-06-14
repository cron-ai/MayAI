import discord
from discord.ext import commands
import signal
import sys
import datetime
import random
from re import match
import asyncio
import os
import aiohttp
import requests
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import json

#CTRLC handling
def signal_handler(signal, frame):
    print("Thank you for using CRON!")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Token
token = ''

client = commands.Bot(command_prefix='>')

with open("greetings.json") as file:
    data = json.load(file)

greetings = []
greetings_reply = []

for intent in data["intents"]:

    for patterns in intent["patterns"]:
        wrds = patterns
        patterns = patterns.lower()
        greetings.append(patterns)

    for responses in intent["responses"]:
        wrds = responses
        greetings_reply.append(responses)

x = datetime.datetime.now()

@client.event
async def reply(message, respond):
    ## Create voice file
    x = datetime.datetime.now()
    date_string = x.strftime("%d%m%Y%H%M%S")
    tts = gTTS(text=respond, lang="en")
    filename = "voice"+date_string+".mp3"
    tts.save(filename)
    # Response  
    ## Connect to voice
    channel = message.author.voice.channel
    vc = await channel.connect()
    ## Respond to channel
    await message.channel.send(respond)
    ## Create a player
    vc.play(discord.FFmpegPCMAudio(filename), after=lambda e: print('done', e))
    while vc.is_playing ():
        await asyncio.sleep(1)
    # disconnect after the player has finished
    vc.stop()
    vcl = message.guild.voice_client
    await vcl.disconnect()
    ## Deleting that file
    os.remove(filename)

@client.event

async def on_ready():
    activity = discord.Game(name="Decoding")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('Cron is activated.')

@client.event

async def on_message(message):

    # Valid channels
    valid_channels = ["cron-may-testing"]

    if str(message.channel) in valid_channels:      

        if message.author == client.user:
            return
        
        if any(i in message.content.lower() for i in greetings):

            response = f'{random.choice(greetings_reply)}'

            await reply(message, response)

        elif "date today" in message.content.lower():

            await message.channel.send(x.strftime("%x"))
        
        elif "creator" in message.content.lower():

            response = "Manal and Somil have created me and they're still working on me."
            
            await reply(message, response)

        elif "!decrypt" in message.content.lower():

            response = message.content[9:]

            dapi = requests.get('https://md5decrypt.net/Api/api.php?hash=' + response + '&hash_type=md5&email=deanna_abshire@proxymail.eu&code=1152464b80a61728').text

            await message.channel.send("Key :- " + dapi)

        elif "introduce yourself" in message.content.lower():

            response = "Hey! I am May. I came into existance on 14 June 2020."

            await reply(message, response)


client.run(token)