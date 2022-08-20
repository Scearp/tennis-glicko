import rate
import time

def main():
    start = 1968
    end = 2022

    f = open('wta.csv', mode='w')
    f.write('mode,player_id,rating,deviation,date\n')

    ratings = {}
    set_ratings = [{}, {}, {}]

    dates = rate.get_dates(start, end)

    for date in dates:
        matches = rate.get_matches(date)
        rate.update_ratings(matches, ratings)
        rate.remove_inactive_players(ratings, 5)
        rate.update_rating_file("match", date, ratings, 160, f)

        for i in range(3):
            sets = rate.get_sets(matches, i)
            rate.update_ratings(sets, set_ratings[i])
            rate.remove_inactive_players(set_ratings[i], 5)
            rate.update_rating_file(f"set_{i+1}", date, set_ratings[i], 160, f)

if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time() - start)
