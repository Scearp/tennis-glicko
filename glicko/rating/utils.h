#ifndef UTILS_H
#define UTILS_H

#include "defines.h"

int is_int_in_array(int n, int array[]);
int *read_csv(char *filename);
int *get_players(int *raw_data);
match *get_matches(int *raw_data);

double player_get_rating(glicko_player player);
double player_get_deviation(glicko_player player);

void player_prepare(glicko_player player);
void remove_int_from_array(int player_id, int array[]);
void remove_player_from_array(int player_id, glicko_player array[]);

double player_g(glicko_player opponent);
double player_expected(glicko_player player, glicko_player opponent);
double player_v(glicko_player player, glicko_player opponents[]);
double player_delta(glicko_player player, glicko_player opponents[], double outcomes[], double v);
double player_new_volatility(glicko_player player, glicko_player opponents[], double outcomes[], double v);

void player_update(glicko_player *player);
void player_dnc(glicko_player *player);

void player_add_opponent(glicko_player *player, glicko_player *opponent, double outcome);
void player_remove_opponents(glicko_player *player);

#endif