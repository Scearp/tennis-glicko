#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "utils.h"

int main() {
    clock_t start = clock();

    int *raw_data = read_csv("wta_matches.csv");
    int *player_ids = get_players(raw_data);
    match *matches = get_matches(raw_data);
    free(raw_data);

    int i;
    glicko_player *players = malloc(sizeof(glicko_player) * (player_ids[0] + 1));
    glicko_player *old_players = malloc(sizeof(glicko_player) * (player_ids[0] + 1));

    for (i=0; i<=player_ids[0]; i++) {
        players[i].id = player_ids[i];
        players[i].rating = 0;
        players[i].deviation = 350.0 / 173.7178;
        players[i].volatility = 0.06;
        players[i].opponents = malloc(sizeof(glicko_player) * 16);
        players[i].opponents[0].id = 0;
        players[i].outcomes = malloc(sizeof(double) * 16);
    }

    int a, b, j, k;
    int last_date = 0;
    int *weekly_players = malloc(sizeof(int) * (player_ids[0] + 1));
    weekly_players[0] = 0;

    FILE *out = fopen("ratings.csv", "w");

    for (i=1; i<=matches[0].winner; i++) {
        if (matches[i].date != last_date) {
            if (last_date % 10000 < 110) {
                printf("%i\n", last_date);
            }
            for (j=0; j<=players[0].id; j++) {
                old_players[j] = players[j];
            }
            for (j=0; j<=players[0].id; j++) {
                if (is_int_in_array(players[j].id, weekly_players)) {
                    player_update(&players[j]);
                    player_remove_opponents(&players[j]);
                    fprintf(out, "%i,%i,%i,%i\n",
                                last_date, players[j].id, (int) player_get_rating(players[j]), (int) player_get_deviation(players[j]));
                    fflush(out);
                } else {
                    player_dnc(&players[j]);
                }
            }
            for (j=0; j<=weekly_players[0]; j++) {
                weekly_players[j] = 0;
            }
            for (j=0; j<=players[0].id; j++) {
                old_players[j] = players[j];
            }
        }

        for (j=0; j<=players[0].id; j++) {
            if (players[j].id == matches[i].winner) {
                a = j;
            }
            if (players[j].id == matches[i].loser) {
                b = j;
            }
        }

        player_add_opponent(&players[a], &old_players[b], 1.0);
        player_add_opponent(&players[b], &old_players[a], 0.0);

        if (!is_int_in_array(player_ids[a], weekly_players)) {
            weekly_players[0] += 2;
            weekly_players[weekly_players[0] - 1] = player_ids[a];
            weekly_players[weekly_players[0]] = player_ids[b];
        } else {
            if (!is_int_in_array(player_ids[b], weekly_players)) {
            weekly_players[0]++;
            weekly_players[weekly_players[0]] = player_ids[b];
            }
        }

        last_date = matches[i].date;
    }

    for (j=0; j<=weekly_players[0]; j++) {
        for (k=0; k<=players[0].id; k++) {
            if (weekly_players[j] == players[k].id) {
                fprintf(out, "%i,%i,%i,%i\n",
                    last_date, players[k].id, player_get_rating(players[k]), player_get_deviation(players[k]));
            }
        }
    }
    
    free(player_ids);
    free(players);
    free(old_players);
    free(weekly_players);
    free(matches);
    fclose(out);

    printf("%f\n", ((double) (clock() - start)) / CLOCKS_PER_SEC);

    return 0;
}