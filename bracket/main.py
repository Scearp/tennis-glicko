import sys

import glicko as gl
import bracket as br
import tipping as tip
import pandas as pd

import json

import time

R_DICT = {
    1: 'W',
    2: 'F',
    3: 'SF',
    4: 'QF',
    5: 'R16',
    6: 'R32',
    7: 'R64',
    8: 'R128'
}

def get_players(names: list,
                players: list,
                ratings: pd.DataFrame) -> list:
    out = []
    for name in names:
        if name == "BYE":
            out.append(name)
        else:
            player = gl.search_players(name, players)
            player.set_rating(ratings)
            out.append(player)

    return out

def format_df(results: pd.DataFrame, set=False) -> pd.DataFrame:
    players = list(results.keys())
    if set:
        ratings = [p.set_ratings if p != 'BYE' else 0 for p in players]
        deviations = [p.set_deviations if p != 'BYE' else 0 for p in players]
    else:
        ratings = [p.rating if p != 'BYE' else 0 for p in players]
        deviations = [p.deviation if p != 'BYE' else 0 for p in players]

    df = pd.DataFrame(results)
    df = df.T

    df.insert(0, 'rat', ratings)
    df.insert(1, 'dev', deviations)

    heads = list(df.head())

    j = len(heads) - 2

    for i in range(2, len(heads)):
        heads[i] = j
        j -= 1

    for i in range(len(heads)):
        try:
            heads[i] = R_DICT[heads[i]]
        except:
            pass

    df.columns = heads
    df = df[df['rat'] != 0]
    df = df.reset_index()
    df.rename(columns={'index': 'player'}, inplace=True)

    return df

def main():
    now = time.time()

    with open("./settings.json") as cfg:
        settings = json.load(cfg)

    path = settings['data_path']
    tour = sys.argv[1]

    print("loading players...")
    players = gl.load_players(path, tour)

    path = settings['rating_path']

    print("loading ratings...")
    ratings = gl.load_ratings(path, tour)

    print(time.time() - now)

    command = ''

    while not command == "exit":
        command = input(":")
        if command == '':
            continue
        if command.split()[0] == 'draw':
            if len(command.split()) == 2 or command.split()[2] == 'm':
                now = time.time()
                print("loading bracket...")
                current_players = br.load_players(tour, command.split()[1])
                current_players = get_players(current_players,
                                            players,
                                            ratings)

                print('running simulation...')
                results = br.monte(current_players, 10000)
                df = format_df(results)
                print(df.to_string())
                last = list(df.columns)[-1]
                print(df[df[last] > 0.02].sort_values(last, ascending=False))
                print(f"simulation took {time.time() - now} seconds.")
            elif command.split()[2] == 's':
                now = time.time()
                print("loading bracket...")
                current_players = br.load_players(tour, command.split()[1])
                current_players = get_players(current_players,
                                            players,
                                            ratings)
                results = br.monte(current_players, 10000, set=True)
                df = format_df(results, set=True)
                print(df.to_string())
                last = list(df.columns)[-1]
                print(df[df[last] > 0.02].sort_values(last, ascending=False))
                print(f"simulation took {time.time() - now} seconds.")

        elif command.split()[0] == 'tip':
            now = time.time()
            current_players = br.load_players(tour, command.split()[1])
            try:
                current_players = get_players(current_players,
                                              players,
                                              ratings)
            except Exception as e:
                print(e)
                continue
            print(tip.odds(current_players).to_string())
            print(f"odds took {time.time() - now} seconds.")
        

if __name__ == '__main__':
    main()