import pandas as pd

import database as db

import time
import json

from datetime import timedelta

def period_start(date, dates):
    i = -1
    while dates[i] > date:
        i -= 1

    return dates[i]

def main():
    start_time = time.time()

    with open("./settings.json") as cfg:
        settings = json.load(cfg)

    with open("./glicko/config.json") as cfg:
        config = json.load(cfg)

    columns = config['columns']

    start_year = 1968
    end_year = 2022

    dfs = []

    for y in range(start_year, end_year + 1):
        dfs.append(db.read_matches(y, 'wta_matches', settings['data_path'], columns))
        dfs.append(db.read_matches(y, 'wta_matches_qual_itf', settings['data_path'], columns))

    df = pd.concat(dfs)

    dates = db.get_dates(start_year, end_year, settings['rating_period'] * timedelta(days=7))

    df = df.sort_values(by='tourney_date')

    df.tourney_date = df.tourney_date.apply(lambda x: db.parse_date(x))
    df.tourney_date = df.tourney_date.apply(lambda x: str(period_start(x, dates)).replace("-", ""))

    df.score = df.score.apply(lambda x: str(db.parse_score(str(x))))
    df = df[df.score.apply(lambda x: db.is_valid_score(x))]

    for i in range(3):
        sdf = db.nth_sets(df, i)


        sdf = sdf.drop('score', axis=1)

        sdf.to_csv(f"./mode_{i+1}.csv", index=False, header=False)

    df = df.drop('score', axis=1)

    df.to_csv("./mode_0.csv", index=False, header=False)

    print(time.time() - start_time)

if __name__ == "__main__":
    main()