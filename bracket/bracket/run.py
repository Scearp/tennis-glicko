import random
import math

import pandas as pd
from numpy import mat
import glicko as gl

def __get_matches(players: list) -> list:
    matches = []
    for i in range(len(players) // 2):
        match = [players[2 * i], players[2 * i + 1]]
        matches.append(match)
    
    return matches

def __trial(players: list, estimate) -> list:
    results = [players]
    while len(results[-1]) > 1:
        matches = __get_matches(results[-1])
        winners = []
        for match in matches:
            expected = estimate(match[0], match[1])
            winners.append(random.choices(match, [expected, 1 - expected])[0])

        results.append(winners)

    return results[1:]

def monte(players: list, n: int, set=False):
    d = {p: [0] * int(math.log(len(players), 2)) for p in players}

    for _ in range(n):
        if set:
            res = __trial(players, gl.get_expectation_from_set)
        else:
            res = __trial(players, gl.get_expectation)
        for r in range(len(res)):
            for p in res[r]:
                d[p][r] += 1

    for p in d:
        d[p] = [round(r / n, 3) for r in d[p]]

    return d
