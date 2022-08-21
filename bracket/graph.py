import glicko as gl
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as pdt

import json
import sys

def main():
    with open("./settings.json") as cfg:
        settings = json.load(cfg)

    tour = "wta"

    players = gl.load_players(settings['data_path'], tour)
    ratings = gl.load_rating_history(settings['rating_path'], tour)

    mode = sys.argv[1]
    names = sys.argv[2:]

    ratings = ratings[ratings['mode'].apply(lambda x: x == mode)]

    names = [name.replace(".", " ") for name in names]
    names = [name.replace("__", " ") for name in names]

    fig, ax = plt.subplots(1)

    for name in names:
        player = gl.search_players(name, players).id

        df = ratings[ratings.player_id.apply(lambda x: x == player)]

        date = df['date']
        rating = df['rating']
        deviation = df['deviation']

        ax.step(date, rating, where='post', label=name)
        #ax.step(date, deviation, where='post', label=name+" dev")

    ax.xaxis.set_major_formatter(pdt.DateFormatter('%y'))
    ax.xaxis.set_major_locator(pdt.YearLocator(4))
    ax.legend()

    plt.show()

if __name__ == "__main__":
    main()