import json
import sys

import glicko as gl
import pandas as pd

def main():
    with open("./settings.json") as cfg:
        settings = json.load(cfg)

    tour = "wta"

    try:
        n = int(sys.argv[1])
    except:
        n = 10

    players = gl.load_players(settings['data_path'], tour)
    ratings = gl.load_ratings(settings['rating_path'], tour)

    df = ratings[ratings['mode'].apply(lambda x: x == 'match')].copy()
    df = df[df['date'].apply(lambda x: x.year == 2022)]
    df = df.sort_values(by='rating', ascending=False).copy()

    player_ids = list(df['player_id'])[:n]

    players = [player for player in players if player.id in player_ids]

    for player in players:
        player.set_rating(ratings)
    
    players = sorted(players, key=lambda x: x.rating, reverse=True)

    names = [str(p) for p in players]
    rats = [p.rating for p in players]
    devs = [p.deviation for p in players]
    srats = [p.set_ratings for p in players]
    sdevs = [p.set_deviations for p in players]

    print(pd.DataFrame([names, rats, devs, srats, sdevs]).T.to_string())

if __name__ == "__main__":
    main()