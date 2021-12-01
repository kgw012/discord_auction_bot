import requests

class Auction:
    def __init__(self, BASE_URL):
        self.BASE_URL = BASE_URL


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
    def list_players(self):
        url = self.BASE_URL + '/players'
        res = requests.get(url)
        players = res.json()

        script = "```md\n"
        for player in players:
            script += f"-{player['name']}-\n"

            for item in player['reg_items']:
                script += f"{item['seq_id']}) {item['name']}"

                if item['bidders']:
                    script += f" : {item['bidders'][0]['name']}"
                    for idx in range(1, len(item['bidders'])):
                        script += f", {item['bidders'][idx]['name']}"
                    script += f" 입찰희망!"

                script += f"\n"
            script += "\n"
        script += "```"

        return script
    