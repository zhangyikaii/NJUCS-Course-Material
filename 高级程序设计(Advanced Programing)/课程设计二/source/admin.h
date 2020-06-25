#pragma once
#include "peashooter.h"
#include "zombie.h"
#include "sunflower.h"
#include "common.h"
#include "linemap.h"
#include "video.h"


// DONE zombie 的血量实时显示.

class obj {
public:
	vector<zombie*> mZom;
	vector<sunflower*> mSun;
	vector<peashooter*> mPea;

	void hurtZombie(int hurtBlood, int id) {
		if (mZom[id]->minusLive(hurtBlood) == 1) {
			delete mZom[id];
			mZom.erase(mZom.begin() + id);
		}
	}


	ShovelStruct peaNew(const int& y, const int& curTime) {
		peashooter* p = new peashooter(y, curTime);
		mPea.push_back(p);
		return ShovelStruct(PEAS, mPea.size() - 1);
	}


	ShovelStruct snowpeaNew(const int& y, const int& curTime) {
		peashooter* p = new snowpeashooter(y, curTime);
		mPea.push_back(p);
		return ShovelStruct(PEAS, mPea.size() - 1);
	}

	ShovelStruct GTNew(const int& y, const int& curTime) {
		peashooter* p = new GT(y, curTime);
		mPea.push_back(p);
		return ShovelStruct(PEAS, mPea.size() - 1);
	}

	ShovelStruct NWNew(const int& y, const int& curTime) {
		peashooter* p = new NW(y, curTime);
		mPea.push_back(p);
		return ShovelStruct(PEAS, mPea.size() - 1);
	}

	ShovelStruct PKNew(const int& y, const int& curTime) {
		peashooter* p = new PK(y, curTime);
		mPea.push_back(p);
		return ShovelStruct(PEAS, mPea.size() - 1);
	}

	ShovelStruct HPNew(const int& y, const int& curTime) {
		peashooter* p = new HP(y, curTime);
		mPea.push_back(p);
		return ShovelStruct(PEAS, mPea.size() - 1);
	}

	ShovelStruct doublepeaNew(const int& y, const int& curTime) {
		peashooter* p = new doublepeashooter(y, curTime);
		mPea.push_back(p);
		return ShovelStruct(PEAS, mPea.size() - 1);
	}

	ShovelStruct sunNew(const int& y, const int& curTime) {
		sunflower* p = new sunflower(y, curTime);
		mSun.push_back(p);
		return ShovelStruct(SUNF, mSun.size() - 1);
	}
};

class admin {
public:
	admin() : adminCurTime(0), curScore(0), curEnergy(USER_INIT_MONEY) {
		isCanBuy[0] = 10;
		isCanBuy[1] = 10;
		isCanBuy[2] = 20;
		isCanBuy[3] = 30;

		isCanBuy[4] = 40;
		isCanBuy[5] = 30;
		isCanBuy[6] = 30;
		isCanBuy[7] = 50;
		for (int i = 0; i < PER_MAP_ROW; ++i)
			isOver[i] = 0;
		// 初始化地图
		boundary.resize(PLINE);
		For(i, 0, LINE) {
			// boundary[i] = '‖';
			boundary[i] = ROW_MARK;
		}
		For(i, 0, PER_MAP_ROW) {
			For(k, 0, PER_SOIL_ROW) {
				for (int j = 19; j < SOIL_LINE; j += PER_SOIL_LINE) {
					fixedSoil[i].l[k][j] = LINE_MARK;
				}

				// 推车的形状.
				fixedSoil[i].l[0][0] = '>';
				fixedSoil[i].l[1][1] = '>';
				fixedSoil[i].l[2][2] = '>';
				fixedSoil[i].l[2][0] = '$';
				fixedSoil[i].l[3][0] = '$';
				fixedSoil[i].l[3][2] = '>';
				fixedSoil[i].l[4][1] = '>';
				fixedSoil[i].l[5][0] = '>';
			}
		}

		clearMap();

		vec.resize(PER_MAP_ROW);
	}

