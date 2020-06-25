#ifndef lol_reversi_h
#define lol_reversi_h

typedef enum {
    None,
    Black,
    White
} Disk;

typedef struct {
    int x;
    int y;
} Point;

typedef struct {
    char board_[8][8];
    Point canSet_[30];
    Disk current_;
    
    int countTurn;
    int countCanSet;
    int countBlack;
    int countWhite;
} Reversi;

Point p_add(Point a, Point b);
Point p_sub(Point a, Point b);
Point p_set(int x, int y);
int p_cmp(const Point* a, const Point* b);

void r_init(Reversi* r);
void r_dump(const Reversi* r);
int r_scan(Reversi* r);
void r_flip(Reversi* r, int x, int y);
int r_set(Reversi* r, Disk d, int x, int y, bool isRand = false);

#endif
