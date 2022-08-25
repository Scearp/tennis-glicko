#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "defines.h"

int is_int_in_array(int n, int array[]) {
    int i;

    if (array[0] == 0) {
        return 0;
    } else {
        for (i=array[0]; i>0; i--) {
            if (array[i] == n) {
                return 1;
            }
        }
    }
    return 0;
}

int *read_csv(const char *filename) {
    int array_size = sizeof(int) * 3 * 10000000;
    int *ints = malloc(array_size);
    char line[32];

    FILE *csv_file = fopen(filename, "r");

    int i = 0;

    while (!feof(csv_file)) {
        fgets(line, 32, csv_file);
        char *token = strtok(line, ",");

        while (token != NULL) {
            i++;
            if (i * sizeof(int) >= array_size - 100 * sizeof(int)) {
                array_size = array_size * 2;
                ints = realloc(ints, array_size);
            }
            ints[i] = atoi(token);
            token = strtok(NULL, ",");
        }
    }
    ints[0] = i;
    fclose(csv_file);

    return ints;
}

int *get_players(int *raw_data) {
    int array_size = sizeof(int) * ((int) raw_data[0]);
    int *players = malloc(array_size);

    players[0] = 0;

    int i, j = 0;

    for (i=0; i<=raw_data[0]; i++) {
        if (j * sizeof(int) >= array_size - sizeof(int)) {
            array_size = array_size * 2;
            players = realloc(players, array_size);
        }
        if (i % 3 != 1) {
            if (!is_int_in_array(raw_data[i], players)) {
                j++;
                players[j] = raw_data[i];
                players[0] = j;
            }
        }
    }

    return players;
}

match *get_matches(int *raw_data) {
    int array_size = sizeof(match) * (raw_data[0] + 6);
    match *matches = malloc(array_size);

    int i, j = 0;

    for (i=1; i<raw_data[0]; i=i+3) {
        j++;
        if (j * sizeof(match) >= array_size - sizeof(match)) {
            array_size = array_size * 2;
            matches = realloc(matches, array_size);
        }
        matches[j].date = raw_data[i];
        matches[j].winner = raw_data[i + 1];
        matches[j].loser = raw_data[i + 2];
    }
    matches[0].winner = j;

    return matches;
}

double player_get_rating(glicko_player player) {
    return (player.rating * 173.7178) + 1500;
}

double player_get_deviation(glicko_player player) {
    return player.deviation * 173.7178;
}

void player_prepare(glicko_player *player) {
    player->deviation = sqrt(pow(player->deviation, 2) + pow(player->volatility, 2));
}

double player_g(player_tuple opponent) {
    return 1 / sqrt(1 + 3 * pow(opponent.deviation, 2) / pow(PI, 2));
}

double player_expected(glicko_player player, player_tuple opponent) {
    return 1 / (1 + exp(-1 * player_g(opponent) * (player.rating - opponent.rating)));
}

double player_v(glicko_player player, player_tuple opponents[]) {
    double sum = 0;
    double E;
    int i;

    for (i=1; i<=opponents[0].id; i++) {
        E = player_expected(player, opponents[i]);
        sum += pow(player_g(opponents[i]), 2) * E * (1 - E);
    }

    return 1 / sum;
}

double player_delta(glicko_player player, player_tuple opponents[], double outcomes[], double v) {
    double sum = 0;
    int i;

    for (i=1; i<=opponents[0].id; i++) {
        sum += player_g(opponents[i]) * (outcomes[i] - player_expected(player, opponents[i]));
    }
    return v * sum;
}

double player_f(glicko_player player, double x, double delta, double v, double a) {
    double ex = exp(x);
    double numerator = ex * (pow(delta, 2) - pow(player.rating, 2) - v - ex);
    double denominator = 2 * pow(pow(player.rating, 2) + v + ex, 2);
    return numerator / denominator - ((x - a) / pow(TAU, 2));
}

double player_new_volatility(glicko_player player, player_tuple opponents[], double outcomes[], double v) {
    double a = log(pow(player.volatility, 2));
    double e = 0.000001;
    double A = a;

    double B;
    double delta = player_delta(player, opponents, outcomes, v);
    if (pow(delta, 2) > (player.deviation + v)) {
        B = log(pow(delta, 2) - player.deviation - v);
    } else {
        int k = 1;
        while (player_f(player, a - k * fabs(TAU), delta, v, a) < 0) {
            k++;
        }
        B = a - k * fabs(TAU);
    }
    double fA = player_f(player, A, delta, v, a);
    double fB = player_f(player, B, delta, v, a);
    while (fabs(B - A) > e) {
        double C = A + fA * (A - B) / (fB - fA);
        double fC = player_f(player, C, delta, v, a);

        if (fC * fB < 0) {
            A = B;
            fA = fB;
        } else {
            fA = fA / 2.0;
        }
        B = C;
        fB = fC;
    }

    return exp(A / 2.0);
}

void player_update(glicko_player *player) {
    player_tuple *opponents = player->opponents;
    double *outcomes = player->outcomes;
    double v = player_v(*player, opponents);
    player->volatility = player_new_volatility(*player, opponents, outcomes, v);
    player_prepare(player);
    player->deviation = 1 / sqrt((1 / pow(player->deviation, 2)) + (1 / v));
    double sum = 0;
    int i;
    for (i=1; i<=opponents[0].id; i++) {
        sum += player_g(opponents[i]) * (outcomes[i] - player_expected(*player, opponents[i]));
    }

    player->rating += pow(player->deviation, 2) * sum;
}

void player_dnc(glicko_player *player) {
    player_prepare(player);
}

void player_add_opponent(glicko_player *player, glicko_player *opponent_player, double outcome) {
    player_tuple opponent;
    opponent.id = opponent_player->id;
    opponent.rating = opponent_player->rating;
    opponent.deviation = opponent_player->deviation;
    opponent.volatility = opponent_player->deviation;    
    player->outcomes[0]++;
    player->opponents[0].id++;
    player->opponents[player->opponents[0].id] = opponent;
    player->outcomes[(int) player->outcomes[0]] = outcome;
}

void player_remove_opponents(glicko_player *player) {
    free(player->opponents);
    free(player->outcomes);
    player->opponents = malloc(sizeof(player_tuple) * 32);
    player->opponents[0].id = 0;
    player->outcomes = malloc(sizeof(double) * 32);
    player->outcomes[0] = 0;
}
