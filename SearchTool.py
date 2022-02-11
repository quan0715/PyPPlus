# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import os
from PyNotion import *

player_on_game_keys = {
    'name_alt': '球員',
    'mins': '上場時間',
    'points': '得分',
    'reb': '籃板',
    'ast': '助攻',
    'blk': '阻攻',
    'stl': '抄截',
    'reb_d': '功板',
    'reb_o': '防板',
    'two_m_two': '兩分球',
    'twop': '兩分命中率',
    'trey_m_trey': '三分球',
    'treyp': '三分球命中率',
    'ft_m_ft': '罰球',
    'ftp': '罰球命中率',
    'pfoul': '犯規',
    'turnover': '失誤',
    'positive': '正負值',
    'eff': '效率值',
    'tsp': '真實命中率',
    'ugp': '球權佔有率',
    'efgp': '有效命中率'
}
team_on_game_keys = {
    'points': '得分',
    'reb': '籃板',
    'ast': '助攻',
    'blk': '阻攻',
    'stl': '抄截',
    'reb_d': '功板',
    'reb_o': '防板',
    'two': '兩分出手',
    'two_m': '兩分命中',
    'twop': '兩分命中率',
    'trey': '三分球出手',
    'trey_m': '三分命中',
    'treyp': '三分命中率',
    'ft': '罰球出手',
    'ft_m': '罰球命中',
    'ftp': '罰球命中率',
    'pfoul': '犯規',
    'turnover': '失誤',
    'positive' : '正負值'
}

def to_csv(filename, Data, foldername1=None, foldername2=None):
    now_path = os.getcwd()
    if foldername1:
        if not os.path.isdir(foldername1):
            os.mkdir(foldername1)
            print(f'資料夾 {foldername1} 創建成功')
        os.chdir(os.path.abspath(foldername1))
    if foldername2:
        if not os.path.isdir(foldername2):
            os.mkdir(foldername2)
            print(f'資料夾 {foldername2} 創建成功')
        os.chdir(os.path.abspath(foldername2))

    Data.to_csv(filename, index=True)
    print(f'{filename} 輸出成功')
    os.chdir(now_path)


def search(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "lxml")
    return soup



def get_players_data():
    text = search("https://pleagueofficial.com/stat_player").select('tr')
    text = [t.text.replace(' ', '').replace(
        '\n', ' ').replace('%', '').split() for t in text]
    link = search(
        'https://pleagueofficial.com/stat_player').select('tr > th > a')
    link = ['https://pleagueofficial.com' + i['href'] for i in link]
    link.insert(0, '球員連結')
    for i in range(len(text)):
        text[i].append(link[i])

    d = {text[0][i]: [text[j][i]
        for j in range(1, len(text))] for i in range(len(text[0]))}
    nd = {text[i][0]: dict(zip(text[0], text[i])) for i in range(1, len(text))}

    return d, nd

def OutputToCsv():
    to_csv('全球員賽季數據.csv', pd.DataFrame(all_player_data), 'Data', '全數據')
    to_csv('全球員賽季數據(姓名)).csv', pd.DataFrame(all_name_player_data), 'Data', '全數據')

all_player_data, all_name_player_data = get_players_data()
PlayerList = [name for name in all_name_player_data.keys()]

