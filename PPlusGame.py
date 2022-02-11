import imp
import pandas as pd
from PyPPlus import *
from PyPPlus.SearchTool import search
from PyPPlus.SearchTool import player_on_game_keys as pk
from PyPPlus.SearchTool import team_on_game_keys as tk


class Game:
    def __init__(self, game_id, live=False):
        self.game_id = game_id
        self.api_url = "https://match.pleagueofficial.com/api/boxscore.php"
        self.game_url = f'https://match.pleagueofficial.com/game/{self.game_id}'
        self.game_type, self.session_id, self.home_team, self.away_team = self.game_detail()
        self.box_score = self.get_box_score()
        self.team_data = self.team_total_data()
        if not live:
            self.player_data = self.get_all_data('DataFrame')
    
    def __api_call(self,target):
         payload = {"id": f"{self.game_id}","away_tab": f"{target}","home_tab": f"{target}"}
         r = requests.get(self.api_url, params=payload)
         return r.json()['data']

    def get_all_data(self,type):
        keys = ['q1', 'q2', 'q3','q4','total']
        dict ={
            k : self.get_player_data(type,k) for k in keys
        }
        return dict
        
    def game_detail(self):
        r = requests.get(self.game_url)
        soup = BeautifulSoup(r.text, "lxml")
        title = soup.title.text
        title = title.split("│")[0]
        title = title.split(" ")
        game_type, game_session_id = title[0].split('G')
        home_team, away_team = title[1], title[3]
        return game_type, game_session_id, home_team, away_team
        # print(game_type, game_session_id, home_team, away_team)

    def get_box_score(self):
        data = self.__api_call('total')
        keys = ['q1','q2','q3','q4','ot1','ot2','score']
        box_score = {k: [data[f'{k}_home'], data[f'{k}_away']] for k in keys}
        s = {
            '主/客場': ('主場', '客場')
            # '球隊' : (self.home_team,self.away_team)
        }
        box_score = {**s, **box_score}
        return box_score
        
    def team_total_data(self):
        data = self.__api_call('total')
        a,h = data['away_total'],data['home_total']
        title = tk
        df = {}
        df['主客場'] = ['home', 'away']
        df['球隊'] = [self.home_team, self.away_team]
        df.update({title[k]: [h[k], a[k]] for k in title.keys()})
        return df
        
    def get_player_data(self, type,target):
        data = self.__api_call(target)
        title = pk
        if type == "DataFrame":
            h_dic = {title[key]: [p[key] for p in data['home']] for key in title.keys()}
            a_dic = {title[key]: [p[key] for p in data['away']] for key in title.keys()}
            h_dic['球隊'] = [self.home_team for i in range(len(h_dic['球員']))]
            h_dic['主場'] = ['主場' for i in range(len(h_dic['球員']))]
            a_dic['球隊'] = [self.away_team for i in range(len(h_dic['球員']))]
            a_dic['主場'] = ['客場' for i in range(len(h_dic['球員']))]
            return {'home': h_dic, 'away': a_dic}
        
        if type == "json_list":
            h_lis = [{title[key]: p[key] for key in title.keys()} for p in data['home'][target]]
            bonus = {'球隊': self.home_team,'主/客場': '主場','節次': target}
            home = [{**h_lis, **bonus} for l in h_lis]
            a_lis = [{title[key]: p[key] for key in title.keys()} for p in data['away'][target]]
            bonus = {'球隊': self.away_team,'主/客場': '客場','節次': target}
            away = [{**a_lis, **bonus} for l in a_lis]
            return {'home' :home,'away':away}

