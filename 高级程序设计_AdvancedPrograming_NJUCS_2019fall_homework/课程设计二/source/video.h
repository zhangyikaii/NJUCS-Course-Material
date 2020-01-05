#pragma once

#include "common.h"

class Video {
public:
	Video() : whatIntmpVideo(0) {
		loadData("newRecord.txt", newRecordVideo);
		loadData("pause.txt", pauseVideo);
		loadData("shop.txt", shopVideo);

		loadOneDimenData("shopMain1.txt", mainShop1);
		loadOneDimenData("shopMain2.txt", mainShop2);
		
		for (int i = 0; i < SCORE_BOARD_ROW; ++i) {
			scoreBoard[i].resize(LINE);
		}
		loadOneDimenData("your.txt", scoreBoard);
		
	}

	void loadData(string fileName, string vedi[][ROW]) {
		FILE* fp;
		int cnt = 0;
		fileName = "./VideoData/" + fileName;
		// cout << "fileName: " << fileName << endl;
		fp = fopen(fileName.c_str(), "r");
		char buf[100010] = "";
		while (!feof(fp)) {
			fgets(buf, 100000, fp);
			string s(buf);
			for (int i = 0, curBef = 0; i < ROW; ++i, curBef += LINE) {
				vedi[cnt][i].clear();
				vedi[cnt][i] = s.substr(curBef, LINE);
			}
			cnt++;
		}

		// cout << cnt << endl;
	}
	void loadOneDimenData(string fileName, string vedi[]) {
		FILE* fp;
		int cnt = 0;
		fileName = "./VideoData/" + fileName;
		// cout << "fileName: " << fileName << endl;
		fp = fopen(fileName.c_str(), "r");
		char buf[100010] = "";
		while (!feof(fp)) {
			fgets(buf, 100000, fp);
			string s(buf);

			// 去掉回车.
			s = s.substr(0, s.size() - 1);
			vedi[cnt] = s;

			cnt++;
		}
		// cout << cnt << endl;
	}

	void startShow() {
		myClear();

		if (whatIntmpVideo != 1) {
			whatIntmpVideo = 1;
			loadData("start.txt", tmpVideo);
		}
		
		int ch = 0;

		int befTime = GetTickCount();
		while (true) {
			for (int whichFrame = 0; whichFrame < VSTART_FRAME; ++whichFrame) {
				while (GetTickCount() - REFRESHRATE < befTime)
					;
				SetConsoleCursorPosition(hOutput, coord);
				SetConsoleCursorInfo(hOutput, &CursorInfo);

				For(i, 0, ROW) {
					cout << tmpVideo[whichFrame][i] << endl;
				}
				befTime = GetTickCount();

				if (_kbhit()) {
					// 按下任意键继续.
					ch = _getch();
					myClear();
					return;
				}
			}
		}

	}
	
	void endShow() {
		if (whatIntmpVideo != 2) {
			whatIntmpVideo = 2;
			loadData("end.txt", tmpVideo);
		}

		int ch = 0;

		int befTime = GetTickCount();
		while (true) {
			for (int whichFrame = 0; whichFrame < VEND_FRAME; ++whichFrame) {
				while (GetTickCount() - REFRESHRATE < befTime)
					;
				SetConsoleCursorPosition(hOutput, coord);
				SetConsoleCursorInfo(hOutput, &CursorInfo);

				For(i, 0, ROW) {
					cout << tmpVideo[whichFrame][i] << endl;
				}
				for (int i = 0; i < 10; ++i) {
					for (int k = 0; k < LINE; ++k) {
						cout << ' ';
					}
				}
				befTime = GetTickCount();

				if (_kbhit()) {
					// 按下任意键继续.
					ch = _getch();
					return;
				}
			}
		}
	}

	void newRecordShow() {
		int ch = 0;

		int befTime = GetTickCount();

		for (int whichFrame = 0; whichFrame < VNEWRECORD_FRAME; ++whichFrame) {
			while (GetTickCount() - REFRESHRATE < befTime)
				;
			SetConsoleCursorPosition(hOutput, coord);
			SetConsoleCursorInfo(hOutput, &CursorInfo);

			For(i, 0, ROW) {
				cout << newRecordVideo[whichFrame][i] << endl;
			}
			befTime = GetTickCount();

			if (_kbhit()) {
				// 按下任意键继续.
				ch = _getch();
				return;
			}
		}
	}

