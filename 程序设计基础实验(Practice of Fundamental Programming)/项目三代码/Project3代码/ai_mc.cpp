#include "Rreversii.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ai_stub.h"
#include "ai_mc.h"
using namespace std;


int g_tryCount = 30000;

//extern int g_tryCount;

#define MAX_THREADS 32

//#define _OSX

#pragma message ("LoLoLoLo for Windows (You will need to define _OSX on Mac OS X)")
#include <Windows.h>


int getCpuCount() {
    int count;
    SYSTEM_INFO info;
    GetSystemInfo(&info);
    count = (int)info.dwNumberOfProcessors;

    return count;
}

DWORD WINAPI AI_MC_Thread(void* args)

{
    int j, x_, y_;
    Reversi tmp;
    AI_Thread_Data* output = (AI_Thread_Data*)args;
    
    for (j = 0; j < output->countTry; j++) {
        
        tmp = *output->orig;
        
        r_set(&tmp, tmp.current_, output->data->pos.x, output->data->pos.y);
        
        while (tmp.current_ != None) {
            AI_Stub(&tmp, &x_, &y_);
            r_set(&tmp, tmp.current_, x_, y_);
        }
        
        if (tmp.countBlack > tmp.countWhite) {
            output->countWinBlack++;
        } else if (tmp.countWhite > tmp.countBlack) {
            output->countWinWhite++;
        }
    }
    
    return 0;
}

int qsort_black(const void *a, const void *b)
{
    AI_Data_Stru *cc, *dd;
    cc = (AI_Data_Stru*)a;
    dd = (AI_Data_Stru*)b;
    
    if (cc->rateBlack > dd->rateBlack) {
        return -1;
    } else if(cc->rateBlack < dd->rateBlack) {
        return 1;
    } else {
        return 0;
    }
}

int qsort_white(const void *a, const void *b)
{
    AI_Data_Stru *cc, *dd;
    cc = (AI_Data_Stru*)a;
    dd = (AI_Data_Stru*)b;
    
    if (cc->rateWhite > dd->rateWhite) {
        return -1;
    } else if(cc->rateWhite < dd->rateWhite) {
        return 1;
    } else {
        return 0;
    }
}



pair<int, int> step(const Reversi* r, int *x, int *y)
{
	if (r->countCanSet == 0)
	{
		return make_pair(-1, -1);
	}

    AI_Data_Stru data[30] = {0}, best;
    int countWinBlack, countWinWhite, i, t, cpu;
    AI_Thread_Data threadData[MAX_THREADS];
	HANDLE thread[MAX_THREADS];
    cpu = getCpuCount();
	//printf("cpu: %d\n", cpu);
    if (cpu > MAX_THREADS) cpu = MAX_THREADS;
    
    for (i = 0; i < r->countCanSet; i++) {
        countWinBlack = 0;
        countWinWhite = 0;
        
        data[i].pos = r->canSet_[i];
        
        memset(threadData, 0, sizeof(threadData));
        
        for (t = 0; t < cpu; t++) {
            threadData[t].countTry = g_tryCount / cpu;
            if (g_tryCount % cpu != 0 && i == cpu - 1) threadData[t].countTry += g_tryCount % cpu;
            
            threadData[t].data = &data[i];
            threadData[t].orig = r;
			thread[t] = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)AI_MC_Thread, &threadData[t], 0, NULL);
        }
        
        for (t = 0; t < cpu; t++) {
			WaitForSingleObject(thread[t], INFINITE);
            countWinBlack += threadData[t].countWinBlack;
            countWinWhite += threadData[t].countWinWhite;
        }
        
        data[i].rateBlack = (double)countWinBlack / g_tryCount;
        data[i].rateWhite = (double)countWinWhite / g_tryCount;
        
        printf("STEP(%d) (%d,%d) B %f / W %f\n", g_tryCount, data[i].pos.y, data[i].pos.x, data[i].rateBlack, data[i].rateWhite);
    }
    
    switch (r->current_) {
        case Black:
            qsort(data, r->countCanSet, sizeof(AI_Data_Stru), qsort_black);
            break;
            
        case White:
            qsort(data, r->countCanSet, sizeof(AI_Data_Stru), qsort_white);
            break;
            
        case None:
            break;
    }
    
    best = data[0];
    
    *x = best.pos.x;
    *y = best.pos.y;
    
    printf("STEP(%d) (%d,%d) B %f / W %f [Best!]\n", g_tryCount, best.pos.y, best.pos.x, best.rateBlack, best.rateWhite);
	return make_pair(best.pos.y, best.pos.x);
}