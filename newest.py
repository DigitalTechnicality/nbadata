import numpy as np
import pandas as pd
import sys
import os
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime #watch out for from datetime import date
import statistics






os.chdir('/Users/adam/PycharmProjects/nbadata/2018-2019_NBA_PbP_Logs')

x = 0


for file_names in os.listdir('/Users/adam/PycharmProjects/nbadata/2018-2019_NBA_PbP_Logs'):
    x += 1

print(x)

#print("x equals: ", x)

def identify_max_difference(framer):


    framer['score_difference'] = framer['score_difference'].abs()

    return framer['score_difference'].argmax()



def analyzeBoxScore(folder):
    sig_games = []
    num_files = 0
    for file_name in os.listdir(folder):

        try:
            df = pd.read_csv(file_name, error_bad_lines=False, encoding = "ISO-8859-1")

            num_files += 1

            new = df[['away_score', 'home_score']]

            new['score_difference'] = new['home_score']-new['away_score'] #was df['home_score]=df['away_score']

            max_difference = identify_max_difference(new)

            #print("The max difference is: ", + max_difference)

            max_score_difference = new['score_difference'].iloc[max_difference]

            final_score_difference = new['score_difference'].iloc[-1]



            if max_score_difference > 14:
                sig_games.append(file_name)


            #print(max_score_difference)

        except:
            print("This file didn't work: ", file_name)





    #print(len(sig_games))
    return(sig_games)


lister = analyzeBoxScore('/Users/adam/PycharmProjects/nbadata/2018-2019_NBA_PbP_Logs')

print(len(lister))

def extra_analysis(listic):


    most_sig_games = []
    least_sig_games = []

    for game in listic:
        df = pd.read_csv(game, error_bad_lines=False, encoding = "ISO-8859-1")
        new = df[['away_score', 'home_score']]

        new['score_difference'] = new['home_score']-new['away_score']

        max_difference = identify_max_difference(new)

        # print("The max difference is: ", + max_difference)

        max_score_difference = new['score_difference'].iloc[max_difference]

        final_score_difference = new['score_difference'].iloc[-1]

        home_instance = new['home_score'].iloc[max_difference]

        away_instance = new['away_score'].iloc[max_difference]


        #home_instance = new.loc[abs(new['difference']) >= 10, 'home_score'].iloc[0]



        #away_instance = new.loc[abs(new['difference']) >= 10, 'away_score'].iloc[0]

        if max_score_difference > 15:

            if home_instance > away_instance:
                #print(home_instance, away_instance)
                #HOME IS LEADING EARLY
                place_holder = 1
            else:
                #print(away_instance, home_instance)
                #AWAY IS LEADING EARLY
                place_holder = 2

            final_home = new['home_score'].iloc[-1]
            final_away = new['away_score'].iloc[-1]

            #if abs(new['difference'].iloc[-1] <=4:
                #close_game = True

            #if close_game = True:
                #most sig_games.append(game)



            if place_holder == 1:
                #home team was leading
                if final_home-final_away < 4:
                    most_sig_games.append(game)

                else:
                    least_sig_games.append(game)



            elif place_holder == 2:
                #away team was leading
                if final_away-final_home < 4:
                    most_sig_games.append(game)

                else:
                    least_sig_games.append(game)

        else:
            least_sig_games.append(game)




        #if place_holder != place_holder_two:
            #most_sig_games.append(game)






    #print(len(most_sig_games))
    return most_sig_games, least_sig_games





comeback_games, non_comeback_games = extra_analysis(listic=lister)

print(comeback_games)
print(len(comeback_games))
print(non_comeback_games)
print(len(non_comeback_games))



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

def after_all_star(games_list):
    after_all_star_group = []
    for game in games_list:
        df = pd.read_csv(game, error_bad_lines=False, encoding="ISO-8859-1")
        df['date'] = pd.to_datetime(df['date'])
        if df['date'].iloc[-1] > datetime.date(2019, 2, 15):
            if df['date'].iloc[-1] < datetime.date(2019, 4, 12):
                after_all_star_group.append(game)

    return after_all_star_group







