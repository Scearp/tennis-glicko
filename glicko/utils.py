import glicko2 as gl
import pandas as pd

from datetime import datetime, timedelta

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

    return date

def get_dates(start_date, end_date, time_delta):
    dates = [start_date]
    date = string_to_date(start_date)

    while date_to_string(date) < end_date:
        date += time_delta
        dates.append(date_to_string(date))

    return dates

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