from numpy import full
from .player import Player

def __parse_name(query: str) -> tuple:
    '''
    Args:
        query: a string, with multiple surnames connected by _'s
    Returns:
        (surname, None) if no given names;
        (surname, given names) otherwise
    '''
    query = query.upper()
    name = query.split()

    if len(name) == 1:
        return (name[0].replace('_', ' '), None)

    surname = name[-1].replace('_', ' ')

    return (surname, " ".join(name[:-1]))

def search_players(query: str, players: list) -> Player:
    name = __parse_name(query)

    matches = [p for p in players if p.surname == name[0]]

    if len(matches) == 0:
        raise ValueError(f"Player {query} not found.")
    if len(matches) == 1:
        return matches[0]
    
    full_matches = [p for p in matches if p.name == name[1]]

    if len(full_matches) == 0:
        print(f"Player {query} not found. Searching similar given names...")
        partial_matches = [p for p in matches if name[1] in p.name]
        if len(partial_matches) == 0:
            raise ValueError(f"Player {query} not found.")
        if len(partial_matches) == 1:
            return partial_matches[0]
        raise ValueError(f"Multiple matches found for player {query}")
    if len(full_matches) == 1:
        return full_matches[0]

    raise ValueError(f"Player {query} not found")