import sqlalchemy as sql
import pandas as pd

import database as db

import time
import json

def upload_year(year, level_string, data_path, columns):
    print(year, level_string)
    path = "{path}/tennis_wta/{level}_{year}.csv"
    path = path.format(path=data_path,
                       level=level_string,
                       year=year)

    df = pd.read_csv(path, usecols=columns, encoding='latin1')
    df.to_sql('wta_match', engine, if_exists="append", index=False)


start_time = time.time()

with open("./settings.json") as cfg:
    settings = json.load(cfg)

engine = db.create_engine(settings)
engine.execute("truncate table wta_match")

with open("./glicko/config.json") as cfg:
    config = json.load(cfg)

columns = config['columns'][1:]

start_year = 1968
end_year = 2022

for y in range(start_year, end_year + 1):
    upload_year(y, 'wta_matches', settings['data_path'], columns)
    upload_year(y, 'wta_matches_qual_itf', settings['data_path'], columns)

print(time.time() - start_time)