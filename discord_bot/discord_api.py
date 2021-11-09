import os
import requests
from dotenv import load_dotenv

import discord
from discord.ext import commands
from requests.api import request


# STATIC VALUES
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
AUCTION_CHANNEL_ID = int(os.getenv('AUCTION_CHANNEL_ID'))
COMMAND_PREFIX = '.'
BASE_URL = 'http://127.0.0.1:8001/api/v1/auction'


# logging setting
# import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)


# methods
def get_player_id_by_name(player_name):
    # player 리스트 가져오기
    list_players_url = BASE_URL + '/players'
    res = requests.get(list_players_url)

    # player_id와 함께 리턴할 메세지
    msg = ''

    # 리스트 가져오는 과정에 오류 발생 시 리턴
    if res.status_code != 200:
        player_id = -1
        msg = f'{res.status_code} / 플레이어 리스트를 불러오는 도중 오류가 발생했습니다.'
        return (player_id, msg)

    # 리스트에서 player_name과 같은 이름을 가진 player 찾기
    players = res.json()

    player_id = -1

    for player in players:
        if player['name'] == player_name:
            player_id = player['id']
            break
    
    # 해당 player_name을 가진 player가 존재하지 않을 시
    if player_id < 0:
        msg = f'플레이어 목록에 해당 아이디를 가진 플레이어가 없습니다: {player_name}.'
        return (player_id, msg)
    
    msg = '성공!'
    return (player_id, msg)

    
def get_or_create_player_id_by_name(player_name):
    # player_name을 이용해 player_id 가져오기
    player_id, msg = get_player_id_by_name(player_name)

    # 해당 plyaer_name을 가진 player가 존재하지 않으면 새로 생성
    if player_id < 0:
        create_player_url = BASE_URL + '/players'
        data = {
            'name': player_name,
        }
        res = requests.post(create_player_url, data)

        # player를 생성하는 과정에서 오류 발생 시 리턴
        if res.status_code != 200:
            player_id = -1
            msg = f'{res.status_code} / 플레이어를 생성하는 도중 오류가 발생했습니다.'
            return (player_id, msg)
        
        # 생성된 player의 id 가져오기
        player_id = res.json()['id']
    
    # player_id와 성공 status_code 리턴
    return (player_id, msg)


def get_item_id_by_name(reg_player_id, item_name):
    # item 리스트 가져오기
    list_items_url = BASE_URL + '/items'
    res = requests.get(list_items_url)

    # item_id와 함께 리턴할 메세지
    msg = ''

    # 리스트 가져오는 과정에 오류 발생 시 리턴
    if res.status_code != 200:
        item_id = -2
        msg = f'{res.status_code} / 아이템 리스트를 불러오는 도중 오류가 발생했습니다.'
        return (item_id, msg)

    # 리스트에서 item_name과 같은 name을 가진 item 찾기
    items = res.json()

    item_id = -1

    for item in items:
        if item['reg_player'] != reg_player_id:
            continue

        if item['name'] == item_name:
            item_id = item['id']
            break
    
    # 리스트에 해당 이름을 가진 item이 없을 시
    if item_id < 0:
        msg = f'목록에 해당 아이템이 없습니다: {item_name}'
        return (item_id, msg)

    msg = '성공!'
    return (item_id, msg)