def team_names(file_names):
    losing_3_list = []
    winning_3_list = []
    winning_3_totals = []
    losing_3_totals = []
    games_final = []
    winner_scores = []
    loser_scores = []
    winning_teams = []
    losing_teams = []
    winner_assists = []
    loser_assists = []
    final_winner_scores =[]
    final_loser_scores = []


    for file in file_names:

        teams = file[-11:-4]
        new_teams = teams.split('@')
        #print(teams)
        #print(new_teams)
        home_team = new_teams[0]
        away_team = new_teams[1]
        df = pd.read_csv(file, error_bad_lines=False, encoding="ISO-8859-1")
        df.drop(["game_id", "data_set", "original_x", "original_y", "converted_x", "converted_y"], axis=1, inplace=True)
        #okay so we know the home team and away team id...

        #print(home_team)
        #print(away_team)


        df['makes_home'] = df['result']
        df['misses_home'] = df['result']

        mask1 = df['team'] == home_team
        mask2 = df['shot_distance'] >= 23
        mask3 = df['result'] == 'made'

        #print(df.loc[(df['team'] == home_team)])

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

        #print(df['makes_home'].head(50))



        df['makes_away'] = df['makes_away'].cumsum()
        df['misses_away'] = df['misses_away'].cumsum()
        df['Three_Pct_Away'] = (df['makes_away']) / ((df['makes_away'] + df['misses_away']))

        #print(df['makes_away'].head(50))

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

        #print(max_difference, file)


        new_df = df.iloc[:max_difference+1]
        #print(new_df['home_score'].iloc[-1], new_df['away_score'].iloc[-1]) #so all of this looks good...

        #print(new_df.tail(2))



        #before_comeback = df.loc[:max_difference]



        #so we have a few issues here... first before_comeback is the same as df
        #second we're still getting some games where it is a blowout

        if identify_winning_team(new_df) == 1:

            #winning_team = home_team

            #home team had large lead

            winning_team, losing_team = home_team, away_team

            final_winning_score = df['home_score'].iloc[-1] #gave up comeback
            final_losing_score = df['away_score'].iloc[-1] #made comeback

            final_winner_scores.append(final_winning_score)
            final_loser_scores.append(final_losing_score)



            #NOW WINNING TEAM IS JUST TEAM THAT WAS AHEAD AT THE TIME

            new_df.rename(columns={'home_score': 'winner_score', 'away_score': 'loser_score','makes_home': 'makes_winner', 'makes_away': 'makes_loser', 'misses_home': 'misses_winner', 'misses_away': 'misses_loser', 'Three_Pct_Home': 'Three_Pct_Winner', 'Three_Pct_Away': 'Three_Pct_Loser', 'home_assists': 'Assists_Winner', 'away_assists': 'Assists_Loser'}, inplace=True)
        else:

            final_winning_score = df['away_score'].iloc[-1]
            final_losing_score = df['home_score'].iloc[-1]

            final_winner_scores.append(final_winning_score)
            final_loser_scores.append(final_losing_score)

            winning_team, losing_team = away_team, home_team
            new_df.rename(columns={'home_score': 'loser_score', 'away_score': 'winner_score', 'makes_home': 'makes_loser', 'makes_away': 'makes_winner', 'misses_home': 'misses_loser', 'misses_away': 'misses_winner', 'Three_Pct_Home': 'Three_Pct_Loser', 'Three_Pct_Away': 'Three_Pct_Winner', 'home_assists': 'Assists_Loser', 'away_assists': 'Assists_Winner'}, inplace=True)
            #winning_team = away_team
            #change columns to winning team and losing team


        #first_half = df.loc[(df['period'] == 1) | (df['period'] == 2)] #this works

        winner_score = new_df['winner_score'].iloc[-1]
        loser_score = new_df['loser_score'].iloc[-1]




        winning_3pct = new_df['Three_Pct_Winner'].iloc[-1]
        losing_3_pct = new_df['Three_Pct_Loser'].iloc[-1]

        winning_3_taken_winner = new_df['misses_winner'].iloc[-1] + new_df['makes_winner'].iloc[-1]
        winning_3_taken_loser = new_df['misses_loser'].iloc[-1] + new_df['makes_loser'].iloc[-1]

        winning_3_totals.append(winning_3_taken_winner)
        losing_3_totals.append(winning_3_taken_loser)

        winning_teams.append(winning_team)
        losing_teams.append(losing_team)


        winning_3_list.append(winning_3pct)
        losing_3_list.append(losing_3_pct)

        loser_scores.append(loser_score)
        winner_scores.append(winner_score)

        games_final.append(new_df)
        #print(first_half.tail(2))

    return losing_3_list, winning_3_list, winning_3_totals, losing_3_totals, winner_scores, loser_scores, winning_teams, losing_teams, final_winner_scores, final_loser_scores

