#pragma once
#include "Wlist.h"
class Admin {
public:
	Admin() { }
	Admin(string wordListInit, string wordDisp, string startDisp) : wordListInit(wordListInit), wordDisp(wordDisp), startDisp(startDisp) { }

	// 展示相关内容(学习单词界面)
	void display(UI_TYPE uiType, Word word = Word(), int dispTime = 0, bool doNotCh = false) {
		SetConsoleCursorPosition(hOutput, coord);
		For(i, 0, MAX_DISP_ROW) {
			// 前面应该用数组的, 但是问题不大.
			if (uiType == START) {
				cout << dispArr[LEARNING][i] << endl;
			}
			else if (uiType == LEARNING) {
				if (i == LEARNING_WORD_POS && word.get_id() > 0)
					cout << "   { " << word.get_id() << " }" << endl;
				else if (i == LEARNING_WORD_POS + 1)
					cout << "   " << word.get_eng().substr(0, MAX_DISP_LINE - 3) << endl;
				else if (i == LEARNING_WORD_POS + 2)
					cout << "   " << word.get_snd().substr(0, MAX_DISP_LINE - 3) << endl;
				else if (doNotCh == false && i == LEARNING_WORD_POS + 3)
					cout << "   " << word.get_ch().substr(0, MAX_DISP_LINE) << endl;
				else
					cout << dispArr[LEARNING][i] << endl;
			}
		}
		if (doNotCh == true) {
			Sleep(3000);
			display(uiType, word, dispTime, false);
		}
		if (dispTime != 0)
			Sleep(dispTime * 1000);
	}

	void study(bool doNotCh = false) {
		char ch;
		bool isOk = false;
		while (true) {
			display(START);
			display(LEARNING, newWlist.get_learning_word(), 0, doNotCh);
			while (true) {
				int forgotRnk = 5;
				if (_kbhit()) {
					ch = _getch();
					ch = _getch();
					// cout << "DEBUG: ch: " << int(ch) << endl;

					// 右键: 认识单词.
					if (ch == 77) {
						forgotRnk = KNOW;
					}
					//// 左键: 上一个单词.
					//else if (ch == 75) {
					//	newWlist.prev_word();
					//}
					// 下键: 不认识
					else if (ch == 80) {
						forgotRnk = KNOW;

					}
					// 上键: 忘记
					else if (ch == 72) {
						forgotRnk = FORGOT;
					}
					// 左键: 模糊
					else if (ch == 75) {
						forgotRnk = VAGUE;
					}
					else if (ch == 27) {
						return;
					}

					// 加入复习列表:
					learnedWlist.push(newWlist.get_learning_word());
					isOk = newWlist.next_word();
					if (isOk == true) {
						// 完成今天的学习.
						++newWlist.get_today();
						// cout << newWlist.get_today() << endl;
						newWlist.update_totalDays();
						return;
					}
					break;
				}
			}
		}
	}

	void review(bool doNotCh = false) {
		char ch;
		while (true) {
			display(START);
			int curReviewWord = learnedWlist.get_review_word();
			if (curReviewWord == -1) {
				// 复习完成:
				// TODO: UI 展示复习完成.
				return;
			}
			display(LEARNING, learnedWlist.lVec[curReviewWord], 0, doNotCh);
			while (true) {
				if (_kbhit()) {
					ch = _getch();
					ch = _getch();
					// cout << "DEBUG: ch: " << int(ch) << endl;

					// 右键: 认识单词.
					if (ch == 77) {
						learnedWlist.lVec[curReviewWord].reduce_rnk(1);
						// cout << learnedWlist.lVec[curReviewWord].get_id() << "  " << learnedWlist.lVec[curReviewWord].get_forgotRnk() << endl;
					}
					//// 左键: 上一个单词.
					//else if (ch == 75) {
					//	newWlist.prev_word();
					//}
					// 下键: 不认识
					else if (ch == 80) {
						// pass
					}
					curReviewWord = learnedWlist.get_review_word();
					break;
				}
			}
		}
	}

