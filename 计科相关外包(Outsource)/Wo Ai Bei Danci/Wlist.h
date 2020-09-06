#pragma once
#include "Word.h"

struct LearnedWlistDS {
	int idx, forgotRnk;
	LearnedWlistDS() { }
	LearnedWlistDS(int idx, int forgotRnk) : idx(idx), forgotRnk(forgotRnk) { }
};

class Wlist {
public:
	Wlist() { }
	// 最开始初始化时从文件导入
	Wlist (string fileName) {
		FILE* fp;
		fp = fopen(fileName.c_str(), "r");
		char buf[100010] = "";
		int wordId = 1;
		while (!feof(fp)) {
			fgets(buf, 100000, fp);
			string s(buf);
			Word wordTmp = Word(s, wordId);
			if (wordTmp.get_id() != -1) {
				wVec.push_back(wordTmp);
				++wordId;
			}
		}
	}

	vector<Word> wVec;
};

// 生词表: 从来没学习过的单词.
class NewWlist : public Wlist {
public:
	NewWlist() { }
	NewWlist(string curFileName, int everyDayLearn = EVERYDAY_LEARN_INIT) : everyDayLearn(everyDayLearn), Wlist(curFileName), today(1), begToday(0), endToday(begToday + everyDayLearn) {
		totalDays = wVec.size() / everyDayLearn + 1;
	}

	Word& get_learning_word() {
		return wVec[begToday];
	}

	bool next_word() {
		if (begToday != wVec.size())
			++begToday;
		if (begToday >= endToday) {
			endToday += everyDayLearn;
			return true;
		}
		return false;
	}
	void prev_word() {
		if (begToday != 0)
			--begToday;
	}

	int& get_begToday() {
		return begToday;
	}
	int& get_endToday() {
		return endToday;
	}
	int& get_today() {
		return today;
	}
	int& get_totalDays() {
		return totalDays;
	}
	int& get_everyDayLearn() {
		return everyDayLearn;
	}
	void update_totalDays() {
		totalDays = wVec.size() / everyDayLearn + 2 - today;
	}
	void update_begendDays() {
		endToday = begToday + everyDayLearn;
	}

private:
	int begToday, endToday, today, totalDays, everyDayLearn;
};

// 已经学习过(可选项: 可能需要重复出现并复习的单词).
class LearnedWlist : public Wlist {
public:
	LearnedWlist() { }
	void push(Word &w) {
		lVec.push_back(w);
	}

	int get_review_word() {
		// static int DEBUG_get_review_word = 0;
		// cout << "\n\nget_review_word begin: " << DEBUG_get_review_word << " " << lVec.size() << endl;
		if (lVec.size() == 0)
			return -1;
		int r = rand() % lVec.size();
		while (lVec.size() != 0 && lVec[r].get_forgotRnk() == 0) {
			lVec.erase(lVec.begin() + r);
			if (lVec.size() == 0)
				return -1;
			r = rand() % lVec.size();
		}
		// cout << "get_review_word end: " << DEBUG_get_review_word << " " << lVec.size() << endl;
		// ++DEBUG_get_review_word;
		if (lVec.size() == 0)
			return -1;
		return r;
	}

	vector<Word> lVec;
};

