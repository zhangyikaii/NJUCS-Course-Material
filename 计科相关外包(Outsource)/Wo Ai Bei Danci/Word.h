#pragma once
#include "common.h"

class Word {
public:
	Word(): id(-1), forgotRnk(-1) { }
	Word(int id, string ch, string snd, string eng) : id(id), ch(ch), snd(snd), eng(eng) { }
	Word(string text, int id) {
		this->id = -1;
		size_t fir = text.find("/");
		if (fir == string::npos)
			return;
		size_t sec = text.find("/", fir + 1);
		if (sec == string::npos)
			return;

		// 截取原始文本文件中的中英文和音标.
		string engTmp = text.substr(0, fir), sndTmp = text.substr(fir, sec + 1 - fir), chTmp = text.substr(sec + 1, text.size() - sec - 2);
		trim(engTmp), trim(sndTmp), trim(chTmp);

		this->id = id;
		this->ch = chTmp;
		this->snd = sndTmp;
		this->eng = engTmp;
		this->forgotRnk = 5;
	}
	void trim(string& s) {
		if (s.empty())
			return;
		if (s[s.size() - 1] == '\n')
			s = s.substr(0, s.size() - 1);
		s.erase(0, s.find_first_not_of(" "));
		s.erase(s.find_last_not_of(" ") + 1, s.size());
	}
	void remove_space(string &str) {
		string::iterator end_pos = std::remove(str.begin(), str.end(), ' ');
		str.erase(end_pos, str.end());
	}
	bool operator<(const Word& other) const {
		return this->forgotRnk < other.forgotRnk;
	}

	string &get_eng() {
		return eng;
	}
	string& get_ch() {
		return ch;
	}
	string& get_snd() {
		return snd;
	}
	int& get_id() {
		return id;
	}
	int& get_forgotRnk() {
		return forgotRnk;
	}
	void reduce_rnk(int r) {
		forgotRnk -= r;
		if (forgotRnk < 0)
			forgotRnk = 0;
	}
private:
	string eng, snd, ch;
	int id, forgotRnk;
};