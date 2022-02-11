from PyPPlus.SearchTool import search, to_csv, all_name_player_data
from PyPPlus import *


class Player:
    def __init__(self, name):
        self.sign = True
        self.name = name
        self.link = all_name_player_data[self.name]['球員連結']
        #self.detail = self.init_detail()
        self.GameData = all_name_player_data[self.name]
        self.GameTable = self.gametable()

    def init_detail(self):
        home_url = 'https://pleagueofficial.com/'
        r = requests.get(self.link)
        r.encoding = "utf-8"
        if r.url == home_url:
            self.sign = False
            print(f'{self.name} 登出\n')
            return None
        else:
            soup = search(self.link)
            detail = soup.select('section')[0].text
            #print(player_detail)
            try:
                player_detail = {}
                player_detail['中文名字'] = (self.name)
                player_detail['英文名字'] = re.search(r'\n(([A-Z\-\s]\w+)+, [A-Z\-\s]\w+|[A-Z][a-z]+ [A-Z][a-z]+)\n', detail).group(1)
                self.EnName = player_detail['英文名字']
                player_detail['球隊'] = all_name_player_data[self.name]['球隊']
                self.team = player_detail['球隊']
                player_detail['背號'] = all_name_player_data[self.name]['背號']
                self.jersey = player_detail['背號']
                player_detail['位置'] = re.search(r"位置\n([A-Z\/]+)", detail).group(1)
                self.place = player_detail['位置']
                player_detail['身高(cm)'] = re.search(r'(\d+) cm', detail).group(1)
                self.hights = player_detail['身高(cm)']
                player_detail['體重(kg)'] = re.search(r'(\d+) kg', detail).group(1)
                self.weights = player_detail['體重(kg)']
                player_detail['生日'] = re.search(r'\d{4}-\d{2}-\d{2}', detail).group()
                self.birthday = player_detail['生日']
                print(f'{self.name} 創建完畢\n')
            except:
                print(f'{self.name} detail wrong')
        return player_detail

    # def player_game():
    def gametable(self):
        if not self.sign: return None
        soup = search(self.link)
        detail = soup.select('tr')
        gamedata = detail[5:len(detail) - 4]
        # print(gamedata)
        title = gamedata[0].text.strip().replace(' ', '')
        title = title.split('\n')
        # print(title)
        table = []
        for i in range(1, len(gamedata)):
            t = gamedata[i].text.strip().replace(' ', '')
            t = t.split('\n')
            while '' in t:
                t.remove('')
            table.append(t)
            # print(t)
        game_table = {title[i]: [t[i] for t in table] for i in range(len(title))}
        t = soup.select('#away_table > tbody > tr > td > a')
        game_table['勝負'] = [re.search(r'(W|L)', i).group(1) for i in game_table['分數']]
        game_table['比賽編號'] = [int(re.search(r'/game/([0-9]+)', i['href']).group(1)) - 12 for i in t]
        game_table['主/客場'] = ['Home' if re.search(r'[0-9]+-[0-9]+(W|L)', t) else 'Away' for t in game_table['分數']]
        return game_table

    def showdetail(self):
        try:
            for k, v in self.detail.items():
                print(f'{k}  :  {v}')
            print('')
        except:
            print(f'{self.name} 已登出\n')

    def showdata(self):
        if self.sign:
            print(f'{self.name}本賽季數據')
        else:
            print(f'{self.name}本賽季數據（已登出）')
        for k, v in self.GameData.items():
            print(f'{k}  :  {v}')
        print('')


if __name__ == '__main__':
    player4 = Player('高國豪')

