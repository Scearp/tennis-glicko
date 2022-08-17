from re import search
import sys

import glicko as gl
import pandas as pd
import numpy as np
import mysql.connector as msql

conn = msql.connect(host='localhost', user='root', password='Butterlands23')
curs = conn.cursor()
curs.execute("use tennis")

def main():
    name = " ".join(sys.argv[1:])

    players = gl.load_players("C:/Users/cefpe/tennis/glicko", 'wta')

    player = gl.search_players(name, players)

    start_year = 2018
    end_year = 2022

    dfs = []

    for y in range(start_year, end_year + 1):
        command = f"select * from wta_match where tourney_date>='{y}-01-01'"

        curs.execute(command)

        dfs.append(pd.DataFrame(curs.fetchall()))

    df = pd.concat(dfs)

    df[6] = [str(s) for s in df[6]]

    df = df[df[6].apply(lambda x: len(x.split()) == 3)]

    wdf = df[df[6].apply(lambda x: int(x.split()[0].split('-')[0]) > int(x.split()[0].split('-')[1][0]))]

    ldf = df[df[6].apply(lambda x: int(x.split()[0].split('-')[0]) < int(x.split()[0].split('-')[1][0]))]

    #wdf = df[df[4] == player.id]
    #ldf = df[df[5] == player.id]

    print(len(wdf), len(ldf))

if __name__ == '__main__':
    main()