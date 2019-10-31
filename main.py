import discord
from discord.ext.commands import Bot
from discord.ext import commands
import pickle
import random

Client = discord.Client()
client = commands.Bot(command_prefix = "!")

global Quotes
Quotes = []
global Info
Info = ""

with open("BMNQuotes", "rb") as in_quotes:
    Quotes = pickle.load(in_quotes)

with open("BMNInfo", "rb") as in_info:
    Info = pickle.load(in_info)

def is_quote_master():
    async def predicate(ctx):
        return ctx.author.id == 260843280361586688
    return commands.check(predicate)

@client.event
async def on_ready():
    print("Ready!")
    stream = discord.Activity(name="BMN 2020", url="https://betamusicnight.nl", type=discord.ActivityType.listening)
    await client.change_presence(activity=stream)

@client.command(name='AddQuote', hidden=True)
@is_quote_master()
async def _addQuote(context, *args):
    quote = " ".join(args)
    Quotes.append(quote)
    await context.message.add_reaction("👍")
    with open("BMNQuotes", "wb") as out_quotes:
        pickle.dump(Quotes, out_quotes)

@client.command(name='Quote', aliases=['quote'], help="Een random quote")
@commands.has_any_role(618181358594031616, 619144995726950444)
async def _quote(context, *args):
    await context.message.channel.send(random.choice(Quotes))

@client.command(name='SetInfo', hidden=True)
@commands.has_role(618181358594031616)
async def _setInfo(context):
    global Info
    Info = context.message.content[9:]
    print(context.message.content)
    with open("BMNInfo", "wb") as out_info:
        pickle.dump(Info, out_info)

@client.command(name='Info', aliases=['info'], help="Het laatste nieuws!")
@commands.has_any_role(618181358594031616, 619144995726950444)
async def _info(context):
    global Info
    await context.message.channel.send(Info)

client.run("NTAwNjI4NTQ4NTE2NzA4MzUy.XbsLQQ._r5tLlNg3xFwb3k-VbkYG2A7g08")