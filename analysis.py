import numpy as np
import pandas as pd
import sys
import os
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime


os.chdir('/Users/adam/PycharmProjects/nbadata/2018-2019_NBA_PbP_Logs')

x = 0


for file_names in os.listdir('/Users/adam/PycharmProjects/nbadata/2018-2019_NBA_PbP_Logs'):
    x += 1

#print("x equals: ", x)


def analyzeBoxScore(folder):
    sig_games = []
    num_files = 0
    for file_name in os.listdir(folder):
        try:
            df = pd.read_csv(file_name, error_bad_lines=False, encoding = "ISO-8859-1")
            #print(df.head(2))
            num_files += 1
            #print(num_files)
        #print(df) #this prints everything for some reason?
            new = df[['away_score', 'home_score']]
        #print(new) #this works also...
            new['difference'] = new['home_score']-new['away_score'] #was df['home_score]=df['away_score']
        #print(new) #this works too
            #y = 0
            for items in new['difference']:
                if abs(items) >= 10:
                    #if new['difference'].iloc[-1] < 10:   #1250 before adding the <10
                    sig_games.append(file_name)
                    #print(file_name)
                    #print(items)

                    #y += 1

                    break
                    #have to escape for loop
        except:
            print(file_name)

    #print(len(sig_games))
    return(sig_games)


lister = analyzeBoxScore('/Users/adam/PycharmProjects/nbadata/2018-2019_NBA_PbP_Logs')

def extra_analysis(listic):
    #list = analyzeBoxScore('/Users/adam/PycharmProjects/nbadata/2018-2019_NBA_PbP_Logs')
    #for x in list:
        #print(x) #this works

    most_sig_games = []

    for game in listic:
        df = pd.read_csv(game, error_bad_lines=False, encoding = "ISO-8859-1")
        new = df[['away_score', 'home_score']]
        # print(new) #this works also...
        new['difference'] = new['home_score']-new['away_score']

        #print(game)
        #print(new.head(10))

        home_instance = new.loc[abs(new['difference']) >= 10, 'home_score'].iloc[0]
        #print("hey")
        #print("hey :", home_instance) #doesn't get here
        away_instance = new.loc[abs(new['difference']) >= 10, 'away_score'].iloc[0]

        if home_instance > away_instance:
            place_holder = 1
        else:
            place_holder = 2

        final_home = new['home_score'].iloc[-1]
        final_away = new['away_score'].iloc[-1]

        if final_home > final_away:
            place_holder_two = 1
        else:
            place_holder_two = 2

        if place_holder != place_holder_two:
            most_sig_games.append(game)

    #print(len(most_sig_games))
    return most_sig_games





games = extra_analysis(listic=lister)
print(len(games))
for game in games:
    print(game)



# def graph_it(gamez):
#     dates = []
#     for game in gamez:
#         df = pd.read_csv(game, error_bad_lines=False, encoding="ISO-8859-1")
#         new = df[['away_score', 'home_score', 'date']]
#         #new['date'] = pd.to_datetime(new['date']).dt.normalize()
#         new['date'] = pd.to_datetime(new['date'])
#
#         game_date = new['date'].iloc[0]
#         dates.append(game_date)
#
#     counts = Counter(dates)
#     D = dict(Counter(dates))
#
#     F = sorted(D.items(), reverse=False)
#
#     plt.bar(*zip(*F))F
    #months = ['november', 'december','january', 'february', 'march', 'april', 'may', 'june']
    #plt.xticks(range(len(months)), months)
    #plt.show()



    #print(d)
    #new_ticks = len(D) / 8
    #rounded = round(new_ticks)
    #plt.bar(range(len(F)), F.values(), align='center')
    #new_ticks = len(D) / 10
    #rounded = round(new_ticks)
    #date_keys = list(F.keys())

    #plt.xticks(range(len(F)), date_keys)

    #plt.show()
    #for date in dates:
        #print(date)

#graph_it(games)

def identify_winning_team(frame):
        #print(frame)
        #df.drop(["game_id", "data_set", "original_x", "original_y", "converted_x", "converted_y"], axis=1, inplace=True)
        #print(frame.head(2))
        home_final = frame['home_score'].iloc[-1]
        away_final = frame['away_score'].iloc[-1]

        if home_final > away_final:
            return 1
        else:
            return 2


def identify_max_difference(framer):

    #return framer.loc[framer['score_difference'].idxmax()] -> this returns like every single value
    #return framer.iloc[framer['score_difference'].idxmax()]
    return framer['score_difference'].argmax()
    #framer[framer['score_difference'] == framer['score_difference'].max()]

