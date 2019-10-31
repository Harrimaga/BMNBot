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

with open("BMNQuotes", "wb") as out_quotes:
    pickle.dump(Quotes, out_quotes)

with open("BMNInfo", "wb") as out_quotes:
    pickle.dump(Info, out_quotes)

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


@client.command(name='AddQuote')
@is_quote_master()
async def _addQuote(context, *args):
    quote = " ".join(args)
    Quotes.append(quote)
    await context.message.add_reaction("👍")
    with open("BMNQuotes", "wb") as out_quotes:
        pickle.dump(Quotes, out_quotes)

@client.command(name='Quote')
@commands.has_any_role(618181358594031616, 619144995726950444)
async def _quote(context, *args):
    await context.message.channel.send(random.choice(Quotes))


client.run("NTAwNjI4NTQ4NTE2NzA4MzUy.Xbr9WA.owlUTYMJQmqSjIo6KEIRwnbvmtk")