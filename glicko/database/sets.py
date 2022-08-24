import pandas as pd
import numpy as np

def is_valid_score(score):
    if score == None: return False
    if "W/O" in score: return False
    if "May" in score: return False
    if "UNK" in score: return False

    na = True
    for n in range(0, 20):
        if str(n) in score:
            na = False
    if na: return False

    return True

def parse_score(raw_score):
    score = []
    try:
        for set in raw_score.split(" "):
            if set.upper() in ["RET", "DEF.", "DEF"]:
                score = score[ :-1]
                score.append(1)
            else:
                set = set.split("-")
                winner = set[0].split("(")[0]
                loser = set[1].split("(")[0]
                if winner > loser:
                    score += "1"
                else:
                    score += "0"

        if len(score) == 1:
            return "{s1}--".format(s1=score[0])
        if len(score) == 2:
            return "{s1}{s2}-".format(s1=score[0], s2=score[1])
        if len(score) == 3:
            return "{s1}{s2}{s3}".format(s1=score[0], s2=score[1], s3=score[2])
    except Exception as e:
        return np.nan

def nth_sets(matches, n):
    sets = matches.copy()
    sets.score = sets.score.apply(lambda x: str(x)[n])

    sets_to_winner = sets[sets.score == '1'].copy()
    sets_to_loser = sets[sets.score == '0'].copy()

    #swapping loser_id and winner_id columns in sets where the loser of the match won.
    temp = sets_to_loser.winner_id.copy()
    sets_to_loser.winner_id = sets_to_loser.loser_id
    sets_to_loser.loser_id = temp

    sets = pd.concat([sets_to_winner, sets_to_loser])
    sets = sets.sort_values("tourney_date")
    sets = sets.reset_index(drop=True)

    sets.winner_id = sets.winner_id.apply(lambda x: int(x))
    sets.loser_id = sets.loser_id.apply(lambda x: int(x))

    return sets