	void pauseShow() {
		myClear();
		int ch = 0;

		int befTime = GetTickCount();
		while (true) {
			for (int whichFrame = 0; whichFrame < VPAUSE_FRAME; ++whichFrame) {
				while (GetTickCount() - REFRESHRATE < befTime)
					;
				SetConsoleCursorPosition(hOutput, coord);
				SetConsoleCursorInfo(hOutput, &CursorInfo);

				For(i, 0, ROW) {
					cout << pauseVideo[whichFrame][i] << endl;
				}
				befTime = GetTickCount();

				if (_kbhit()) {
					// 按下任意键继续.
					ch = _getch();
					return;
				}
			}
		}
	}

	void shopShow() {
		myClear();
		int ch = 0;

		int befTime = GetTickCount();
		for (int whichFrame = 0; whichFrame < VSHOP_FRAME; ++whichFrame) {
			while (GetTickCount() - REFRESHRATE < befTime)
				;
			SetConsoleCursorPosition(hOutput, coord);
			SetConsoleCursorInfo(hOutput, &CursorInfo);

			For(i, 0, ROW) {
				cout << shopVideo[whichFrame][i] << endl;
			}
			befTime = GetTickCount();

			if (_kbhit()) {
				// 按下任意键继续.
				ch = _getch();
				return;
			}
		}
	}


	void myDelay(int delayRate) {
		DWORD befTime = GetTickCount();
		while (GetTickCount() - delayRate < befTime)
			;
	}

	void shopFrameChoose(int whi, int fraWhi) {
		string* fraWhiArr = NULL;
		if (fraWhi == 0) {
			fraWhiArr = mainShop1;
		}
		else
			fraWhiArr = mainShop2;
		int beg = whi * 10, aft = (whi + 1) * 10;
		SetConsoleCursorPosition(hOutput, coord);
		SetConsoleCursorInfo(hOutput, &CursorInfo);

		For(i, 0, ROW) {
			For(k, 0, fraWhiArr[i].size()) {
				if (i >= beg && i < aft) {
					if (fraWhiArr[i][k] == ' ')
						cout << '.';
					else
						cout << fraWhiArr[i][k];
				}
				else
					cout << fraWhiArr[i][k];
			}
			cout << endl;
		}

		
		myDelay(REFRESHRATE * 10);

		SetConsoleCursorPosition(hOutput, coord);
		SetConsoleCursorInfo(hOutput, &CursorInfo);

		For(i, 0, ROW) {
			cout << fraWhiArr[i] << endl;
		}

		myDelay(REFRESHRATE * 10);
	}

	void shopFrame1Show() {
		myClear();
		SetConsoleCursorPosition(hOutput, coord);
		SetConsoleCursorInfo(hOutput, &CursorInfo);

		For(i, 0, ROW) {
			cout << mainShop1[i] << endl;
		}
	}

	void shopFrame2Show() {
		SetConsoleCursorPosition(hOutput, coord);
		SetConsoleCursorInfo(hOutput, &CursorInfo);

		For(i, 0, LINE) {
			cout << mainShop2[i] << endl;
		}
	}

	void myClear() {
		SetConsoleCursorPosition(hOutput, coord);
		SetConsoleCursorInfo(hOutput, &CursorInfo);

		For(i, 0, ROW + 5) {
			For(k, 0, LINE)
				cout << " ";
			cout << endl;
		}
	}

	void showScoreBoard(const int& scor, const int& ener) {
		For(i, 0, LINE)
			cout << ' ';
		cout << endl;
		string sc = to_string(scor), ene = to_string(ener);
		For(i, 0, 4) {
			scoreBoard[1][110 + i] = ' ';
			scoreBoard[7][115 + i] = ' ';
		}
		For(i, 0, sc.size()) {
			scoreBoard[1][110 + i] = sc[i];
		}
		For(i, 0, ene.size()) {
			scoreBoard[7][115 + i] = ene[i];
		}
		For(i, 0, SCORE_BOARD_ROW) {
			cout << scoreBoard[i] << endl;
		}
	}



private:
	// video数组的第一个分量表示帧数, 设定好的对特定video起作用的, 不要随意更改.
	string newRecordVideo[VNEWRECORD_FRAME][ROW], pauseVideo[VPAUSE_FRAME][ROW];
	string shopVideo[VSHOP_FRAME][ROW];
	// 其他视频要用的时候在导入.
	string tmpVideo[VMAX_FRAME][ROW];
	int whatIntmpVideo;

	string mainShop1[ROW], mainShop2[ROW];
	string scoreBoard[SCORE_BOARD_ROW];
};


/*

*/
