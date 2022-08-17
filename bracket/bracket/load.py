import glicko as gl

def load_players(tour: str, name: str) -> list:
    filename = f"./{tour}/{name}.txt"

    with open(filename, 'r') as txt:
        rows = txt.readlines()

        players = [row.rstrip('\n') for row in rows]

    return players
