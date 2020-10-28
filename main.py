import discord
from discord.ext.commands import Bot
from discord.ext import tasks, commands
import pickle
import random
import gspread
import re
import pytz
import datetime
from datetime import timedelta
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('BMNBot.json', scope)
gc = gspread.authorize(credentials)

Client = discord.Client()
client = commands.Bot(command_prefix = "!")

names = ["GlockenSpiel", "Kalimba", "Ukulele", "Kazoo", "Ocarina", "Toetsen", "Coolere", "Pauken", "SymfonieOrkest", "Xylofoon", "Vibrafoon", "Sitar", "Theremin", "Hydrolauphone", "Thoramin", "Aartsluit", "Accordeon", "Altblokfluit", "Altklarinet", "Autoharp", "Aulos", "Balalaika", "Bamboefluit", "Bandoneon", "Baritonsaxofoon", "Blaas-bas", "Buffetpiano", "Cajón", "Castagnetten", "Clavicytherium", "Cobza", "Cornetto", "Didgeridoo", "Djembé", "Ektar", "Fagot", "Koebel", "Lamellofoon", "Lyricon", "Mirliton", "Psalterium", "Sambaballen", "Symphonetta", "Tinwhistle", "Torupill", "Virginaal", "Zingende kaars "]
B = ["Beuken", "Braken", "Boekenlezen", "Beroven", "Bestellen", "Babbelen", "Babysitten", "Backflippen", "Badderen", "Bakken", "Begluren", "Bankieren", "Barbecueën", "Barricaderen", "Beitelen", "Beatboxen", "Bedotten", "Beeldhouwen"]
N = ["Naaidozen", "Na-apers", "Naaktzwemmers", "Nationaliteitenproblemen", "Neanderthalers", "Nederwiet", "Napoleon", "Nijlpaarden", "Nummerherkenning"]

global Quotes
Quotes = []
global Info
Info = ""
global today
today = ""

with open("BMNQuotes", "rb") as in_quotes:
    Quotes = pickle.load(in_quotes)

with open("BMNInfo", "rb") as in_info:
    Info = pickle.load(in_info)

with open("BMNToday", "rb") as in_day:
    today = pickle.load(in_day)

def is_quote_master():
    async def predicate(ctx):
        return ctx.author.id == 260843280361586688
    return commands.check(predicate)

@tasks.loop(minutes=1.0)
async def Loop():
    global today
    tday = datetime.datetime.now(tz=pytz.timezone('Europe/Amsterdam'))
    channel = client.get_channel(632950303968329728)
    if tday.day != today.day:
        Server = client.get_guild(500419426974302220)
        Batto = Server.get_member(260843280361586688)
        await Batto.edit(nick=random.choice(names) + "Tim")
        gc = gspread.authorize(credentials)
        sheetVerjaardag = gc.open_by_url('https://docs.google.com/spreadsheets/d/1aUmCqRy_iUWkQzx1wWmWATi_U4Y1B7W-PqGQHE0dU3I/')
        verjaardagsheet = sheetVerjaardag.get_worksheet(1)
        dag_re = re.compile((r'{}-{}-[0-9]*').format(tday.day, tday.month))
        print((r'{}-{}-[0-9]*').format(tday.day, tday.month), flush = True)
        cell_list = verjaardagsheet.findall(dag_re)
        print(cell_list)
        for cell in cell_list:
            val = cell.val
            if val.startswith(tday.day):
                row = cell.row
                col = cell.col
                await channel.send(content=verjaardagsheet.cell(row, col-2).value + " is vandaag jarig!")
        today = tday
        with open("BMNToday", "wb") as out_day:
            pickle.dump(today, out_day)
    #values_list = verjaardagSheet.row_values(1)
    #print(values_list)