	// 生物二维string[], whi在哪行(0~4), x(传0), y位置(0~179), num个数, 
	void copyBiology(string bio[], const int& whi, const int& x, const int& y, int num = 0) {
		if (x < 0 || y < 0) {
			// cout << x << " " << y << endl;
			return;
		}
		For (i, 0, BIO_SIZE) {
			For (k, 0, BIO_SIZE) {
				if (x + i < PER_SOIL_ROW && y + k < LINE) {
					// cout << whi << " " << x + i << " " << y + k << endl;
					asoil(whi, x + i, y + k) = bio[i][k];
				}
			}
		}
		if (num != 0)
			asoil(whi, x, y) = '0' + num;
	}

	void deletePlant(const int &x, const int &y, WHO isSun) {
		if (isSun == SUNF) {
			delete vec[x].mSun[y];
			_ASSERTE(_CrtCheckMemory());
			vec[x].mSun.erase(vec[x].mSun.begin() + y);
			_ASSERTE(_CrtCheckMemory());
		}
		else {
			delete vec[x].mPea[y];
			_ASSERTE(_CrtCheckMemory());
			vec[x].mPea.erase(vec[x].mPea.begin() + y);
			_ASSERTE(_CrtCheckMemory());
		}
	}


	void killLineZombie(int l) {
		inverseSoilRow(l);
		for (int i = 0; i < vec[l].mZom.size(); ++i) {
			delete vec[l].mZom[i];
			_ASSERTE(_CrtCheckMemory());
			vec[l].mZom.erase(vec[l].mZom.begin() + i);
			_ASSERTE(_CrtCheckMemory());
		}
	}

