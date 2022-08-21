import rate
import json
import time

import sqlalchemy as sql
import database as db

from datetime import timedelta

def main():
    start = 1968
    end = 2022

    f = open('wta.csv', mode='w')
    f.write('mode,player_id,rating,deviation,date\n')

    with open("./settings.json") as cfg:
        settings = json.load(cfg)

    engine = db.create_engine(settings)
    engine.execute("use tennis")

    ratings = {}
    set_ratings = [{}, {}, {}]

    period = settings['rating_period']
    time_delta = timedelta(days=7*period)
    dates = rate.get_dates(start, end, time_delta)

    for i in range(len(dates) - 1):
        date = dates[i]
        next_date = dates[i+1]
        matches = rate.get_matches(date, next_date, engine)
        rate.update_ratings(matches, ratings)
        rate.remove_inactive_players(ratings, 5, period)
        rate.update_rating_file("match", date, ratings, 160, f)

        for i in range(3):
            sets = rate.get_sets(matches, i)
            rate.update_ratings(sets, set_ratings[i])
            rate.remove_inactive_players(set_ratings[i], 5, period)
            rate.update_rating_file(f"set_{i+1}", date, set_ratings[i], 160, f)

if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time() - start)
