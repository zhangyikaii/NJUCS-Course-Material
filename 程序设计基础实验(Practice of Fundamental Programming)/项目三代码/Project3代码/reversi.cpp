#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "reversi.h"

//#define _DEBUG
const Point dir[8] = { { 0, 1 }, { 1, 1 }, { 1, 0 }, { 1, -1 }, { 0, -1 }, { -1, -1 }, { -1, 0 }, { -1, 1 } };
int befX = -1, befY = -1;


Point p_add(Point a, Point b)
{
    Point res;
    
    res = a;
    res.x += b.x;
    res.y += b.y;
    
    return res;
}

Point p_sub(Point a, Point b)
{
    Point res;
    
    res = a;
    res.x -= b.x;
    res.y -= b.y;
    
    return res;
}

Point p_set(int x, int y)
{
    Point res;
    
    res.x = x;
    res.y = y;
    
    return res;
}

int p_cmp(const Point* a, const Point* b) {
    if (memcmp(a, b, sizeof(Point)) == 0) return 1;
    return 0;
}

void r_init(Reversi* r)
{
    memset(r->board_, 0, sizeof(r->board_[0][0]) * 64);
    memset(r->canSet_, 0, sizeof(r->canSet_));
    
    r->current_ = Black;
    r->countTurn = 1;
    
	r->board_[3][3] = Black;
	r->board_[4][3] = White;
	r->board_[3][4] = White;
	r->board_[4][4] = Black;
    
    r->countBlack = 2;
    r->countWhite = 2;
    
    r_scan(r);
}

void r_dump(const Reversi* r)
{
    int x, y, i;
    char overlay[8][8] = {0};
    
    for (i = 0; i < r->countCanSet; i++) {
        overlay[r->canSet_[i].x][r->canSet_[i].y] = 1;
    }
    
    printf("===== Turn %2d =====\n", r->countTurn);
    
    printf(" %c ", r->current_ == Black ? 'B' : 'W');
    
    for (i = 0; i < 8; i++) {
        printf("%d ", i);
    }
    
    printf("\n");
    
    for (y = 0; y < 8; y++) {
        printf(" %d ", y);
        
        for (x = 0; x < 8; x++) {
            switch (r->board_[x][y]) {
                case None:
                    if (overlay[x][y] == 1) {
                        printf("* ");
                    } else {
                        printf(". ");
                    }
                    break;
                case Black:
                    printf("B ");
                    break;
                case White:
                    printf("W ");
                    break;
            }
        }
        
        printf("\n");
    }
    
    printf("=== B %2d / W %2d ===\n", r->countBlack, r->countWhite);
    
    printf("\n");
}


// 更改并返回有多少个可以放的以及计算其他一些参数
int r_scan(Reversi* r)
{
    int count = 0, x, y, i, flag, bench = 0;
    Point cur;
    
    r->countBlack = (r->countWhite = 0);
    

    for (y = 0; y < 8; y++) {
        for (x = 0; x < 8; x++)	{
            bench++;
            
            if (r->board_[x][y] == Black) {
                r->countBlack++;
                continue;
            } else if (r->board_[x][y] == White) {
                r->countWhite++;
                continue;
            }

			// 如果黑棋下完白棋没地方下 然后黑棋下 黑棋旁边算不算禁手 就在这里改
			if (befX != -1 && befY != -1 && (x == befX && y == befY + 1) || (x == befX && y == befY - 1)
				|| (x == befX + 1 && y == befY) || (x == befX - 1 && y == befY))
				continue;

			// 判断八个方向有没有可以放的
            for (i = 0; i < 8; i++) {
                cur = p_set(x, y);
                flag = 0;
                
                for (;;) {
                    bench++;
                    cur = p_add(cur, dir[i]);
                    
                    if (cur.x < 0 || cur.y < 0 || cur.x >= 8 || cur.y >= 8) {
                        break;    // Out of bounds.
                    }
                    if (r->board_[cur.x][cur.y] == None) {
                        break;    // Free
                    }
                    if (!flag && r->board_[cur.x][cur.y] == r->current_) {
                        break;    // LoL
                    }
                    
                    if (flag && r->board_[cur.x][cur.y] == r->current_)
					{
						r->canSet_[count] = p_set(x, y);
						count++;

						flag = -1;

						break;
						
                    }
                    
                    if (r->board_[cur.x][cur.y] == (r->current_ == Black ? White : Black)) {
                        flag++;
                    }
                }
                
                if (flag == -1) {
                    break;
                }
            }
        }
    }
    
    r->countCanSet = count;
    
//#ifdef _BENCHMARK
//    printf("\t\t\t\t\t\t\tr_scan() count = %d / bench = %d\n", count, bench);

    
    return count;
}