	void bombPlant(int x, int y) {
		if (x >= 0 && x < PER_MAP_ROW && y >= 0 && y < PER_MAP_LINE) {
			inverseSoilRL(x, y);
			if (shovelArr[x][y].id != -1) {
				deletePlant(x, shovelArr[x][y].id, PEAS);
				shovelArr[x][y].id = -1;
			}
		}
	}

	
	// 生物原先在哪里的信息会被丢失. 但是vec里有实时的位置信息.
	// 通过vec更新map.
	// 向日葵里的letter好像很麻烦, 可以考虑做那种滚动播放的.
	int updateMap(bool isHaveLetter = false) {
		clearMap();

		// 整个处理的for中adminCurTime是静止的
		// zombie 覆盖 豌豆 花
		For(i, 0, PER_MAP_ROW) {
			// i 表示行纵向数有五块.

			// DONE 看看大根堆还是小根堆.

			// 当前zombie优先队列.
			int plantHurt = -1;

			priority_queue<CmpZomPos> zomPosQue;
			For(k, 0, vec[i].mZom.size()) {
				zomPosQue.push(CmpZomPos(vec[i].mZom[k]->getPos(adminCurTime, shovelArr[i], plantHurt), k));
			}

			// 向日葵.
			For(k, 0, vec[i].mSun.size()) {
				curEnergy += SUN_PER_ENERGY_PRO;
				copyBiology(vec[i].mSun[k]->getMe(adminCurTime, isHaveLetter), i, 0, vec[i].mSun[k]->getPos());
			}

			// 射手
			For(k, 0, vec[i].mPea.size()) {
				copyBiology(vec[i].mPea[k]->getMe(adminCurTime), i, 0, vec[i].mPea[k]->getPos());
				// 子弹扫一遍zombie, 并更新zombie

				// 第i行 第k个射手的第j个子弹.
				// 子弹不要飞太快. zombie 尽量id前的跑在前面.
				For(j, 0, vec[i].mPea[k]->bullVec.size()) {
					bullet& curBull = vec[i].mPea[k]->bullVec[j];

					if (!zomPosQue.empty() && curBull.getPos(adminCurTime) > zomPosQue.top().pos) {
						cout << "bullet POS: " << curBull.getPos(adminCurTime) << "  ";
						// 发现这个子弹搞到了zombie.
						int curHurtZom = zomPosQue.top().id;
						zomPosQue.pop();
						
						// TODO zombie 被打到之后会变化.
						if (vec[i].mZom[curHurtZom]->minusLive(curBull.getHurt()) == 1) {
							// zombie 被 kill
							curScore += 5;
							delete vec[i].mZom[curHurtZom];
							vec[i].mZom.erase(vec[i].mZom.begin() + curHurtZom);

							// cout << i << " " << curHurtZom << endl;
						}
						else {
							// zombie 没有被kill
							if (curBull.getWhoAmI() == 2) {
								// zombie 被冻结
								vec[i].mZom[curHurtZom]->setFixed(adminCurTime);
							}
						}

						// delete 子弹.
						vec[i].mPea[k]->bullVec.erase(vec[i].mPea[k]->bullVec.begin() + j);
					}
					else {
						if (curBull.getPos(adminCurTime) >= LINE) {
							// delete 子弹.
							vec[i].mPea[k]->bullVec.erase(vec[i].mPea[k]->bullVec.begin() + j);
						}
						else {
							// 发现这个子弹没有搞到zombie, 复制到vec.
							copyBiology(curBull.getMe(), i, 0, curBull.getPos(adminCurTime));
						}
					}
				}
			}

			// zombie
			// DONE zombie 碰到植物要停止.
			For(k, 0, vec[i].mZom.size()) {
				// k 表示 这一行所有zombie的哪一个zombie.
				plantHurt = -1;			// 初始化plantHurt.
				int zombiePos = vec[i].mZom[k]->getPos(adminCurTime, shovelArr[i], plantHurt);
				if (zombiePos < 1) {
					if (isOver[i] == 0) {
						inverseSoilRow(i);
						vide.endShow();

						killLineZombie(i);
						continue;
					}
					else {
						vide.newRecordShow();
						return -1;
					}
				}

				copyBiology(vec[i].mZom[k]->getMe(), i, 0, zombiePos);
				if (plantHurt != -1) {
					// zombie碰到植物了, 植物掉血.
					if (shovelArr[i][plantHurt].who == SUNF) {
						// 向日葵被kill
						int curId = shovelArr[i][plantHurt].id;
						if (vec[i].mSun[curId]->getHurt() == -1) {
							deletePlant(i, curId, SUNF);
							shovelArr[i][plantHurt].id = -1;			// 清空铲除列表.
							continue;
						}
					}
					else {
						int curId = shovelArr[i][plantHurt].id;
						// 火爆辣椒.
						if (vec[i].mPea[curId]->isHP == true) {
							killLineZombie(i);
							deletePlant(i, curId, PEAS);
							shovelArr[i][plantHurt].id = -1;			// 清空铲除列表.
							continue;
						}

						// 如果是普通zombie, 碰到了则植物掉血.
						if (vec[i].mZom[k]->isClo() == false) {
							if (vec[i].mPea[curId]->getHurt(PEA_BLOOD_HURT) == -1) {
								// 植物被kill
								deletePlant(i, curId, PEAS);
								shovelArr[i][plantHurt].id = -1;			// 清空铲除列表.
								continue;
							}
						}
						
						if (vec[i].mZom[k]->minusLive(vec[i].mPea[curId]->getAttack()) == 1) {
							// zombie 被 kill
							delete vec[i].mZom[k];
							vec[i].mZom.erase(vec[i].mZom.begin() + k);
							continue;
						}
						else {
							// zombie 没有被kill
							// 小丑僵尸, 四个角的被反色.
							if (vec[i].mZom[k]->isClo() == true) {
								// 2 / 3 的概率.
								if (rand() % 3 > 0) {
									bombPlant(i, plantHurt);
									bombPlant(i + 1, plantHurt - 1);
									bombPlant(i + 1, plantHurt + 1);
									bombPlant(i - 1, plantHurt - 1);
									bombPlant(i - 1, plantHurt + 1);
								}
							}
						}

					}
				}
				// cout << vec[i].mZom[k]->getPos() << endl;
			}

		}

		return 1;
	}

