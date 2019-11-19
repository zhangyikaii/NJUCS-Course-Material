#ifndef lol_ai_mc_h
#define lol_ai_mc_h

#include "reversi.h"

typedef struct {
    Point pos;
    double rateBlack;
    double rateWhite;
} AI_Data_Stru;

typedef struct {
    int countTry, countWinBlack, countWinWhite;
    AI_Data_Stru* data;
    const Reversi* orig;
} AI_Thread_Data;


#endif
