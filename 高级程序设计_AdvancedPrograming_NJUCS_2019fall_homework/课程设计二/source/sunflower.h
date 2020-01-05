#pragma once

#include "common.h"

class sunflower {
public:
	sunflower(int birPos, int curTime) : myPos(birPos), birthday(curTime), blood(BLOOD_SHOW) {
		me1[0] = "   SUN";
		me1[1] = "FLOWER";
		me1[2] = "  @@  ";
		me1[3] = " @  @ ";
		me1[4] = "  @@  ";
		me1[5] = "OOOOOO";

		me2[0] = "   SUN";
		me2[1] = "FLOWER";
		me2[2] = " @@@@ ";
		me2[3] = "@    @";
		me2[4] = " @@@@ ";
		me2[5] = "OOOOOO";
	}

	int getPos() {
		return myPos;
	}

	string* getMe(int curTime, bool isHaveLetter = false) {
		// TODO 更新随机字母(阳光) 以及 是否需要返回带有字母的.
		string* me = (rand() % 2) == 0 ? me1 : me2;
		if ((curTime - birthday) % GENE_SUN_GAP == 0)
			letter = rand() % 26 + 'A';

		if (isHaveLetter == true) {
			me[3][2] = letter;
		}
		else {
			me[3][2] = ' ';
		}

		for (int i = 0; i < BLOOD_SHOW - int(blood); ++i) {
			me[5][i] = ' ';
		}

		return me;
	}

	int getHurt(double hurtVol = SUN_BLOOD_HURT) {
		blood -= hurtVol;
		if (blood < 0.1)
			return -1;
		return 0;
	}

private:
	string me1[10], me2[10];
	char letter;
	time_t birthday;
	int myPos;

	double blood;
};

