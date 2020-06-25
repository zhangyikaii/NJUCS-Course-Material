#include <stdio.h>
#include <time.h>
#include "ai_mc.h"
#include <stdlib.h>
#include "reversi.h"
#include "Rreversii.h"

#include "cui.h"

//#define _OSX

#include <Windows.h>



//int g_tryCount;
extern int g_tryCount;

void benchmark() {
    const long baseline = 2428500; // Mac mini Late 2012 (clang -O4) [microsecond]
    
    int blackhole;
    unsigned long result;
    Reversi board;
    unsigned long start, end;

    
    double rate;
    
    printf("benchmark() : Wait a moment...\n");
    
    srand(353535);
    
    r_init(&board);
    
    start = GetTickCount();

    step(&board, &blackhole, &blackhole);

	end = GetTickCount();

    
    result = (end - start) * 1000;

    
	printf("%d", result);
    rate = (double)baseline / result;
    
    g_tryCount *= rate;
    
    printf("benchmark() : Baseline %ld / Your system %ld => %f\n", baseline, result, rate);
    
    if (rate < 0.8) {
        printf("\n[WARNING] Your system is too slow! [WARNING]\n");
        printf("Tips : Compile with optimize option. (ex cl /O2 *.c\n\n");

    }
    
    printf("benchmark() : Let's start!\n\n");
}

void cuiTop(Menu* m)
{   
    m->isBlackPlayer = -1;
    m->isWhitePlayer = -1;
        
//#ifdef _DEBUG
//    printf("!!! Debug Mode !!!\n");
//
    
    //benchmark();
    
	// 这里处理先手后手 要传参数到RoundStart里面改掉!   

	m->AI = 0;

	// 开启了benchmark()用
	//g_tryCount = g_tryCount * 3 / 2;

	// 未开启时自己设置
	g_tryCount = 19900;
}

