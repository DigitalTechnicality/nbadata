import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 1000)

df = pd.read_csv('nbastats.csv')

dict = df.game_id.unique()

##This works for iterating through games
for game in dict:
    s = df.loc[df.game_id == game]
    #print(s)
    #print('Fin')

#print(df.head())

df_scores = df[['away_score', 'home_score']]


#print(df_scores.head())

df_d = df[['game_id', 'team', 'result', 'shot_distance']]

df_s = df_d.loc[df_d['game_id'] == dict[0]]

#print(df_shotdistance.head())

x = df_s.dropna()

#print(x.head())

##will need to create new column with 3pt %, track turnovers
##features vs target... features will be 3pt%, turnovers, players,  free throws, shot distance, score, rebounds, layups
##target will be score 20% of the game ahead up until the end of the game
##make a column score difference

w = x[x.team == 'BOS']

z = w[w.shot_distance >= 22]

#print(w.head())

#print(df_s.head())

df_s['makes'] = df_s['result']
df_s['misses'] = df_s['result']

df_s.loc[(df_s['team'] == 'BOS') & (df_s['shot_distance'] >= 23) & (df_s['result'] == 'made'), 'makes'] = 1
df_s.loc[(df_s['team'] != 'BOS') | (df_s['shot_distance'] < 23) | (df_s['result'] == 'missed') | (df_s['makes'] == 'made'), 'makes'] = 0
df_s.fillna(0, inplace=True)

df_s.loc[(df_s['team'] == 'BOS') & (df_s['shot_distance'] >= 23) & (df_s['result'] == 'missed'), 'misses'] = 1
df_s.loc[(df_s['team'] != 'BOS') | (df_s['shot_distance'] < 23) | (df_s['result'] == 'made'), 'misses'] = 0
df_s.fillna(0, inplace=True)

df_s['makes'] = df_s['makes'].cumsum()
df_s['misses'] = df_s['misses'].cumsum()
df_s['Three_Pct'] = (df_s['makes'])/((df_s['makes']+df_s['misses']))

#df_s['Bos_Threes'] = (df_s['makes'])/(((df_s['makes'])+(df_s['misses'])))
#df_s['Bos_Threes'] = df_s.loc[[(df_s['team'] == 'BOS') & (df_s['shot_distance'] >= 23)]]


#df_s['Boston_Shots'] = np.where(df_s.team == 'BOS', df_s.result, 0)
#df_s['Boston_Threes'] = np.where(df_s.Boston_Shots >= '23', df_s.result, 0)
#df_s['Boston_Threes_Made'] = np.where(df_s.Boston_Threes == 'made', 1, 0).cumsum()
#df_s['Boston_Threes_Missed'] = np.where(df_s.Boston_Threes == 'missed', 1, 0).cumsum()
#df_s['Bos3pct'] = (df_s['Boston_Threes_Made'])/((df_s['Boston_Threes_Made']+df_s['Boston_Threes_Missed']))
#df_s['makes_misses'] = df_s.loc[df.result == 'made', 'makes_misses'] = 1
#df_s['make_misses'] = df_s.loc[df.result == 'missed', 'makes_misses'] = 0

#can try match or contain
#df_shotdistance['makes_misses'] = df_shotdistance.loc[df_shotdistance.makes_misses == False, 'makes_misses'] = 0
#df.loc(df_shotdistance.result = 'made') = 0

#iloc=integer location, thats why the i
#df[(df.Sex == 'female') | (df.iloc[:,2] == 1) ].iloc[:3]

def get_pct(column):
    a = 0
    b=0
    for a in column:
        a += a
    for b in column:
        b += b
    for row in column:
        pct = a/(a+b)
    return pct



bos_made = z[z.result == 'made']
bos_missed = z[z.result == 'missed']


print(df_s)



#print(bos_made.count())
#print(bos_missed.count())
