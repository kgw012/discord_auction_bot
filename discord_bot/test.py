import requests

BASE_URL = 'http://127.0.0.1:8000/api/v1/auction'


script = "```markdown\n"\
    "# 명령어 목록\n\n"\
    ".목록 : 현재 등록된 물품 보기\n\n"\
    ".초기화 : 목록 초기화\n\n"\
    ".등록 <물품이름> : 물품을 옥션에 등록한다.\n\n"\
    ".등록취소 <물품이름> : 물품 등록을 취소한다.(등록자만 가능)\n\n"\
    ".입찰 <등록자 아이디> <물품이름> : 해당 물품에 입찰한다.\n\n"\
    ".입찰취소 <등록자 아이디> <물품이름> : 해당 입찰을 취소한다.\n\n"\
    "```"

url = BASE_URL + '/players'
res = requests.get(url)
items = res.json()

# script = "```md\n"
# for item in items:
#     item_script = f'{item.id} {}'

print(items)