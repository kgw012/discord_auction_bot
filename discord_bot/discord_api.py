import os
import requests
from dotenv import load_dotenv

import discord
from discord.ext import commands


# STATIC VALUES
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
AUCTION_CHANNEL_ID = int(os.getenv('AUCTION_CHANNEL_ID'))
COMMAND_PREFIX = '.'
BASE_URL = 'http://127.0.0.1:8000/api/v1/auction'


# logging setting
# import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)


# classes
class Auction:
    # 거래소 목록 조회
    @staticmethod
    def list_items():
        list_players_url = BASE_URL + '/players'
        res = requests.get(list_players_url)
        if res.status_code != 200:
            return res.status_code

        players = res.json()
        

        script = "```markdown\n"\
            "# 목록 보기\n\n"

        for player in players:
            items = player['reg_items']

            if not items:
                continue
            
            script += f"-{player['name']}-\n"
            for item in items:
                script += f"{item['name']}"

                bidders = item['bidders']

                if not bidders:
                    script += "\n"
                    continue
                
                script += " : "
                for bidder in bidders:
                    script += f"{bidder['name']} "
                
                script += f"입찰희망\n"

            script += "\n"

        script += "```"
        return script


    # 거래소 목록 초기화
    @staticmethod
    def clear(player_name):
        url = BASE_URL + '/clear'
        res = requests.delete(url)
        if res.status_code != 204:
            return res.status_code

        script = f"'{player_name}'님이 목록을 초기화하였습니다."
        return script


    # 물품 등록
    @staticmethod
    def reg_item(player_name, item_name):
        pass
    
    # 물품 등록 삭제
    @staticmethod
    def del_item(player_name, item_name):
        pass

    # 입찰
    @staticmethod
    def bid(player_name, reg_author, item_name):
        pass

    # 입찰 삭제
    @staticmethod
    def unbid(player_name, reg_author, item_name):
        pass


# bot
bot = commands.Bot(command_prefix='.')


# commands
@bot.command(aliases=['목록'])
async def list(ctx):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        res = Auction.list_items()
        await ctx.send(res)
        

@bot.command(aliases=['초기화'])
async def clear(ctx):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        if ctx.message != '.초기화':
            await ctx.send('올바르지 않은 입력입니다.')
        else:
            player_name = f'{ctx.author.name}#{ctx.author.discriminator}'
            res = Auction.clear(player_name)
            await ctx.send(res)


@bot.command(aliases=['등록'])
async def reg_item(ctx, item_name):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        player_name = f'{ctx.author.name}#{ctx.author.discriminator}'
        res = Auction.reg_item(player_name, item_name)
        await ctx.send(res)


@bot.command(aliases=['테스트'])
async def test(ctx):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        res = f'{ctx.author.name}#{ctx.author.discriminator}'
        await ctx.send(res)


# run
bot.run(DISCORD_BOT_TOKEN)
