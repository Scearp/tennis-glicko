import pandas as pd

def read_matches(year, level_string, data_path, columns):
    print(year, level_string)
    path = "{path}/tennis_wta/{level}_{year}.csv"
    path = path.format(path=data_path,
                       level=level_string,
                       year=year)

    df = pd.read_csv(path, usecols=columns, encoding='latin1')

    return df