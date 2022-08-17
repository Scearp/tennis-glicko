import pandas as pd
import sys

def first_cap(string):
    return string[0].upper() + string[1:]

def format_name(name):
    name = name.lower()
    name = name.replace('-', ' ')
    match_types = ['tb1', 'tb2', 'tb3', 'sr']
    name_list = name.split(' ')
    for type in match_types:
        name_list = [n for n in name_list if n != type]
    try:
        name_list = [first_cap(n) for n in name_list]
    except:
        raise ValueError(name, name_list)
    name = " ".join(name_list)
    
    return name

def main():
    path = "./{tour}/oop.csv".format(tour=sys.argv[1])

    df = pd.read_csv(path, header=None)
    players = []
    for match in list(df[0]):
        for player in match.split(' {spl} '.format(spl=sys.argv[2])):
            players.append(format_name(player))
    
    out_path = "./{tour}/tip.txt".format(tour=sys.argv[1])
    with open(out_path, mode='w') as csv_file:
        for player in players:
            csv_file.write("{player}\n".format(player=player))


if __name__ == '__main__':
    main()
