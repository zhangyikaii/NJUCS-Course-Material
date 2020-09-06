#pragma once

#include <bits/stdc++.h>
#include <Windows.h>
#include <conio.h>

using namespace std;

extern HANDLE hOutput;
extern COORD coord;
extern CONSOLE_CURSOR_INFO CursorInfo;

typedef long long ll;

#define For(i, a, b) for(int i = a; i < b; ++i)
#define MAX_DISP_NUM 5
#define MAX_DISP_ROW 11
#define MAX_DISP_LINE 42
#define LEARNING_WORD_POS 5
#define START_TIPS_NUM 3
#define EVERYDAY_LEARN_INIT 5
enum UI_TYPE {
	LEARNING = 0,
	START
};

enum {
	KNOW = 1,
	VAGUE = 3,
	UNKNOWN = 4,
	FORGOT = 5
};