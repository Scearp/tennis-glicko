import glicko as gl
import pandas as pd

import math

def odds(players: list):
    matches = [[players[2*i], players[2*i+1]] for i in range(len(players)//2)]
    match = []
    match_set = []
    straights = []
    decider = []
    set_1 = []
    set_2 = []
    set_3 = []

    for p in [i for i in players if i != 'BYE']:
        if p.deviation >= 70 or p.set_deviations[-1] >= 100:
            p.set_ratings[-1] += p.rating - 290
            p.set_ratings[-1] /= 2

            p.set_deviations[-1] = p.set_deviations[-1] ** 2 + p.deviation ** 2 + 73 ** 2
            p.set_deviations[-1] = math.sqrt(p.set_deviations[-1])

    for m in matches:
        match.append(gl.get_expectation(m[0], m[1]))
        match_set.append(gl.get_expectation_from_set(m[0], m[1]))
        
        set_1.append(gl.get_set_expectation(m[0], m[1], 0))
        set_2.append(gl.get_set_expectation(m[0], m[1], 1))
        set_3.append(gl.get_set_expectation(m[0], m[1], 2))

        s2w = min(1, set_2[-1] + 0.05)
        s2l = min(1, set_2[-1] - 0.05)

        straights.append(set_1[-1] * s2w)
        decider.append(set_1[-1] * (1 - s2w) * set_3[-1] + 
                       (1 - set_1[-1]) * s2l * set_3[-1])

        match.append(1 - match[-1])
        match_set.append(1 - match_set[-1])

        set_1.append(1 - set_1[-1])
        set_2.append(1 - set_2[-1])
        set_3.append(1 - set_3[-1])

        s2w = min(1, set_2[-1] + 0.05)
        s2l = min(1, set_2[-1] - 0.05)

        straights.append(set_1[-1] * s2w)
        decider.append(set_1[-1] * (1 - s2w) * set_3[-1] + 
                       (1 - set_1[-1]) * s2l * set_3[-1])

    df = pd.DataFrame([players,
                       match,
                       set_1,
                       set_2,
                       set_3,
                       match_set,
                       straights,
                       decider]).T

    df.columns = ['name', 'match', 'set_1', 'set_2', 'set_3', 'match_set', '2-0', '2-1']
    return df