void r_flip(Reversi* r, int x, int y)
{
    const Point dir[8] = {{0, 1}, {1, 1}, {1, 0}, {1, -1}, {0, -1}, { -1, -1}, { -1, 0}, { -1, 1}};
    int i, flag, bench = 0;
    Point cur;
    
    for (i = 0; i < 8; i++) {
        cur = p_set(x, y);
        flag = 0;
        
        for (;;) {
            bench++;
            cur = p_add(cur, dir[i]);
            
            if (cur.x < 0 || cur.y < 0 || cur.x >= 8 || cur.y >= 8) {
                break;    // Out of bounds.
            }
            if (r->board_[cur.x][cur.y] == None) {
                break;    // Free
            }
            if (!flag && r->board_[cur.x][cur.y] == r->current_) {
                break;    // LoL
            }
            
            if (flag && r->board_[cur.x][cur.y] == r->current_) {
                cur = p_sub(cur, dir[i]);
                
                do {
                    r->board_[cur.x][cur.y] = r->current_;
                    cur = p_sub(cur, dir[i]);
                    bench++;
                } while (r->board_[cur.x][cur.y] != r->current_);
                break;
            }
            
            if (r->board_[cur.x][cur.y] == (r->current_ == Black ? White : Black)) {
                flag++;
            }
        }
    }
    
//#ifdef _BENCHMARK
//    printf("\t\t\t\t\t\t\tr_flip() bench = %d\n", bench);

    
}

int r_set(Reversi* r, Disk d, int x, int y, bool isRand)
{
	/*if (r->current_ == None || x == -1 && y == -1)
	{
		r->current_ = NoneColor;
		return -1;
	}*/

	if (x == -1 && y == -1)
	{
		r->current_ = (r->current_ == Black ? White : Black);
		r_scan(r);
		r->countTurn++;
		return 1;
	}


	int i = 0;
	
	if (r->current_ != d) {
		printf("r_set : It's not your turn.\n");
		//exit(EXIT_FAILURE);

		return -1;
	}

	if (r->board_[x][y] != None) {
		printf("r_set : It seems like that (%d,%d) is already using.\n", x, y);
		//exit(EXIT_FAILURE);

		return -1;
	}

	for (i = 0; i < r->countCanSet; i++) {
		if (r->canSet_[i].x == x && r->canSet_[i].y == y) {

			r->board_[x][y] = r->current_;

			r_flip(r, x, y);

			r->current_ = (r->current_ == Black ? White : Black);

			if (isRand == false && r_scan(r)== 0) { // Skip?
				r->current_ = (r->current_ == Black ? White : Black);

				if (isRand == false && r_scan(r) == 0) { // Game Over
					r->current_ = None;

					return 1;
				}
			}

			if (isRand == true)
				r_scan(r);

			r->countTurn++;

			return 1;
		}
	}
//
//#ifdef _DEBUG
//	printf("r_set : (%d,%d) can't be set.\n", x, y);
//	exit(EXIT_FAILURE);
//

	return -1;
}