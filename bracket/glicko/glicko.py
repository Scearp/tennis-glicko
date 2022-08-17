import math

def __g(deviation):
    return 1 / math.sqrt(1 + 3 * math.pow(deviation, 2) / math.pow(math.pi, 2))

def __get_expectation(rating_1, rating_2, deviation_1, deviation_2):
    rating_1 = float(rating_1 - 1500) / 173.7178
    rating_2 = float(rating_2 - 1500) / 173.7178

    deviation_1 = float(deviation_1) / 173.7178
    deviation_2 = float(deviation_2) / 173.7178

    deviation = math.sqrt(deviation_1 ** 2 + deviation_2 ** 2)

    return 1 / (1 + math.exp(-1 * __g(deviation) * (rating_1 - rating_2)))

def get_expectation(player_1, player_2):
    if player_1 == "BYE":
        return 0
    if player_2 == "BYE":
        return 1

    return __get_expectation(player_1.rating,
                             player_2.rating,
                             player_1.deviation,
                             player_2.deviation)

def __set_expectation(player_1, player_2, set):
    return __get_expectation(player_1.set_ratings[set],
                             player_2.set_ratings[set],
                             player_1.set_deviations[set],
                             player_2.set_deviations[set])

def get_expectation_from_set(player_1, player_2):
    if player_1 == "BYE":
        return 0
    if player_2 == "BYE":
        return 1

    es = [__set_expectation(player_1, player_2, i) for i in range(3)]
    
    s1 = es[0]
    s2w = es[1] + 0.05
    s2l = es[1] - 0.05
    s3 = es[2]

    return s1 * s2w + s1 * (1 - s2w) * s3 + (1 - s1) * s2l * s3
    
def get_set_expectation(player_1, player_2, set):
    if player_1 == "BYE":
        return 0
    if player_2 == "BYE":
        return 1
    
    return __set_expectation(player_1, player_2, set)