	void clearMap() {
		For(i, 0, PER_MAP_ROW) {
			For(k, 0, PER_SOIL_ROW) {
				rsoil(i, k) = fixedSoil[i].l[k];
			}
		}
	}

	void showAll() {
		SetConsoleCursorPosition(hOutput, coord);
		SetConsoleCursorInfo(hOutput, &CursorInfo);


		cout << boundary << endl;
		For(i, 0, PER_MAP_ROW) {
			For(k, 0, PER_SOIL_ROW) {
				cout << rsoil(i, k) << endl;
			}
			cout << boundary << endl;
		}

		vide.showScoreBoard((int)curScore, (int)curEnergy);
	}

	void showFixed() {
		SetConsoleCursorPosition(hOutput, coord);
		SetConsoleCursorInfo(hOutput, &CursorInfo);

		cout << boundary << endl;
		For(i, 0, PER_MAP_ROW) {
			For(k, 0, PER_SOIL_ROW) {
				cout << fixedSoil[i].l[k] << endl;
			}
			cout << boundary << endl;
		}

		vide.showScoreBoard((int)curScore, (int)curEnergy);
	}

	// 返回买了啥.
	// 上下键选择, 右键确定, 左键返回.
	int goShopping() {
		vide.myClear();
		vide.shopShow();
		vide.myClear();
		int curChoose = 0;
		int ch = 0;
		int befChoose = 0;
		while (true) {
			if ((befChoose == 3 && curChoose == 4) || (befChoose == 4 && curChoose == 3))
				vide.myClear();
			if (curChoose >= 0 && curChoose < 8) {
				vide.shopFrameChoose(curChoose % 4, curChoose / 4);
			}

			befChoose = curChoose;
			if (_kbhit()) {
				// 按上下键有作用, 注意需要在vs中文环境下运行, 这样的输入上下键因为是中文编码所以会有两个字符.
				ch = _getch();
				ch = _getch();
				if (ch == 72 && curChoose != 0)
					curChoose--;
				else if (ch == 80 && curChoose != 7)
					curChoose++;
				else if (ch == 77) {
					return curChoose;
				}
				else if (ch == 75) {
					return -1;
				}
			}
		}

		return -1;
	}

	// 在哪一行地块产生zombie(0~4).
	void geneZB(int whi) {
		zombie* p = new zombie(adminCurTime);
		vec[whi].mZom.push_back(p);
	}

	void geneRZB(int whi) {
		zombie* p = new RoadblockZB(adminCurTime);
		vec[whi].mZom.push_back(p);
	}

	void geneTTZB(int whi) {
		zombie* p = new BucketZB(adminCurTime);
		vec[whi].mZom.push_back(p);
	}

	void geneTMZB(int whi) {
		zombie* p = new DoorZB(adminCurTime);
		vec[whi].mZom.push_back(p);
		cout << vec[whi].mZom[vec[whi].mZom.size() - 1]->isClo() << endl;
	}

	void geneYQZB(int whi) {
		zombie* p = new FlagZB(adminCurTime);
		vec[whi].mZom.push_back(p);
	}

	void geneXCZB(int whi) {
		zombie* p = new ClownZB(adminCurTime);
		vec[whi].mZom.push_back(p);
	}