def team_names(file_names):
    team_dict = {}
    for file in file_names:

        teams = file[-11:-4]
        teams.split('@')
        home_team = teams[0]
        away_team = teams[1]
        df = pd.read_csv(file, error_bad_lines=False, encoding="ISO-8859-1")
        df.drop(["game_id", "data_set", "original_x", "original_y", "converted_x", "converted_y"], axis=1, inplace=True)
        #okay so we know the home team and away team id...



        df['makes_home'] = df['result']
        df['misses_home'] = df['result']

        mask1 = df['team'] == home_team
        mask2 = df['shot_distance'] >= 23
        mask3 = df['result'] == 'made'

        df.loc[(mask1 & mask2 & mask3), 'makes_home'] = 1
        df.loc[(~mask1 | ~mask2 | ~mask3), 'makes_home'] = 0
        df.fillna(0, inplace=True)

        mask4 = df['team'] == home_team
        mask5 = df['shot_distance'] >= 23
        mask6 = df['result'] == 'missed'

        df.loc[(mask4 & mask5 & mask6), 'misses_home'] = 1
        df.loc[(~mask4 | ~mask5 | ~mask6), 'misses_home'] = 0
        df.fillna(0, inplace=True)

        df['makes_away'] = df['result']
        df['misses_away'] = df['result']

        mask11 = df['team'] == away_team
        mask22 = df['shot_distance'] >= 23
        mask33 = df['result'] == 'made'

        df.loc[(mask11 & mask22 & mask33), 'makes_away'] = 1
        df.loc[(~mask11 | ~mask22 | ~mask33), 'makes_away'] = 0
        df.fillna(0, inplace=True)

        mask44 = df['team'] == away_team
        mask55 = df['shot_distance'] >= 23
        mask66 = df['result'] == 'missed'

        df.loc[(mask44 & mask55 & mask66), 'misses_away'] = 1
        df.loc[(~mask44 | ~mask55 | ~mask66), 'misses_away'] = 0
        df.fillna(0, inplace=True)

        df['makes_home'] = df['makes_home'].cumsum()
        df['misses_home'] = df['misses_home'].cumsum()
        df['Three_Pct_Home'] = (df['makes_home']) / ((df['makes_home'] + df['misses_home']))



        df['makes_away'] = df['makes_away'].cumsum()
        df['misses_away'] = df['misses_away'].cumsum()
        df['Three_Pct_Away'] = (df['makes_away']) / ((df['makes_away'] + df['misses_away']))

        df['team_assists'] = df['assist']
        mask7 = df['team'] == home_team
        maskNA = df['assist'] != 'NaN'
        df.loc[(mask7 & maskNA), 'team_assists'] = home_team

        mask8 = df['team'] == away_team
        df.loc[(mask8 & maskNA), 'team_assists'] = away_team
        mask9 = df['team_assists'].isna()
        df.loc[df['assist'].isnull(), 'team_assists'] = 0

        df['home_assists'] = df['team_assists']
        df['away_assists'] = df['team_assists']

        mask_hassist = df['home_assists'] == home_team
        mask_hassists2 = df['home_assists'] != home_team
        mask_awassist = df['away_assists'] == away_team
        mask_awassists2 = df['away_assists'] != away_team
        df.loc[(mask_hassist), 'home_assists'] = 1
        df.loc[(mask_awassist), 'away_assists'] = 1
        df.loc[(mask_hassist), 'home_assists'] = 1
        df.loc[(mask_awassist), 'away_assists'] = 1

        df['score_difference'] = abs(df['home_score'] - df['away_score'])



        max_difference = identify_max_difference(df)

        # when you run this -> print(max_difference) you get 'None' lmao, so here's an issue

        #print(max_difference) -> seems to work now

        before_comeback = df.loc[:max_difference]



        #so we have a few issues here... first before_comeback is the same as df
        #second we're still getting some games where it is a blowout

        if identify_winning_team(df) == 1:
            #home_team won
            #winning_team = home_team
            #change columns to winning team and losing team
            df.rename(columns={'Three_Pct_Home': 'Three_Pct_Winner', 'Three_Pct_Away': 'Three_Pct_Loser', 'home_assists': 'Assists_Winner', 'away_assists': 'Assists_Loser'}, inplace=True)
        else:
            df.rename(columns={'Three_Pct_Home': 'Three_Pct_Loser', 'Three_Pct_Away': 'Three_Pct_Winner', 'home_assists': 'Assists_Loser', 'away_assists': 'Assists_Winner'}, inplace=True)
            #winning_team = away_team
            #change columns to winning team and losing team

        #print(df.head(2))

#team_names(games)
