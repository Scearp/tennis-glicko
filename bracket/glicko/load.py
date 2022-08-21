import pandas as pd
from pyarrow import csv

from .player import Player

def load_players(path: str, tour: str) -> list:
    player_file = f"{path}/tennis_{tour}/{tour}_players.csv"
    players = []

    data = pd.read_csv(player_file)

    use_cols = ['player_id', 'name_first', 'name_last', 'ioc']
    cols = [list(data[col]) for col in use_cols]

    for row in zip(*cols):
        players.append(Player(row[0], row[2], row[1], row[3]))

    return players

def load_ratings(path: str, tour: str) -> pd.DataFrame:
    rating_file = f"{path}/{tour}.csv"

    table = csv.read_csv(rating_file)

    df = table.to_pandas()
    df = df.sort_values(by='date')
    df = df.drop_duplicates(['player_id', 'mode'], keep='last')

    return df

def load_rating_history(path: str, tour: str) -> pd.DataFrame:
    table = csv.read_csv(f"{path}/{tour}.csv")

    return table.to_pandas()

def load_set_ratings(path: str, tour: str) -> pd.DataFrame:
    rating_file = f"{path}/{tour}_ratings.csv"

    table = csv.read_csv(rating_file)

    df = table.to_pandas()

    return df