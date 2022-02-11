from SearchTool import search,to_csv

'''
class AllData():
  def __init__(self):
    self.all_player_data,self.all_name_player_data = self.table_maker()
  def table_maker():
    text = search("https://pleagueofficial.com/stat_player").select('tr')
    text = [t.text.replace(' ', '').replace(
        '\n', ' ').replace('%', '').split() for t in text]
    link = search(
        'https://pleagueofficial.com/stat_player').select('tr > th > a')
    link = ['https://pleagueofficial.com' + i['href'] for i in link]
    link.insert(0, '球員連結')
    for i in range(len(text)):
        text[i].append(link[i])

    d = {text[0][i]: [text[j][i] for j in range(1, len(text))] for i in range(len(text[0]))}
    nd = {text[i][0]: dict(zip(text[0], text[i])) for i in range(1, len(text))}

    return d, nd

  def OutputToCsv(self):
     to_csv('全球員賽季數據.csv', pd.DataFrame(self.all_player_data), 'Data', '全數據')
     to_csv('全球員賽季數據(姓名)).csv', pd.DataFrame(self.all_name_player_data), 'Data', '全數據')

print(AllData.all_player_data)
'''