@tasks.loop(minutes=1.0)
async def CheckTop():
    gc = gspread.authorize(credentials)
    sheet = gc.open('Top2000')
    worksheet = sheet.get_worksheet(0)
    channel = client.get_channel(626533887690145813)
    tday = datetime.datetime.now(tz=pytz.timezone('Europe/Amsterdam'))
    cell_list = worksheet.findall(str(tday.day))
    print(tday)
    if len(cell_list) > 0:
        msg = "**BMN nummers dit uur in de Top 2000:**\n"
        for cell in cell_list:
            row = cell.row
            col = cell.col
            if col == 3 and worksheet.cell(row, col + 1).value != "Geweest!" and int(worksheet.cell(row, col + 1).value) == tday.hour:
                rowVals = worksheet.row_values(row)
                msg += rowVals[4] + ":\t" + rowVals[0] + " - " + rowVals[1] + "\n"
                worksheet.update_cell(row, col + 1, "Geweest!")
        if msg!= "**BMN nummers dit uur in de Top 2000:**\n":
            await channel.send(content=msg)

@Loop.before_loop
async def before_Loop():
    await client.wait_until_ready()

@Loop.after_loop
async def on_Loop_cancel():
    CheckTop.restart()

@client.event
async def on_ready():
    print("Ready!", flush = True)
    stream = discord.Activity(name="BMN 2020", url="https://betamusicnight.nl", type=discord.ActivityType.listening)
    await client.change_presence(activity=stream)
    Server = client.get_guild(500419426974302220)
    Batto = Server.get_member(260843280361586688)
    await Batto.edit(nick=random.choice(names) + "Tim")

@client.command(name='BMN')
async def _bmn(context, *args):
    bmn = random.choice(B) + " Met " + random.choice(N)
    await context.message.channel.send(bmn)

@client.command(name='AddQuote', hidden=True)
@is_quote_master()
async def _addQuote(context, *args):
    quote = " ".join(args)
    Quotes.append(quote)
    await context.message.add_reaction("👍")
    with open("BMNQuotes", "wb") as out_quotes:
        pickle.dump(Quotes, out_quotes)

@client.command(name='DelQuote', hidden=True)
@is_quote_master()
async def _delQuote(context, *args):
    await context.message.channel.send("Removed: " + Quotes.pop(int(args[0])))
    with open("BMNQuotes", "wb") as out_quotes:
        pickle.dump(Quotes, out_quotes)

@client.command(name='Quote', aliases=['quote'], help="Een random quote")
@commands.has_any_role(618181358594031616, 619144995726950444)
async def _quote(context, *args):
    quote = ""
    if len(args) > 0:
        q = []
        for quote in Quotes:
            if quote.endswith(args[0]):
                q.append(quote)
        if len(q) < 1:
            await context.message.channel.send(args[0] + " heeft geen quotes :(")
        quote = random.choice(q)
    else:
        quote = random.choice(Quotes)

    embed = discord.Embed(
        title = " ".join(quote.split()[:-1]),
        description = quote.split()[-1][1:],
        colour = discord.Colour(0x800020)
        )
    embed.set_thumbnail(url='https://cdn.discordapp.com/icons/500419426974302220/ccb477a3d8018f146a320bf3fa298445.webp?size=128')
    await context.message.channel.send(embed=embed)

@client.command(name='AllQuotes', aliases=['allquotes'], hidden=True)
@is_quote_master()
async def _allQuotes(context, *args):
    i = 0
    for quote in Quotes:
        await context.message.channel.send(str(i) + ": " + quote)
        i += 1

@client.command(name='SetInfo', hidden=True)
@commands.has_role(618181358594031616)
async def _setInfo(context):
    global Info
    Info = context.message.content[9:]
    await context.message.add_reaction("👍")
    print(context.message.content)
    with open("BMNInfo", "wb") as out_info:
        pickle.dump(Info, out_info)

@client.command(name='Info', aliases=['info'], help="Het laatste nieuws!")
@commands.has_any_role(618181358594031616, 619144995726950444)
async def _info(context):
    global Info
    await context.message.channel.send(Info)

Loop.start()
#CheckTop.start()
client.run("---")
