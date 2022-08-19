import glicko2 as gl
import pandas as pd

from datetime import datetime, timedelta

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

def string_to_date(date):
    date = str(date).split("-")

    y = int(date[0])
    m = int(date[1])
    d = int(date[2])

    return datetime(y, m, d).date()

def date_to_string(date):
    y = date.year
    m = date.month
    d = date.day

    if m < 10:
        m = "0" + str(m)
    if d < 10:
        d = "0" + str(d)

    return "-".join([str(y), str(m), str(d)])

def monday(date):
    date = string_to_date(date)
    date = date - timedelta(days=date.weekday())

    return date_to_string(date)

def get_dates(start_date, end_date):
    dates = [start_date]
    date = string_to_date(start_date)

    while date_to_string(date) != end_date:
        date += timedelta(days=7)
        dates.append(date_to_string(date))

    return dates

def is_valid_tournament(tourney_name):
    if "BJK" in tourney_name: return False
    if "Fed Cup" in tourney_name: return False
    if "Davis Cup" in tourney_name: return False

    #if "W10" in tourney_name: return False
    #if "W15" in tourney_name: return False
    #if "W25" in tourney_name: return False
    #if "W50" in tourney_name: return False
    #if "W60" in tourney_name: return False

    #if "10K" in tourney_name: return False
    #if "15K" in tourney_name: return False
    #if "25K" in tourney_name: return False
    #if "50K" in tourney_name: return False
    #if "60K" in tourney_name: return False

    return True

def is_valid_score(score):
    if score == None: return False
    if "W/O" in score: return False
    if "May" in score: return False
    if "UNK" in score: return False

    na = True
    for n in range(0, 20):
        if str(n) in score:
            na = False
    if na: return False

    return True