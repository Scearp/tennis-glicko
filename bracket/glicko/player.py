from pandas import DataFrame

class Player:
    def __init__(self, player_id, surname, name, country):
        self.id = int(player_id)
        self.surname = surname.upper()

        self.name = name.upper() if isinstance(name, str) else None
        self.country = country.upper() if isinstance(country, str) else None

    def set_rating(self, ratings: DataFrame) -> None:
        df = ratings[ratings['player_id'] == self.id]
        tdf = df[df['mode'] == 'match']
        try:
            self.rating = list(tdf['rating'])[0]
            self.deviation = list(tdf['deviation'])[0]
        except:
            print(self.surname)

        self.set_ratings = []
        self.set_deviations = []

        for i in range(1, 4):
            tdf = df[df['mode'] == f"set_{i}"]
            try:
                self.set_ratings.append(list(tdf['rating'])[0])
                self.set_deviations.append(list(tdf['deviation'])[0])
            except:
                print(self.surname)

    def __str__(self):
        return f"{self.name[0]}. {self.surname}"