	void inverseSoilRow(int i) {
		short xb = i * 7 + 1, yb = 0;
		COORD tmpCoord = { yb, xb };
		For(i, 0, PER_SOIL_ROW) {
			tmpCoord = { yb, xb + (short)i };
			SetConsoleCursorPosition(hOutput, tmpCoord);
			SetConsoleCursorInfo(hOutput, &CursorInfo);

			For(k, 0, LINE - 1) {
				cout << '#';
			}
		}
		vide.myDelay(REFRESHRATE * 6);
		For(i, 0, PER_SOIL_ROW) {
			tmpCoord = { yb, xb + (short)i };
			SetConsoleCursorPosition(hOutput, tmpCoord);
			SetConsoleCursorInfo(hOutput, &CursorInfo);

			For(k, 0, LINE - 1) {
				cout << ' ';
			}
		}
		vide.myDelay(REFRESHRATE * 6);
	}

	// 传进来的x, y必须合法.
	void inverseSoilRL(int x, int y) {
		short xb = x * 7 + 1, yb = 20 * y;
		int loopNum = 1;
		while (loopNum--) {
			COORD tmpCoord = { yb, xb };
			For(i, 0, PER_SOIL_ROW) {
				tmpCoord = { yb, xb + (short)i };
				SetConsoleCursorPosition(hOutput, tmpCoord);
				SetConsoleCursorInfo(hOutput, &CursorInfo);

				For(k, 0, PER_SOIL_LINE - 1) {
					cout << '#';
				}
			}
			vide.myDelay(REFRESHRATE * 4);
			For(i, 0, PER_SOIL_ROW) {
				tmpCoord = { yb, xb + (short)i };
				SetConsoleCursorPosition(hOutput, tmpCoord);
				SetConsoleCursorInfo(hOutput, &CursorInfo);

				For(k, 0, PER_SOIL_LINE - 1) {
					cout << ' ';
				}
			}
			vide.myDelay(REFRESHRATE * 4);
		}
	}

	// 传进来的x, y必须合法.
	void chooseWhereToPlant(int &x, int &y, bool isC = false) {
		if (isC == false)
			vide.myClear();

		int ch = 0;

		while (true) {
			showAll();
			vide.myDelay(REFRESHRATE * 10);

			short xb = x * 7 + 1, yb = 20 * y;
			COORD tmpCoord = { yb, xb };
			For(i, 0, PER_SOIL_ROW) {
				tmpCoord = { yb, xb + (short)i };
				SetConsoleCursorPosition(hOutput, tmpCoord);
				SetConsoleCursorInfo(hOutput, &CursorInfo);

				For(k, 0, PER_SOIL_LINE - 1) {
					cout << '.';
				}
			}
			vide.myDelay(REFRESHRATE * 10);

			if (_kbhit()) {
				// 按上下键有作用, 注意需要在vs中文环境下运行, 这样的输入上下键因为是中文编码所以会有两个字符.
				ch = _getch();
				// 上 下 左 右 的顺序.
				if (ch == 119 && x != 0)
					x--;
				else if (ch == 115 && x != PER_MAP_ROW - 1)
					x++;
				else if (ch == 97 && y != 0) {
					y--;
				}
				else if (ch == 100 && y != 6) {
					y++;
				}
				else if (ch == 13) {
					return;
				}
			}
		}
	}

	void myDelay() {
		DWORD befTime = GetTickCount();
		while (GetTickCount() - REFRESHRATE < befTime)
			;
	}


