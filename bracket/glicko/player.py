from pandas import DataFrame

class Player:
    def __init__(self, player_id, surname, name, country):
        self.id = int(player_id)
        self.surname = surname.upper()

        self.name = name.upper() if isinstance(name, str) else None
        self.country = country.upper() if isinstance(country, str) else None

    def set_rating(self, ratings: DataFrame, set_rats: DataFrame) -> None:
        df = ratings[ratings['player_id'] == self.id]
        tdf = df[df['mode'] == 'match']
        try:
            self.rating = list(tdf['rating'])[0]
        except:
            (print(self.surname))
        self.deviation = list(tdf['deviation'])[0]

        df = set_rats[set_rats['player_id'] == self.id]
        use_cols = ['set1_rating', 'set2_rating', 'set3_rating']
        cols = [list(df[c])[0] for c in use_cols]

        self.set_ratings = [cols[0], cols[1], cols[2]]
        self.set_ratings[2] = (self.set_ratings[2] + self.rating) // 2

        use_cols = ['set1_rd', 'set2_rd', 'set3_rd']
        cols = [list(df[c])[0] for c in use_cols]

        self.set_deviations = [cols[0], cols[1], cols[2]]

    def __str__(self):
        return f"{self.name[0]}. {self.surname}"