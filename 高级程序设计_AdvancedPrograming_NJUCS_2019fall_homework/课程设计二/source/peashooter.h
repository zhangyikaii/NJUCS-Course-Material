#pragma once

#include "common.h"


class bullet {
public:
	bullet(int birPos, int who, int curTime) : myPos(birPos), whoAmI(who), birthday(curTime), speed(BULLET_SPEED) {
		ame[0] = "      ";
		ame[1] = "  G>  ";
		ame[2] = " GGG> ";
		ame[3] = "  G>  ";
		ame[4] = "      ";
		ame[5] = "      ";

		bme[0] = "      ";
		bme[1] = "  BB> ";
		bme[2] = "      ";
		bme[3] = "  BB> ";
		bme[4] = "      ";
		bme[5] = "      ";

		cme[0] = "      ";
		cme[1] = " D  D ";
		cme[2] = "  DD  ";
		cme[3] = " D  D ";
		cme[4] = "      ";
		cme[5] = "      ";
	}

	// 子弹不可能停住, 所以可以用这样方式更新位置.
	int getPos(int curTime) {
		return (int)floor((double)myPos + speed * (double)(curTime - birthday));
	}

	string *getMe() {
		if (whoAmI == 0) {
			return ame;
		}
		else if (whoAmI == 1)
			return bme;
		return cme;
	}

	int& getWhoAmI() {
		return whoAmI;
	}

	virtual int getHurt() {
		return (whoAmI + 1) * 2;
	}

private:
	string ame[BIO_SIZE], bme[BIO_SIZE], cme[BIO_SIZE];
	int myPos, birthday;
	int whoAmI;
	double speed;
};

class peashooter {
public:
	peashooter(int fiPos, int curTime) : blood(BLOOD_SHOW), fixedPos(fiPos), birthday(curTime), befBullTime(curTime), isGT(false), isHP(false), attack(0) {
		me1[0] = "   PEA";
		me1[1] = " SHOOT";
		me1[2] = "  %%  ";
		me1[3] = " %  <=";
		me1[4] = "  %%  ";
		me1[5] = "$$$$$$";

		me2[0] = "   PEA";
		me2[1] = " SHOOT";
		me2[2] = "  %%  ";
		me2[3] = " %  >>";
		me2[4] = "  %%  ";
		me2[5] = "$$$$$$";
	}

	virtual string* getMe(int curTime) {
		if (curTime - befBullTime > EMIS_FREQ) {
			// 产生一个子弹.
			befBullTime = curTime;
			bullVec.push_back(bullet(fixedPos + 6, 0, curTime));
		}
		
		string *ret = (rand() % 2) == 0 ? me1 : me2;
		for (int i = 0; i < BLOOD_SHOW - int(blood); ++i) {
			ret[5][i] = ' ';
		}

		return ret;
	}

	int getHurt(double hurtVol = PEA_BLOOD_HURT) {
		blood -= hurtVol;
		if (blood < 0.1)
			return -1;
		return 0;
	}

	int getPos() {
		return fixedPos;
	}

	double& getAttack() {
		return attack;
	}

	vector<bullet> bullVec;
	bool isGT, isHP;

protected:
	string me1[BIO_SIZE], me2[BIO_SIZE];

	int birthday;
	int fixedPos;

	int befBullTime;

	double blood;
	double attack;
};


class snowpeashooter : public peashooter {
public:
	snowpeashooter(int fiPos, int curTime) : peashooter(fiPos, curTime) {
		me1[0][2] = 'S';
		me1[0][3] = 'N';
		me1[0][4] = 'O';
		me1[0][5] = 'W';

		me2[0][2] = 'S';
		me2[0][3] = 'N';
		me2[0][4] = 'O';
		me2[0][5] = 'W';
	}
	string* getMe(int curTime) {
		if (curTime - befBullTime > SNOW_EMIS_FREQ) {
			// 产生一个子弹.
			befBullTime = curTime;
			bullVec.push_back(bullet(fixedPos + 6, 2, curTime));
		}


		string* ret = (rand() % 2) == 0 ? me1 : me2;
		for (int i = 0; i < BLOOD_SHOW - int(blood); ++i) {
			ret[5][i] = ' ';
		}
		return ret;
	}
};

class GT : public peashooter {
public:
	GT(int fiPos, int curTime) : peashooter(fiPos, curTime) {
		isGT = true;
		blood *= 2;
		attack = GT_HURT;
		mee[0] = " >   G";
		mee[1] = "  >  T";
		mee[2] = "   >> ";
		mee[3] = "  >   ";
		mee[4] = " >    ";
		mee[5] = "$$$$$$";
	}

	string* getMe(int curTime) {
		for (int i = 0; i < BLOOD_SHOW - int(blood); ++i) {
			mee[5][i] = ' ';
		}

		return mee;
	}
private:
	string mee[BIO_SIZE];
};


class NW : public peashooter {
public:
	NW(int fiPos, int curTime) : peashooter(fiPos, curTime) {
		mee[0] = "   NUT";
		mee[1] = "  WALL";
		mee[2] = " oooo ";
		mee[3] = " O  O ";
		mee[4] = " 0000 ";
		mee[5] = "$$$$$$";

		blood *= 4;
	}

	string* getMe(int curTime) {
		for (int i = 0; i < BLOOD_SHOW - int(blood / 18.0 * 6.0); ++i) {
			mee[5][i] = ' ';
		}

		return mee;
	}
private:
	string mee[BIO_SIZE];
};


class PK : public peashooter {
public:
	PK(int fiPos, int curTime) : peashooter(fiPos, curTime) {
		attack = GT_HURT * 10;
		mee[0] = "  PUMP";
		mee[1] = "   KIN";
		mee[2] = "  oo  ";
		mee[3] = " |  | ";
		mee[4] = " ==== ";
		mee[5] = "$$$$$$";

		blood = 0.6;	// 血很脆, 攻擊很強.
	}

	string* getMe(int curTime) {
		for (int i = 0; i < BLOOD_SHOW - int(blood / 0.6 * 6.0); ++i) {
			mee[5][i] = ' ';
		}
		return mee;
	}
private:
	string mee[BIO_SIZE];
};

class HP : public peashooter {
public:
	HP(int fiPos, int curTime) : peashooter(fiPos, curTime) {
		isHP = true;
		mee[0] = "  HOT ";
		mee[1] = "PEPPER";
		mee[2] = "  |   ";
		mee[3] = " | |  ";
		mee[4] = "| | | ";
		mee[5] = "oooooo";

	}

	string* getMe(int curTime) {
		return mee;
	}
private:
	string mee[BIO_SIZE];
};

class doublepeashooter : public peashooter {
public:
	doublepeashooter(int fiPos, int curTime) : peashooter(fiPos, curTime) {
		me1[0][2] = 'D';
		me1[0][3] = 'O';
		me1[0][4] = 'U';
		me1[0][5] = 'B';

		me2[0][2] = 'D';
		me2[0][3] = 'O';
		me2[0][4] = 'U';
		me2[0][5] = 'B';
	}
	string* getMe(int curTime) {
		if (curTime - befBullTime > EMIS_FREQ) {
			// 产生一个子弹.
			befBullTime = curTime;
			bullVec.push_back(bullet(fixedPos + 6, 1, curTime));
		}
		string* ret = (rand() % 2) == 0 ? me1 : me2;
		for (int i = 0; i < BLOOD_SHOW - int(blood); ++i) {
			ret[5][i] = ' ';
		}
		return ret;
	}
};

