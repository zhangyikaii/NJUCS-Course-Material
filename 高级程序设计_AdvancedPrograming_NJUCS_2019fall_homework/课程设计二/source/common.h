#pragma once

#include <bits/stdc++.h>
#include <Windows.h>
#include <conio.h>

using namespace std;

extern HANDLE hOutput;
extern COORD coord;
extern CONSOLE_CURSOR_INFO CursorInfo;

typedef long long ll;

#define ROW 50
#define LINE 180
#define PLINE 200

// 对于全地图, 纵向有5块地, 横向7块
#define PER_MAP_ROW 5
#define PER_MAP_LINE 7

// 每块地的行内纵向有6格, 横向20格.
#define PER_SOIL_ROW 6
#define PER_SOIL_LINE 20

#define MAX_BIOLOGY 100
#define For(x, a, b) for(int x=a;x<b;++x)
#define asoil(a,b,c) (soil[a].l[b][c])
#define rsoil(a,b) (soil[a].l[b])
#define beginsoil(a,b) (soil[a].l[b*20][0])

// 生物是6格*6格的.
#define BIO_SIZE 6

// video的最大帧数.
#define MYFRAME_NUM 500

// 各种video的帧数
#define VSTART_FRAME 235
#define VNEWRECORD_FRAME 237
#define VPAUSE_FRAME 269
#define VSHOP_FRAME 230
#define VEND_FRAME 213
#define VINSHOP_FRAME 143

#define VMAX_FRAME 500

#define REFRESHRATE 30

#define GENE_SUN_GAP 10

#define SOIL_LINE 140

#define USER_INIT_MONEY 1000

#define SCORE_BOARD_ROW 23

#define ZOMBIE_LIVE 20
#define EMIS_FREQ 70
#define SNOW_EMIS_FREQ 50

#define SNOW_FIXED_TIME 25

#define BULLET_SPEED 1

#define ZOMBIE_HAIR_REFRESH_RATE 4

#define ZOMBIE_SPEED 0.15

#define BLOOD_SHOW 6

#define SUN_BLOOD_HURT 0.15

#define PEA_BLOOD_HURT 0.02
#define GT_GET_HURT 0.02
#define GT_HURT 0.6

#define SUN_PER_ENERGY_PRO 0.01

#define ROW_MARK '-'
#define LINE_MARK '^'


enum {
	MYESC = 0,
	MYGOON,
	MYPAUSE
};

enum WHO {
	SUNF = 0,
	PEAS
};

struct ShovelStruct {
	WHO who;
	int id;
	// id = -1 表示当前地块为空.
	ShovelStruct() : id(-1) { }
	ShovelStruct(WHO w, int i) : who(w), id(i) { }
};

struct TestModeStruct {
	int t, bWhat = 0;
	int xPl = 0, yPl = 0;

	TestModeStruct(int ti, int bW, int xP, int yP) : t(ti), bWhat(bW), xPl(xP), yPl(yP) { }
};

