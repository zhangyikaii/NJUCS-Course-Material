#pragma once

#include "common.h"

class zombie {
public:
	zombie(int curTime) : speed(ZOMBIE_SPEED), fixedTime(-1), befPos(LINE - 1), birthday(curTime), callNum(0), lastTime(curTime) {
		myPos = LINE - 1;
		live = ZOMBIE_LIVE;

		me1[0] = "     Z";
		me1[1] = "**** O";
		me1[2] = "|..| M";
		me1[3] = "|__| B";
		me1[4] = " ||  I";
		me1[5] = "$$$$$$";
		
		
		me2[0] = " **  Z";
		me2[1] = "*  * O";
		me2[2] = "|..| M";
		me2[3] = "|__| B";
		me2[4] = " ||  I";
		me2[5] = "$$$$$$";
	}

	// 寒冰射手射出之后冻住zombie
	void setFixed(int curTime) {
		fixedTime = curTime + SNOW_FIXED_TIME;

		speed = 0;
	}

	// 传进来当前行的铲子矩阵, 看看当前行这个位置有没有植物.
	int getPos(int curTime, ShovelStruct shovelArrLine[], int &plantHurt) {
		//if (curTime < fixedTime)
		//	return befPos;
		//return floor((double)myPos + speed * (double)(birthday - curTime));


		// 解除fixed.
		if (speed == 0 && curTime > fixedTime)
			speed = ZOMBIE_SPEED * 1.3;			// 解除后加速

		// DONE zombie 碰到植物要静止.
		if (myPos < 140 && shovelArrLine[int(myPos / PER_SOIL_LINE)].id != -1) {
			plantHurt = int(myPos / PER_SOIL_LINE);
			lastTime = curTime;
			// 相当于speed = 0, 没有走返回, 因为已经碰到了植物.
			return (int)myPos;
		}


		myPos += (double)(lastTime - curTime) * speed;

		lastTime = curTime;
		return int(myPos);
	}

	virtual string* getMe() {
		string* ret = NULL;
		++callNum;
		if ((callNum / ZOMBIE_HAIR_REFRESH_RATE) % 2)
			ret = me1;
		else
			ret = me2;


		for (int i = 0; i < BLOOD_SHOW - int(double(live) / ZOMBIE_LIVE * 6.0); ++i) {
			ret[5][i] = ' ';
		}
		

		return ret;
	}

	// 返回 1 => kill the zombie
	int minusLive(double minu) {
		live -= minu;
		if (live <= 0)
			return 1;
		return 0;
	}

	// 换一种fixed的方式, 通过改变当前速度, 每次更新位置通过 + speed * (与上次调用时间差值).
	//void setFixed(int curTime) {
	//	fixedTime = curTime + SNOW_FIXED_TIME;
	//	befPos = getPos(curTime);
	//}
	virtual bool isClo() {
		return false;
	}

protected:
	double live;
	string me1[10], me2[10];
	double speed;
	int callNum;

private:
	time_t birthday;
	double myPos;

	int fixedTime, befPos;


	int lastTime;
};

class RoadblockZB : public zombie {
public:
	RoadblockZB(int curTime) : zombie(curTime) {
		live *= 1.3;
		speed *= 1.15;
		For(i, 0, 4) {
			me1[1][i] = '^';
		}
		me2[1][0] = '^';
		me2[1][3] = '^';
		me2[0][1] = '^';
		me2[0][2] = '^';
	}
};


class BucketZB : public zombie {
public:
	BucketZB(int curTime) : zombie(curTime) {
		live *= 1.4;
		speed *= 1.5;

		me1[0] = "     Z";
		me1[1] = "---- O";
		me1[2] = "|..| M";
		me1[3] = "---- B";
		me1[4] = "     I";
		me1[5] = "$$$$$$";


		me2[0] = " --  Z";
		me2[1] = "-  - O";
		me2[2] = "|..| M";
		me2[3] = "|__| B";
		me2[4] = " ||  I";
		me2[5] = "$$$$$$";
	}
};


class FlagZB : public zombie {
public:
	FlagZB(int curTime) : zombie(curTime) {
		speed *= 1.7;

		me1[0] = "FLAG Z";
		me1[1] = " **  O";
		me1[2] = "  /--M";
		me1[3] = " /__|B";
		me1[4] = "/    I";
		me1[5] = "$$$$$$";


		me2[0] = "FLAG Z";
		me2[1] = "*  * O";
		me2[2] = "|--- M";
		me2[3] = "|__| B";
		me2[4] = "|    I";
		me2[5] = "$$$$$$";

		mee[0] = " %%  Z";
		mee[1] = "%  % O";
		mee[2] = "|..| M";
		mee[3] = "\\__/ B";
		mee[4] = " ||  I";
		mee[5] = "$$$$$$";

		initLive = live / 2;
	}

	string* getMe() {
		string* ret = NULL;
		++callNum;
		if ((callNum / ZOMBIE_HAIR_REFRESH_RATE) % 2)
			ret = me1;
		else
			ret = me2;

		if (live < initLive) {
			ret = mee;
		}

		for (int i = 0; i < BLOOD_SHOW - int(double(live) / ZOMBIE_LIVE * 6.0); ++i) {
			ret[5][i] = ' ';
		}

		return ret;
	}

private:
	string mee[BIO_SIZE];
	double initLive;
};


class DoorZB : public zombie {
public:
	DoorZB(int curTime) : zombie(curTime) {
		live *= 1.5;
		speed *= 1.5;

		me1[0] = "DOOR Z";
		me1[1] = " **  O";
		me1[2] = "/..\\ M";
		me1[3] = "\\__/ B";
		me1[4] = "     I";
		me1[5] = "$$$$$$";


		me2[0] = "DOOR Z";
		me2[1] = "*  * O";
		me2[2] = "|..| M";
		me2[3] = "\\__/ B";
		me2[4] = "     I";
		me2[5] = "$$$$$$";
	}
};




class ClownZB : public zombie {
public:
	ClownZB(int curTime) : zombie(curTime) {
		speed *= 1.1;
		live *= 1.7;

		me1[0] = " %%  Z";
		me1[1] = "%  % O";
		me1[2] = "%..% M";
		me1[3] = "$__% B";
		me1[4] = " ||  I";
		me1[5] = "$$$$$$";


		me2[0] = "     Z";
		me2[1] = "%%%% O";
		me2[2] = "%..% M";
		me2[3] = "$__% B";
		me2[4] = " ||  I";
		me2[5] = "$$$$$$";
	}

	bool isClo() {
		return true;
	}
};



struct CmpZomPos {
	int pos;
	int id;

	CmpZomPos(int p, int t) : pos(p), id(t) { }

	bool operator<(const CmpZomPos& tmp) const {
		return tmp.pos < pos;
	}
};

