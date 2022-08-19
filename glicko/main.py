import rate
import time

def main():
    start = 1968
    end = 2022

    f = open('wta.csv', mode='w')
    f.write('mode,player_id,rating,deviation,date\n')

    ratings = {}

    dates = rate.get_dates(start, end)

    for date in dates:
        matches = rate.get_matches(date)
        rate.update_ratings(matches, ratings)
        rate.remove_inactive_players(ratings, 10)
        rate.update_rating_file("match", date, ratings, 160, f)

if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time() - start)
