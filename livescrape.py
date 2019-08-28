import requests
import pandas as pd
from pandas.io.json import json_normalize
import json

game = 'https://stats.nba.com/stats/playbyplayv2?EndPeriod=10&EndRange=55800&GameID=0021800549&RangeType=2&Season=2018-19&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
r = requests.get(game, headers=headers, timeout=10)
#Sometimes you have to make the user agent "more human" by adding headers like
#headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

#For some reason only r.text works, not r alone or r.json
mm = r.json()

lol = mm['resultSets'][0]['rowSet']

df = pd.DataFrame(lol)

col_names = mm['resultSets'][0]['headers']

#df.rename(columns={col_names})
df.set_axis(col_names, axis=1, inplace=True)

#hmm = json_normalize(lol)

#hmm.drop('name')

#print(x['resultSets'][0]['rowSet'])

print(df)

#df = pd.DataFrame()

#print(hmm)