	void modify_plan() {
		char ch;

		while (true) {
			display(START);
			display(LEARNING, Word(0, "= PLEASE INPUT: " + to_string(newWlist.get_everyDayLearn()) + " Words/Day =", "Day " + to_string(newWlist.get_today()) + ", Total " + to_string(newWlist.get_totalDays()) + " days.", "# SELECTED! MODIFY Learned Per Day..."));
			while (true) {
				if (_kbhit()) {
					ch = _getch();
					ch = _getch();
					// cout << "DEBUG: ch: " << int(ch) << endl;

					// 右键: 增加.
					if (ch == 77) {
						++newWlist.get_everyDayLearn();
						newWlist.update_totalDays();
						newWlist.update_begendDays();
					}
					// 左键: 减少
					else if (ch == 75) {
						if (newWlist.get_everyDayLearn() != 1) {
							--newWlist.get_everyDayLearn();
							newWlist.update_totalDays();
							newWlist.update_begendDays();
						}
					}
					// 回车: 选择了:
					else if (ch == 13) {
						return;
					}
					break;
				}
			}
		}
	}

	// 将disp文件内容读入缓存, 后面display的时候直接输出缓存即可.
	void read_disp(string fileName, int dispIdx) {
		FILE* fp;
		fp = fopen(fileName.c_str(), "r");
		char buf[100010] = "";
		int cnt = 0;
		while (!feof(fp)) {
			fgets(buf, 100000, fp);
			string s(buf);
			dispArr[dispIdx][cnt++] = s.substr(0, s.size() - 1);
		}
	}

	void main() {
		// 读入"新学习单词"的UI界面.
		read_disp(wordDisp, LEARNING);
		// 读入"欢迎界面"
		read_disp(startDisp, START);

		char ch;
		string startTips[START_TIPS_NUM] = {
			">> NEW STUDY",
			">> REVIEW   ",
			">> SET PLAN "
		};

		// 所有单词表:
		newWlist = NewWlist(wordListInit);

		bool isFirst = true;
		while (true) {
			// 展示欢迎界面.
			display(START);

			int curChoose = 0;
			while (true) {
				if (isFirst == false)
					display(LEARNING, Word(0, "== Please use the up and down key. ==", startTips[curChoose % START_TIPS_NUM], "# SELECT MODE #"));
				if (_kbhit()) {
					// 按上下键有作用, 注意需要在vs中文环境下运行, 这样的输入上下键因为是中文编码所以会有两个字符.
					ch = _getch();
					// cout << int(ch) << "  " << curChoose << endl;
					// 上下键选择模式.
					if (ch == 72)
						curChoose--;
					else if (ch == 80)
						curChoose++;

					// 回车选择:
					else if (ch == 13) {
						curChoose %= START_TIPS_NUM;
						break;
					}
					while (curChoose < 0)
						curChoose += START_TIPS_NUM;
					display(LEARNING, Word(0, "== Please use the up and down key. ==", startTips[curChoose % START_TIPS_NUM], "# SELECT MODE #"));
				}
			}
			isFirst = false;

			display(START);

			time_t startTime = time(NULL);
			bool doNotCh = false;
			// 此时选择了相应的模式, 跳转进入相应的界面. 根据curChoose选择.
			switch (curChoose) {
			case 0:
				// 开始新的学习.
				display(START);
				display(LEARNING, Word(0, "== TODAY's Goal: " + to_string(newWlist.get_endToday() - newWlist.get_begToday()) + " Words ==", "Day " + to_string(newWlist.get_today()), "# SELECTED! Hide Chinese, press [H] #"));
				startTime = time(NULL);
				while (time(NULL) - startTime < 9) {
					display(LEARNING, Word(0, "== TODAY's Goal: " + to_string(newWlist.get_endToday() - newWlist.get_begToday()) + " Words ==", "Day " + to_string(newWlist.get_today()) + ", Total " + to_string(newWlist.get_totalDays()) + " days. (" + to_string(9 - (time(NULL) - startTime)) + "s LEFT)", "# SELECTED! Hide Chinese, press [H] #"));
					// cout << int(ch) << "  " << curChoose << endl;
					if (_kbhit()) {
						ch = _getch();
						if (ch == 104) {
							doNotCh = true;
						}
						else if (ch == 13)
							break;
					}
				}
				study(doNotCh);
				break;
			case 1:
				// 开始复习.
				review(doNotCh);
				break;
			case 2:
				// 查看/修改学习计划.
				modify_plan();
				break;
			}
		}
	}

private:
	string wordListInit, wordDisp, startDisp; // 文件名.
	NewWlist newWlist;
	LearnedWlist learnedWlist;
	string dispArr[MAX_DISP_NUM][MAX_DISP_ROW + 10];
};

