import discord
from discord.ext import commands

class Auction:
    def __init__(self):
        self.auction_dict = dict()
        

BOT_TOKEN = 'OTA1MDM1ODc3MDYxODkwMDg4.YYEOVw.arwSm9aqVTIVU2xtsvTzanBo7KE'

bot = commands.Bot(command_prefix='.')

@bot.command()
async def 핑(ctx):
    await ctx.send('pong')

bot.run(BOT_TOKEN)