#better_list = after_all_star(comeback_games)
#print(len(better_list))
#print(better_list)
#worse_list = after_all_star(non_comeback_games)
#print(len(worse_list))
#print(worse_list)

# losses_pct, wins_pct, winning_threes, losing_threes, winner_points, loser_points, winning_team_list, losing_team_list = team_names(better_list) #used to be games as argument
# losses_pct2, wins_pct2, winning_threes2, losing_threes2, winner_points2, loser_points2, winning_team_list2, losing_team_list2 = team_names(worse_list)


losses_pct, wins_pct, winning_threes, losing_threes, winner_points, loser_points, winning_team_list, losing_team_list, winning_final_scorez, losing_final_scorez = team_names(comeback_games) #used to be games as argument
losses_pct2, wins_pct2, winning_threes2, losing_threes2, winner_points2, loser_points2, winning_team_list2, losing_team_list2, winning_final_scorez2, losing_final_scorez2 = team_names(non_comeback_games)







print(winner_points)
print(loser_points)

checkit = tuple(zip(winner_points, loser_points))
checkit2 = tuple(zip(winning_final_scorez, losing_final_scorez))

print(checkit)
print(checkit2)

wins_mean = statistics.mean(wins_pct)
losses_mean = statistics.mean(losses_pct)
winning_threes_mean = statistics.mean(winning_threes)
losing_threes_mean = statistics.mean(losing_threes)
loser_points_mean = statistics.mean(loser_points)
winner_points_mean = statistics.mean(winner_points)
print(loser_points_mean)
print(winner_points_mean)


myList = list(np.around(np.array(wins_pct),3))
myList2 = list(np.around(np.array(losses_pct),3))



myList = [incom for incom in myList if str(incom) != 'nan']
myList2 = [incom for incom in myList2 if str(incom) != 'nan']

wins_mean = statistics.mean(myList)
losses_mean = statistics.mean(myList2)



print(winning_threes_mean)
print(losing_threes_mean)
print(Counter(winning_team_list))
print(Counter(losing_team_list))


print(wins_mean, "Down and ended up winning")
print(losses_mean, "Up and ended up losing")
print(winning_threes_mean, "Winning at the time but lost")
print(losing_threes_mean, "Losing at the time but won")

#wins_mean2 = statistics.mean(wins_pct2)
losses_mean2 = statistics.mean(losses_pct2)
winning_threes_mean2 = statistics.mean(winning_threes2)
losing_threes_mean2 = statistics.mean(losing_threes2)
loser_points_mean2 = statistics.mean(loser_points2)
winner_points_mean2 = statistics.mean(winner_points2)
print(loser_points_mean2)
print(winner_points_mean2)
print(losses_pct2)
print(wins_pct2)
print(winning_threes_mean2)
print(losing_threes_mean2)
print(Counter(winning_team_list2))
print(Counter(losing_team_list2))

myList3 = [incom for incom in wins_pct2 if str(incom) != 'nan']
wins_mean2 = statistics.mean(myList3)


print(wins_mean2, "Up and Won")
print(losses_mean2, "Down and Lost")
print(winning_threes_mean2, "Up and Won")
print(losing_threes_mean2, "Down and Lost")
