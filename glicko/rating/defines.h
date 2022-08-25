#ifndef DEFINES_H
#define DEFINES_H

#define TAU 0.5
#define PI 3.1415926535897

typedef struct match {
    int date, winner, loser;
} match; 

typedef struct glicko_player {
    int id, inactive, has_played;
    double rating, deviation, volatility;
    double *outcomes;
    struct player_tuple *opponents;
} glicko_player;

typedef struct player_tuple {
    int id;
    double rating, deviation, volatility;
} player_tuple;

#endif