import sqlalchemy as mysql
import pandas as pd

import time

start_time = time.time()

engine = mysql.create_engine("mysql://root:Butterlands23@localhost/tennis")
engine.execute("truncate table wta_match")

cols = ["tourney_name", "tourney_date", "winner_id", "loser_id", "score", "surface", "round", "tourney_level", "draw_size"]

start = 1968
end = 2022

for y in range(start, end + 1):
    print(y, "main draw")
    df = pd.read_csv("./tennis_wta/wta_matches_{year}.csv".format(year=y), usecols=cols)
    df.columns = ['tourney_name', 'match_surface', "draw_size", 'level', 'tourney_date', 'winner_id', 'loser_id', 'match_score', 'round']

    df.to_sql('wta_match', engine, if_exists='append', index=False)

for y in range(start, end + 1):
    print(y, "qualies itf")
    df = pd.read_csv("./tennis_wta/wta_matches_qual_itf_{year}.csv".format(year=y), usecols=cols, encoding='latin1')

    df.columns = ['tourney_name', 'match_surface', "draw_size", 'level', 'tourney_date', 'winner_id', 'loser_id', 'match_score', 'round']

    df.to_sql('wta_match', engine, if_exists='append', index=False)

#print('live')
#df = pd.read_csv('./live_wta.csv', usecols=cols)
#df.columns = ['tourney_name', 'match_surface', 'level', 'tourney_date', 'winner_id', 'loser_id', 'match_score', 'round']
#df.to_sql('wta_match', engine, if_exists='append', index=False)

print(time.time() - start_time)
