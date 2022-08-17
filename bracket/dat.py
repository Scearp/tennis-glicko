import pandas as pd

from pyarrow import csv

import mysql.connector as msql

from datetime import datetime

conn = msql.connect(host='***REMOVED***', user='***REMOVED***', password='***REMOVED******REMOVED***')
curs = conn.cursor()
curs.execute("use tennis")

curs.execute("select * from wta_match where tourney_date>'2020-01-01'")

df = pd.DataFrame(curs.fetchall())

df = df[df[6].notnull()]

df = df[df[6].apply(lambda x: 'W/O' not in x)]
df = df[df[6].apply(lambda x: 'Ret.' not in x)]
df = df[df[6].apply(lambda x: 'Def.' not in x)]

print(len(df))

print(df)

set = [1 if len(s.split()) > 2 else 0 for s in df[6]] * 2
match = [1] * len(df[6]) + [0] * len(df[6])
player = list(df[4]) + list(df[5])

rat = []
dev = []

tab = csv.read_csv("C:/Users/***REMOVED***/tennis/glicko/wta.csv")
rdf = tab.to_pandas()

rdf = rdf[rdf['date'] > datetime(2019,1,1).date()]

for tup in zip(list(df[1]), list(df[4])):
    print(tup)

    tdf = rdf[rdf['date'] < tup[0]]
    tdf = tdf.sort_values(by='date')
    tdf = tdf.drop_duplicates(['player_id', 'mode'], keep='last')

    tdf = tdf[tdf['player_id'] == tup[1]]

    try:
        rat.append(list(tdf['rating'])[0])
        dev.append(list(tdf['deviation'])[0])
    except:
        rat.append(0)
        dev.append(0)

for tup in zip(list(df[1]), list(df[5])):
    print(tup)

    tdf = rdf[rdf['date'] < tup[0]]
    tdf = tdf.sort_values(by='date')
    tdf = tdf.drop_duplicates(['player_id', 'mode'], keep='last')

    tdf = tdf[tdf['player_id'] == tup[1]]

    try:
        rat.append(list(tdf['rating'])[0])
        dev.append(list(tdf['deviation'])[0])
    except:
        rat.append(0)
        dev.append(0)

ndf = pd.DataFrame()

ndf['player'] = player
ndf['win_set'] = set
ndf['win_match'] = match
ndf['rating'] = rat
ndf['deviation'] = dev

ndf = ndf[ndf['rating'] > 0]

ndf.to_csv('./data.csv')