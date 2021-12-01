import os

from dotenv import load_dotenv
from discord.ext import commands

import auction as auction_module

# STATIC VALUES
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
AUCTION_CHANNEL_ID = int(os.getenv('AUCTION_CHANNEL_ID'))
COMMAND_PREFIX = '.'
BASE_URL = os.getenv('BASE_URL')


# logging setting
# import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)


# load Auction
auction = auction_module.Auction(BASE_URL=BASE_URL)

# bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


# commands
@bot.command(aliases=['도움말'])
async def help2(ctx):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        res = auction.help()
        await ctx.send(res)


@bot.command(aliases=['목록'])
async def list(ctx):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        res = auction.list_players()
        await ctx.send(res)
        

# run
bot.run(DISCORD_BOT_TOKEN)