# classes
class Auction:
    # 도움말 출력
    @staticmethod
    def help():
        script = "```markdown\n"\
            "# 명령어 목록\n\n"\
            ".목록 : 현재 등록된 물품 보기\n\n"\
            ".초기화 : 목록 초기화\n\n"\
            ".등록 <물품이름> : 물품을 옥션에 등록한다.\n\n"\
            ".등록취소 <물품이름> : 물품 등록을 취소한다.(등록자만 가능)\n\n"\
            ".입찰 <등록자 아이디> <물품이름> : 해당 물품에 입찰한다.\n\n"\
            ".입찰취소 <등록자 아이디> <물품이름> : 해당 입찰을 취소한다.\n\n"\
            "```"
        return script


    # 거래소 목록 조회
    @staticmethod
    def list_items():
        # 플레이어 리스트 가져오기
        list_players_url = BASE_URL + '/players'
        res = requests.get(list_players_url)
        if res.status_code != 200:
            return res.status_code

        players = res.json()
        
        # 출력문 작성
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
                
                script += f"\n"

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

        script = "```markdown\n"\
            f"'{player_name}'님이 목록을 초기화하였습니다.\n```"
        return script


    # 물품 등록
    @staticmethod
    def reg_item(player_name, item_name):
        # player_name을 이용하여 id 가져오기
        player_id, msg = get_or_create_player_id_by_name(player_name)

        # 가져오는 과정에 오류 발생 시 오류메세지 출력
        if player_id < 0:
            return msg
        
        # id를 이용해 아이템 등록하기
        create_item_url = f'{BASE_URL}/players/{player_id}/items'
        data = {
            'name': item_name,
        }
        res = requests.post(create_item_url, data)

        # 아이템 등록 실패 시
        if res.status_code != 200:
            return f'{res.status_code} / 아이템을 등록하는 도중 오류가 발생했습니다.'
        
        # 출력문 작성
        script = "```markdown\n"\
            f"'{player_name}'님이 물품을 등록하였습니다: {item_name}\n"\
            "```"
        return script

    
    # 물품 등록 취소
    @staticmethod
    def del_item(player_name, item_name):
        script = "```markdown\n"

        # player_name 가져오기 실패 시
        player_id, msg = get_player_id_by_name(player_name)
        if player_id < 0:
            script += (msg + "\n```")
            return script
        
        # item_id 가져오기 실패 시
        item_id, msg = get_item_id_by_name(player_id, item_name)
        if item_id < 0:
            script += (msg + "\n```")
            return script
        
        # 물픔 등록 삭제 요청
        delete_item_url = BASE_URL + f'/players/{player_id}/items/{item_id}'
        res = requests.delete(delete_item_url)

        if res.status_code == 403:
            script += "아이템의 등록자만 취소할 수 있습니다.\n```"
            return script
        elif res.status_code != 204:
            script += "아이템 등록을 취소하는 도중 오류가 발생했습니다.\n```"
            return script
        
        script += f"'{player_name}'님이 물품 등록을 취소하였습니다: {item_name}\n```"
        return script


    # 입찰
    @staticmethod
    def bid(player_name, reg_player_name, item_name):
        script = "```markdown\n"

        player_id, msg = get_player_id_by_name(player_name)
        if player_id < 0:
            script += (msg + "\n```")
            return script
        
        reg_player_id, msg = get_player_id_by_name(reg_player_name)
        if reg_player_id < 0:
            script += (msg + "\n```")
            return script
        
        item_id, msg = get_item_id_by_name(reg_player_id, item_name)
        if item_id < 0:
            script += (msg + "\n```")
            return script
        
        get_reg_player_url = BASE_URL + f'/players/{reg_player_id}'
        res = requests.get(get_reg_player_url)

        if res.status_code != 200:
            script += f"플레이어 정보를 불러오는 도중 문제가 발생했습니다: {reg_player_name}"
            return script
        
        reg_player = res.json()
        flag = False
        for reg_item in reg_player['reg_items']:
            if reg_item['id'] == item_id:
                for bidder in reg_item['bidders']:
                    if bidder['id'] == player_id:
                        script += f"'{player_name}'님은 이미 이 아이템에 입찰하셨습니다: {item_name}\n```"
                        return script
                flag = True

        if flag:
            bid_url = BASE_URL + f'/players/{player_id}/bid/{item_id}'
            res = requests.post(bid_url)
            
            if res.status_code == 201:
                script += f"'{player_name}'님이 입찰하였습니다: {reg_player_name} - {item_name}\n```"
                return script
            else:
                script += f"{res.status_code} / 입찰을 진행하는 도중 알 수 없는 오류가 발생하였습니다.\n```"

        script += f"{res.status_code} / 알 수 없는 오류가 발생하였습니다.\n```"
        return script


    # 입찰 삭제
    @staticmethod
    def unbid(player_name, reg_player_name, item_name):
        script = "```markdown\n"

        player_id, msg = get_player_id_by_name(player_name)
        if player_id < 0:
            script += (msg + "\n```")
            return script
        
        reg_player_id, msg = get_player_id_by_name(reg_player_name)
        if reg_player_id < 0:
            script += (msg + "\n```")
            return script
        
        item_id, msg = get_item_id_by_name(reg_player_id, item_name)
        if item_id < 0:
            script += (msg + "\n```")
            return script
        
        get_reg_player_url = BASE_URL + f'/players/{reg_player_id}'
        res = requests.get(get_reg_player_url)

        if res.status_code != 200:
            script += f"플레이어 정보를 불러오는 도중 문제가 발생했습니다: {reg_player_name}\n```"
            return script
        
        reg_player = res.json()
        flag = False
        for reg_item in reg_player['reg_items']:
            if reg_item['id'] == item_id:
                for bidder in reg_item['bidders']:
                    if bidder['id'] == player_id:
                        flag = True
                        break
                if flag:
                    break
                else:
                    script += f"'{player_name}'님은 이 아이템의 입찰 목록에 없습니다.: {item_name}\n```"
                    return script

        if flag:
            bid_url = BASE_URL + f'/players/{player_id}/bid/{item_id}'
            res = requests.post(bid_url)
            
            if res.status_code == 204:
                script += f"'{player_name}'님이 입찰을 취소하였습니다: {reg_player_name} - {item_name}\n```"
                return script
            else:
                script += f"{res.status_code} / 입찰을 진행하는 도중 알 수 없는 오류가 발생하였습니다.\n```"

        script += f"{res.status_code} / 알 수 없는 오류가 발생하였습니다.\n```"
        return script




