#ifndef lol_cui_h
#define lol_cui_h

typedef struct {
    int isBlackPlayer;
    int isWhitePlayer;
    int AI;
} Menu;

void cuiTop(Menu* m);
void cuiPlaying(int* x, int* y);

#endif
