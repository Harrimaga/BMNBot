import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from datetime import datetime, timedelta, date
import pickle
import asyncio

Client = discord.Client()
client = commands.Bot(command_prefix = "!")

firstItems = {}

global Songs
Songs = dict.fromkeys(firstItems)

with open("SongDict", "rb") as load:
    Songs = pickle.load(load)

async def checkSongs():
    await client.wait_until_ready()
    while not client.is_closed:
        now = datetime.utcnow()
        tobedeleted = []
        for times in Songs.keys():
            if times.hour == now.hour and times.day == now.day:
                await client.send_message(client.get_channel("500419426974302224"), "Dit uur in de top 2000: " + Songs[times])
                tobedeleted.append(times)

        for i in tobedeleted:
            Songs.pop(i)

        await asyncio.sleep(60)

@client.event
async def on_ready():

    global GameMode
    print("Ready to Rock!")
    await client.change_presence(game=discord.Game(name= str("BMN 2019"),  url="https://twitch.tv/Batsphemy", type=1))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    args = message.content.split(" ")

    if args[0].upper() == "ADDSONG":

        d = int(args[1])
        h = (int(args[2]) - 1)%24
        if h == 23:
            d -= 1
        songname = " ".join(args[3:])

        now = datetime.utcnow()
        songTime = now.replace(hour=h, day=d)

        Songs[songTime] = songname
        print(Songs)
        with open("SongDict", "wb") as save:
            pickle.dump(Songs, save)

    if message.channel.id == "500627829474459669":
        msg = message.content
        msg = msg.replace('*', '')

        await client.delete_message(message)
        await client.send_message(message.channel, "***" + msg + "*** :bewust: - " + message.author.nick)


client.loop.create_task(checkSongs())
client.run("NTAwNjI4NTQ4NTE2NzA4MzUy.DqNmTw.-W1gtIDkqjaKxQkW4zeRLP-uVmw")
