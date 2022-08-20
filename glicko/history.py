import pandas as pd
import glicko2 as gl
import numpy as np
import mysql.connector as msql

from datetime import datetime, timedelta

import time

import utils
import copy

def read_matches(dir, start_year, end_year):
    matches = []
    columns = ["tourney_name", "tourney_date",
               "winner_id", "loser_id", "score"]
    for year in range(start_year, end_year + 1):
        file = "{dir}/wta_matches_{year}.csv".format(dir=dir, year=year)
        matches.append(pd.read_csv(file, usecols=columns))
        file2 = "{dir}/wta_matches_qual_itf_{year}.csv".format(dir=dir, year=year)
        matches.append(pd.read_csv(file2, usecols=columns, encoding="latin1"))

    return pd.concat(matches).sort_values("tourney_date").reset_index(drop=True)

def parse_score(raw_score):
    score = []
    try:
        for set in raw_score.split(" "):
            if set == "RET" or set == "Def.":
                score = score[ :-1]
                score.append(1)
            else:
                set = set.split("-")
                winner = set[0].split("(")[0]
                loser = set[1].split("(")[0]
                if winner > loser:
                    score += "1"
                else:
                    score += "0"
        if len(score) == 1:
            return "{s1}--".format(s1=score[0])
        if len(score) == 2:
            return "{s1}{s2}-".format(s1=score[0], s2=score[1])
        if len(score) == 3:
            return "{s1}{s2}{s3}".format(s1=score[0], s2=score[1], s3=score[2])
    except:
        return np.nan

def nth_sets(matches, n):
    matches.score = [str(s) for s in matches.score]
    matches.score = [parse_score(s) for s in matches.score]
    matches.score = [str(s) for s in matches.score]
    winner_sets = matches[matches.score.apply(lambda x: x[n] == "1")]
    loser_sets = matches[matches.score.apply(lambda x: x[n] == "0")]

    winners = [winner for winner in loser_sets.loser_id]
    losers = [loser for loser in loser_sets.winner_id]

    loser_sets.winner_id = winners
    loser_sets.loser_id = losers

    sets = pd.concat([winner_sets, loser_sets])
    sets = sets.sort_values("tourney_date")
    sets = sets.reset_index(drop=True)

    return sets

def calculate_ratings(year, players, set=None, f=None):
        start_date = "{year}-01-01".format(year=year)
        start_date = utils.string_to_date(utils.monday(start_date))
        start_date = utils.date_to_string(start_date)

        end_date = "{year}-01-01".format(year=year + 1)
        end_date = utils.string_to_date(utils.monday(end_date))
        end_date -= timedelta(days=7)
        end_date = utils.date_to_string(end_date)

        if year == 2022:
            end_date = datetime.today()
            end_date = utils.date_to_string(end_date)
            end_date = utils.monday(end_date)

        dates = utils.get_dates(start_date, end_date)

        dates = dates[:-1]

        for date in dates:
            #print(date)
            weekly_sets = get_matches(date)
            if set != None and not weekly_sets.empty:
                weekly_sets = nth_sets(weekly_sets, set)
            weekly_players = []
            if not weekly_sets.empty:
                for s in zip(weekly_sets.winner_id, weekly_sets.loser_id):
                    if s[0] not in players:
                        players[s[0]] = gl.Player()
                    if s[1] not in players:
                        players[s[1]] = gl.Player()
                    if s[0] not in weekly_players:
                        weekly_players.append(s[0])
                    if s[1] not in weekly_players:
                        weekly_players.append(s[1])

                    players[s[0]].add_opponent(players[s[1]], 1)
                    players[s[1]].add_opponent(players[s[0]], 0)

            for player in players:
                if player not in weekly_players:
                    players[player].did_not_compete()
                else:
                    players[player].update_player()
                    players[player].remove_opponents()

            if f != None:
                for player in weekly_players:
                    f.write("{p},{r},{d},{da}\n".format(p=player, r=round(players[player].getRating()), d=round(players[player].getRd()), da=date))

        return players

conn = msql.connect(host='***REMOVED***', user='***REMOVED***', password='***REMOVED******REMOVED***')
curs = conn.cursor()
curs.execute("use tennis")

def get_matches(date, con=conn):
    next_date = utils.string_to_date(date)
    next_date += timedelta(days=7)
    next_date = utils.date_to_string(next_date)
    com1 = "select tourney_date, winner_id, loser_id, score from wta_match"
    com2 = "where tourney_date>='{date}'".format(date=date)
    com3 = "and tourney_date<'{date}'".format(date=next_date)
    com4 = "and tourney_name not like '%Fed Cup%'"
    com5 = "and tourney_name not like '%BJK%'"
    com6 = "and tourney_name not like '%10K%'"
    com7 = "and tourney_name not like '%W10%'"
    com6 = "and tourney_name not like '%15K%'"
    com7 = "and tourney_name not like '%W15%'"

    com = " ".join([com1, com2, com3])

    curs.execute(com)
    df = pd.DataFrame(curs.fetchall())
    try:
        df.columns = ['tourney_date', 'winner_id', 'loser_id', 'score']
        df = df[df.score.apply(lambda x: utils.is_valid_score(x))]
    except:
        print("{date}: no matches".format(date=date))

    return df
        
def nth_sets_yearly(args):
    matches = args[0]
    n = args[1]

    sets = nth_sets(matches, n)

    return sets

def yearly_matches(args):
    return args[0]

def main():
    start = 1968
    end = 2022

    set_ratings = [{}, {}, {}]
    setw_ratings = [{}, {}]
    setl_ratings = [{}, {}]
    match_ratings = {}

    f = open("history_wta.csv", "w")

    for year in range(start, end + 1):
        print('match', year)
        match_ratings = calculate_ratings(year, match_ratings, f=f)

    f.close()

if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time() - start)
