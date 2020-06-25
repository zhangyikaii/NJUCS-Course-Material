//
//  main.cpp
//  ReversiClient
//
//  Created by ganjun on 2018/3/5.
//  Copyright © 2018年 ganjun. All rights reserved.
//

#include "Rreversii.h"

Reversi r;
Menu m;

int main() {
	srand((unsigned int)time(NULL));
	cuiTop(&m);
	r_init(&r);

    Rreversii reversi = Rreversii();
    reversi.gameStart();

	system("pause");
    return 0;
}
