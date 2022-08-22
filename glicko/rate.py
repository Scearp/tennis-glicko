import pandas as pd
import glicko2 as gl
import numpy as np

from datetime import datetime

import utils

def parse_score(raw_score):
    score = []
    try:
        for set in raw_score.split(" "):
            if set.upper() in ["RET", "DEF.", "DEF"]:
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
    sets = matches.copy()
    sets.score = sets.score.apply(lambda x: str(parse_score(str(x))))
    sets.score = sets.score.apply(lambda x: x[n])

    sets_to_winner = sets[sets.score == '1'].copy()
    sets_to_loser = sets[sets.score == '0'].copy()

    #swapping loser_id and winner_id columns in sets where the loser of the match won.
    temp = sets_to_loser.winner_id.copy()
    sets_to_loser.winner_id = sets_to_loser.loser_id
    sets_to_loser.loser_id = temp

    sets = pd.concat([sets_to_winner, sets_to_loser])
    sets = sets.sort_values("tourney_date")
    sets = sets.reset_index(drop=True)

    sets.winner_id = sets.winner_id.apply(lambda x: int(x))
    sets.loser_id = sets.loser_id.apply(lambda x: int(x))

    return sets

def get_dates(start_year, end_year, time_delta):
    start_date = "{year}-01-01".format(year=start_year)
    start_date = utils.monday(start_date)

    if end_year == 2022:
        limit_date = datetime.today().date()
    else:
        limit_date = utils.monday(f"{end_year + 1}-01-01")

    i = 1

    while start_date + i * time_delta < limit_date:
        i += 1

    end_date = start_date + i * time_delta

    start_date = utils.date_to_string(start_date)
    end_date = utils.date_to_string(end_date)

    dates = utils.get_dates(start_date, end_date, time_delta)

    return dates  

def update_ratings(matches, players={}):
    period_players = []

    if not matches.empty:
        for match in zip(matches.winner_id, matches.loser_id):
            if match[0] not in players:
                players[match[0]] = gl.Player()
            if match[1] not in players:
                players[match[1]] = gl.Player()
            if match[0] not in period_players:
                period_players.append(match[0])
            if match[1] not in period_players:
                period_players.append(match[1])

            players[match[0]].add_opponent(players[match[1]], 1)
            players[match[1]].add_opponent(players[match[0]], 0)

    for player in players:
        if player not in period_players:
            players[player].did_not_compete()
        else:
            players[player].update_player()
            players[player].remove_opponents()

    return players

def remove_inactive_players(ratings, years, period):
    inactive_players = []
    for player in ratings:
        if ratings[player].since_last_match > 52 // period * years:
            inactive_players.append(player)
    for player in inactive_players:
        del ratings[player]

def update_rating_file(type, date, players, max_dev, f):
    line = "{type},{player},{rating},{deviation},{date}\n"
    
    for player in players:
        if max_dev < players[player].getRd():
            continue
        next_line = line.format(type=type,
                                player=player,
                                rating=round(players[player].getRating()),
                                deviation=round(players[player].getRd()),
                                date=date)

        f.write(next_line)

def calculate_ratings(date, matches, players, set=None, f=None):

        if set != None and not matches.empty:
            matches = nth_sets(matches, set)
        period_players = []
        if not matches.empty:
            for s in zip(matches.winner_id, matches.loser_id):
                if s[0] not in players:
                    players[s[0]] = gl.Player()
                if s[1] not in players:
                    players[s[1]] = gl.Player()
                if s[0] not in period_players:
                    period_players.append(s[0])
                if s[1] not in period_players:
                    period_players.append(s[1])

                players[s[0]].add_opponent(players[s[1]], 1)
                players[s[1]].add_opponent(players[s[0]], 0)

        for player in players:
            if player not in period_players:
                players[player].did_not_compete()
            else:
                players[player].update_player()
                players[player].remove_opponents()

        if f != None:
            for player in period_players:
                f.write("{p},{r},{d},{da}\n".format(p=player, r=round(players[player].getRating()), d=round(players[player].getRd()),da=date))

        return players

def get_matches(date, next_date, engine):
    com1 = "select tourney_date, winner_id, loser_id, score from wta_match"
    com2 = "where tourney_date>='{date}'".format(date=date)
    com3 = "and tourney_date<'{date}'".format(date=next_date)

    com = " ".join([com1, com2, com3])

    df = pd.read_sql(com, engine)

    try:
        df.columns = ['tourney_date', 'winner_id', 'loser_id', 'score']
        df = df[df.score.apply(lambda x: utils.is_valid_score(x))]
    except:
        print("{date}: no matches".format(date=date))

    if len(df) == 0:
        print("{date}: no matches".format(date=date))

    return df

def get_sets(matches, set):
    if matches.empty:
        return matches
    sets = nth_sets(matches, set)
    return sets