# bot
bot = commands.Bot(command_prefix='.')


# commands
@bot.command(aliases=['도움말'])
async def help2(ctx):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        res = Auction.help()
        await ctx.send(res)


@bot.command(aliases=['목록'])
async def list(ctx):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        res = Auction.list_items()
        await ctx.send(res)
        

@bot.command(aliases=['초기화'])
async def clear(ctx):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        player_name = f'{ctx.author.name}#{ctx.author.discriminator}'
        res = Auction.clear(player_name)
        await ctx.send(res)


@bot.command(aliases=['등록'])
async def reg_item(ctx, item_name):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        player_name = f'{ctx.author.name}#{ctx.author.discriminator}'
        res = Auction.reg_item(player_name, item_name)
        await ctx.send(res)


@bot.command(aliases=['등록취소'])
async def del_item(ctx, item_name):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        player_name = f'{ctx.author.name}#{ctx.author.discriminator}'
        res = Auction.del_item(player_name, item_name)
        await ctx.send(res)


@bot.command(aliases=['입찰'])
async def bid(ctx, reg_player_name, item_name):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        player_name = f'{ctx.author.name}#{ctx.author.discriminator}'
        res = Auction.bid(player_name, reg_player_name, item_name)
        await ctx.send(res)


@bot.command(aliases=['입찰취소'])
async def unbid(ctx, reg_player_name, item_name):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        player_name = f'{ctx.author.name}#{ctx.author.discriminator}'
        res = Auction.unbid(player_name, reg_player_name, item_name)
        await ctx.send(res)


@bot.command(aliases=['테스트'])
async def test(ctx):
    if ctx.channel.id == AUCTION_CHANNEL_ID:
        res = f'{ctx.author.name}#{ctx.author.discriminator}'
        await ctx.send(res)


# run
bot.run(DISCORD_BOT_TOKEN)
