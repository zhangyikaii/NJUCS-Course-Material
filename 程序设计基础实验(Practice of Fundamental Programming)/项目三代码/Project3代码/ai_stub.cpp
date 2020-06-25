#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ai_stub.h"

void AI_Stub(const Reversi* r, int* x, int* y)
{
    int i = rand() % r->countCanSet;
    
    if (r->countCanSet == 0) {
        printf("AI_Stub() Error.\n");
        exit(EXIT_FAILURE);
    }
    
    *x = r->canSet_[i].x;
    *y = r->canSet_[i].y;
}