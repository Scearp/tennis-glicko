#ifndef DEFINES_H
#define DEFINES_H

#define TAU 0.5
#define PI 3.1415926535897

typedef struct match {
    int date, winner, loser, mode;
} match; 

typedef struct glicko_player {
    int id;
    double rating, deviation, volatility;
    double *outcomes;
    struct glicko_player *opponents;
} glicko_player;

#endif