	// shijian shunxu bixu cong xiao dao da
	void initTestMode() {
		qTestMode.push(TestModeStruct(50, 0, 0, 0));
		qTestMode.push(TestModeStruct(55, 0, 1, 0));
		qTestMode.push(TestModeStruct(60, 0, 2, 0));
		qTestMode.push(TestModeStruct(70, 0, 3, 0));
		qTestMode.push(TestModeStruct(80, 0, 4, 0));

		qTestMode.push(TestModeStruct(85, 1, 0, 1));
		qTestMode.push(TestModeStruct(90, 2, 1, 1));
		//qTestMode.push(TestModeStruct(95, 3, 2, 1));
		qTestMode.push(TestModeStruct(97, 3, 3, 1));
		qTestMode.push(TestModeStruct(100, 2, 4, 1));

		qTestMode.push(TestModeStruct(102, 4, 0, 5));
		qTestMode.push(TestModeStruct(105, 5, 1, 4));
		//qTestMode.push(TestModeStruct(107, 6, 2, 5));
		qTestMode.push(TestModeStruct(109, 7, 3, 3));


		qTestMode.push(TestModeStruct(112, -1, 0, -1));
		qTestMode.push(TestModeStruct(115, -2, 1, -1));
		qTestMode.push(TestModeStruct(117, -3, 2, -1));
		qTestMode.push(TestModeStruct(119, -3, 3, -1));
		qTestMode.push(TestModeStruct(120, -6, 4, -1));

		qTestMode.push(TestModeStruct(140, 4, 0, 2));
		qTestMode.push(TestModeStruct(143, 1, 1, 2));
		// qTestMode.push(TestModeStruct(147, 5, 2, 2));
		qTestMode.push(TestModeStruct(156, 0, 3, 2));
		qTestMode.push(TestModeStruct(159, 3, 4, 2));

		qTestMode.push(TestModeStruct(232, -3, 0, -1));
		qTestMode.push(TestModeStruct(235, -4, 1, -1));
		qTestMode.push(TestModeStruct(239, -6, 2, -1));
		qTestMode.push(TestModeStruct(240, -5, 3, -1));
		qTestMode.push(TestModeStruct(260, -4, 4, -1));

		// DONE zombie也做成这样队列push的测试.
	}
	
	
	void AdminMain() {
		initTestMode();

		SetConsoleCursorInfo(hOutput, &CursorInfo);

		int ch = -1;

		vide.startShow();
		
		// DONE 主循环.

		// 产生zombie.
		geneZB(1);
		geneTMZB(2);

		geneTTZB(3);
		geneRZB(4);

		int buyWhat = 0;
		int xPlant = 0, yPlant = 0;

		while (true) {
			if (_kbhit() || (!qTestMode.empty() && qTestMode.front().t == adminCurTime)) {
				if (qTestMode.empty()) {
					ch = _getch();
					// cout << "_getch(): " << ch << endl;
				}

				// 1 直接购买:
				if (ch >= 49 && ch <= 56) {
					// 选择xPlant和yPlant.
					do {
						chooseWhereToPlant(xPlant, yPlant, true);
					} while (shovelArr[xPlant][yPlant].id != -1);

					int directBuy = ch - 49;
					curEnergy -= isCanBuy[directBuy];
					switch (directBuy)
					{
					case 0:
						// sunflower.
						shovelArr[xPlant][yPlant] = vec[xPlant].sunNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
						break;
					case 1:
						shovelArr[xPlant][yPlant] = vec[xPlant].peaNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
						break;
					case 2:
						shovelArr[xPlant][yPlant] = vec[xPlant].doublepeaNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
						break;
					case 3:
						shovelArr[xPlant][yPlant] = vec[xPlant].snowpeaNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
						break;
					case 4:
						shovelArr[xPlant][yPlant] = vec[xPlant].GTNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
						break;
					case 5:
						shovelArr[xPlant][yPlant] = vec[xPlant].NWNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
						break;
					case 6:
						shovelArr[xPlant][yPlant] = vec[xPlant].PKNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
						break;
					case 7:
						shovelArr[xPlant][yPlant] = vec[xPlant].HPNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
						break;
					default:
						break;
					}
				}

				// T
				else if (ch == 116)
					vide.pauseShow();
				// B

				// 需要在测试数据导入完才能按按键.
				else if ((ch == 98) || !qTestMode.empty()) {
					buyWhat = -1;
					if (qTestMode.empty()) {
						// 测试的数据都导入完了.
						// 选择buyWhat.
						do {
							buyWhat = goShopping();
							if (buyWhat == -1)
								break;
						} while (curEnergy < isCanBuy[buyWhat]);
						// 选择xPlant和yPlant.
						if (buyWhat != -1) {
							do {
								chooseWhereToPlant(xPlant, yPlant);
							} while (shovelArr[xPlant][yPlant].id != -1);
						}
					}
					else {
						if (qTestMode.front().bWhat >= 0) {
							buyWhat = qTestMode.front().bWhat;
							xPlant = qTestMode.front().xPl;
							yPlant = qTestMode.front().yPl;
							qTestMode.pop();
						}
						else {
							int tmpWhatZB = qTestMode.front().bWhat;
							switch (tmpWhatZB)
							{
							case -1:
								geneZB(qTestMode.front().xPl);
								break;
							case -2:
								geneRZB(qTestMode.front().xPl);
								break;
							case -3:
								geneTTZB(qTestMode.front().xPl);
								break;
							case -4:
								geneTMZB(qTestMode.front().xPl);
								break;
							case -5:
								geneYQZB(qTestMode.front().xPl);
								break;
							case -6:
								geneXCZB(qTestMode.front().xPl);
								break;
							default:
								break;
							}
							qTestMode.pop();
						}
					}

					if (buyWhat != -1) {
						// 判断买了啥并种植.
						curEnergy -= isCanBuy[buyWhat];
						switch (buyWhat)
						{
						case 0:
							// sunflower.
							shovelArr[xPlant][yPlant] = vec[xPlant].sunNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
							break;
						case 1:
							shovelArr[xPlant][yPlant] = vec[xPlant].peaNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
							break;
						case 2:
							shovelArr[xPlant][yPlant] = vec[xPlant].doublepeaNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
							break;
						case 3:
							shovelArr[xPlant][yPlant] = vec[xPlant].snowpeaNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
							break;
						case 4:
							shovelArr[xPlant][yPlant] = vec[xPlant].GTNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
							break;
						case 5:
							shovelArr[xPlant][yPlant] = vec[xPlant].NWNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
							break;
						case 6:
							shovelArr[xPlant][yPlant] = vec[xPlant].PKNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
							break;
						case 7:
							shovelArr[xPlant][yPlant] = vec[xPlant].HPNew(yPlant * PER_SOIL_LINE + 7, adminCurTime);
							break;
						default:
							break;
						}
					}
				}

				// C 铲子铲掉东西 DONE 建立位置和vec里面生物的联系 再开一个数据结构 实时更新.
				else if (ch == 99) {
					// 可以用chooseWhereToPlant去选择.
					int xShovel = 0, yShovel = 0;
					do {
						chooseWhereToPlant(xShovel, yShovel, true);
					} while (shovelArr[xShovel][yShovel].id == -1);

					deletePlant(xShovel, shovelArr[xShovel][yShovel].id, shovelArr[xShovel][yShovel].who);
					shovelArr[xShovel][yShovel].id = -1;
				}
			}

			// TODO 下面还要产生zombie.

			if (updateMap() == -1)
				return;
			showAll();
			cout << "time: " << adminCurTime << endl << shovelArr[4][1].id << endl;
			++adminCurTime;
		}
	}


private:
	string boundary;
	linemap soil[PER_MAP_ROW], fixedSoil[PER_MAP_ROW];	// 每个元素代表一个行的地块, 有5个, 5个行地块. 注意这里没有边界, 这里只有实打实的土地部分.
	Video vide;

	// 需要维护的就是vec里面的变化. 每次将vec不断刷新到地图上就可以了.
	// 买了一个东西被种好之后就是更新vec, 然后刷新.
	vector<obj> vec;
	vector<int> zomMap[PER_MAP_ROW];	// 每个元素有180个, 代表180格的位置上每个位置有几只僵尸.
	int fixedBio[PER_MAP_ROW][PER_MAP_LINE];
	double curEnergy, curScore;
	int maxScore;
	ShovelStruct shovelArr[PER_MAP_ROW][PER_MAP_LINE];

	int adminCurTime;

	int isOver[PER_MAP_ROW];

	int isCanBuy[10];

	queue<TestModeStruct> qTestMode;
};