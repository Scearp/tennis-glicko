from msilib.schema import Directory
import pandas as pd

import sys

def first_cap(string):
    if len(string) > 1:
        return string[0].upper() + string[1:]
    return string[0].upper()

def _format_name(name):
    match_types = ['tb1', 'tb2', 'tb3', 'sr']

    name = [t.lower() for t in name if t.lower() not in match_types]
    return [first_cap(n) for n in name]

def format_name(name):
    name = name.replace('-', ' ')
    names = []
    surnames = []

    for token in name.split(' '):
        if token.upper() == token:
            surnames.append(token)
        else:
            names.append(token)

    name = " ".join(_format_name(names))
    surname = "_".join(_format_name(surnames))

    return " ".join([name, surname])

def main():
    path = "./bracket/{tour}/oop.csv".format(tour=sys.argv[1])

    df = pd.read_csv(path, header=None)
    players = []
    for match in list(df[0]):
        for player in match.split(' {spl} '.format(spl=sys.argv[2])):
            players.append(format_name(player))
    
    out_path = "./bracket/{tour}/oop.txt".format(tour=sys.argv[1])
    with open(out_path, mode='w') as csv_file:
        for player in players:
            csv_file.write("{player}\n".format(player=player))


if __name__ == '__main__':
    main()
