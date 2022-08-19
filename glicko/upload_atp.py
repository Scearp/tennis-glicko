import mysql.connector as msql
import sqlalchemy as mysql
import pandas as pd
import time

start_time = time.time()

engine = mysql.create_engine("mysql://root:Butterlands23@localhost/tennis")
engine.execute("truncate table atp_match")

cols = ["tourney_name", "tourney_date", "winner_id", "loser_id", "score", "surface"]

start = 1968
end = 2022

for y in range(start, end + 1):
    print(y, "main draw")
    df = pd.read_csv("./tennis_atp/atp_matches_{year}.csv".format(year=y), usecols=cols)

    df.columns = ['tourney_name', 'match_surface', 'tourney_date', 'winner_id', 'loser_id', 'match_score']

    df.to_sql('atp_match', engine, if_exists='append', index=False)

for y in range(max(start, 1978), end + 1):
    print(y, "qualies itf")
    df = pd.read_csv("./tennis_atp/atp_matches_qual_chall_{year}.csv".format(year=y), usecols=cols, encoding='latin1')

    df.columns = ['tourney_name', 'match_surface', 'tourney_date', 'winner_id', 'loser_id', 'match_score']

    df.to_sql('atp_match', engine, if_exists='append', index=False)

print(time.time() - start_time)