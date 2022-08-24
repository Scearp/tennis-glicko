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
    int array_size = sizeof(int) * 3 * 100000;
    int *ints = malloc(array_size);
    char line[32];

    FILE *csv_file = fopen(filename, "r");

    int i = 0;

    while (!feof(csv_file)) {
        fgets(line, 32, csv_file);
        char *token = strtok(line, ",");

        while (token != NULL) {
            i++;
            if (i * sizeof(int) >= array_size - sizeof(int)) {
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
    int array_size = sizeof(int) * ((int) (raw_data[0] / 50));
    int *players = malloc(array_size);

    players[0] = 0;

    int i, j = 0;

    for (i=0; i<=raw_data[0]; i++) {
        if (j * sizeof(int) >= array_size - sizeof(int)) {
            array_size = array_size * 2;
            players = realloc(players, array_size);
        }
        if (i % 3 != 0) {
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
    int array_size = sizeof(match) * (raw_data[0] + 4) / 3;
    match *matches = malloc(array_size);

    int i, j = 0;

    for (i=1; i<raw_data[0]; i=i+4) {
        j++;
        if (j * sizeof(match) >= array_size - sizeof(match)) {
            array_size = array_size * 2;
            matches = realloc(matches, array_size);
        }
        matches[j].date = raw_data[i];
        matches[j].winner = raw_data[i + 1];
        matches[j].loser = raw_data[i + 2];
        matches[j].mode = raw_data[i + 3];
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

double player_g(glicko_player opponent) {
    return 1 / sqrt(1 + 3 * pow(opponent.deviation, 2) / pow(PI, 2));
}

double player_expected(glicko_player player, glicko_player opponent) {
    return 1 / (1 + exp(-1 * player_g(opponent) * (player.rating - opponent.rating)));
}

double player_v(glicko_player player, glicko_player opponents[]) {
    double sum = 0;
    double E;
    int i;

    for (i=1; i<=opponents[0].id; i++) {
        E = player_expected(player, opponents[i]);
        sum += pow(player_g(opponents[i]), 2) * E * (1 - E);
    }

    return 1 / sum;
}

double player_delta(glicko_player player, glicko_player opponents[], double outcomes[], double v) {
    double sum = 0;
    int i;

    for (i=1; i<=opponents[0].id; i++) {
        sum += player_g(opponents[i]) * (outcomes[i] - player_expected(player, opponents[i]));
    }
    return v * sum;
}

double player_new_volatility(glicko_player player, glicko_player opponents[], double outcomes[], double v) {
    int i = 0;
    double delta = player_delta(player, opponents, outcomes, v);
    double a = log(pow(player.volatility, 2));

    double x0 = a;
    double x1 = 0;

    double e = 0.000001;

    int count = 0;

    while (abs(x0 - x1) > e) {
        x0 = x1;
        double d = pow(player.rating, 2) + v + exp(x0);
        double h1 = -(x0 - a) / pow(TAU, 2) - 0.5 * exp(x0) / d + 0.5 * exp(x0) * pow(delta / d, 2);
        double h2 = -1 / pow(TAU, 2) - 0.5 * exp(x0) * (pow(player.rating, 2) + v) / pow(d, 2) + 0.5 * pow(delta, 2) * exp(x0) * (pow(player.rating, 2) + v - exp(x0)) / pow(d, 3);
        x1 = x0 - (h1 / h2);
        count++;
        if (count > 100) {
            break;
        }
    }

    return exp(x1/ 2);
}

void player_update(glicko_player *player) {
    glicko_player *opponents = player->opponents;
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

void player_add_opponent(glicko_player *player, glicko_player *opponent, double outcome) {
    player->outcomes[0]++;
    player->opponents[0].id++;
    player->opponents[player->opponents[0].id] = *opponent;
    player->outcomes[(int) player->outcomes[0]]  = outcome;
}

void player_remove_opponents(glicko_player *player) {
    free(player->opponents);
    free(player->outcomes);
    player->opponents = malloc(sizeof(glicko_player) * 16);
    player->opponents[0].id = 0;
    player->outcomes = malloc(sizeof(double) * 16);
    player->outcomes[0] = 0;
}
