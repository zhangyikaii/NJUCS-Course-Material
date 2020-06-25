#pragma once
#include "MdFile.h"

enum {
	TITLE = 1,
	TEXT,
	URL,
	ITALIC,
	STRONG,
	LIST,
	CODE,
	LINE,
	CODEBLOCK,
	QUOTEBLOCK
};

#define Fora for (; ii < vec.size(); ++ii)
#define Forb for (; kk < vec[ii].size(); ++kk)
#define Cur (vec[ii][kk])
#define CurBef (vec[ii][bef])
#define LineSize (vec[ii].size())
#define StrCh (MyCharToString(ch))

#define CSS_PATH "./night.css"

struct MyPair {
	int fir, sec;
	MyPair() : fir(0), sec(0) { }
	MyPair(int f, int s) : fir(f), sec(s) { }
	bool operator<(const MyPair pa) const {
		return pa.fir < this->fir;
	}
};

class HtmlFile
{
public:
	HtmlFile() : ii(0), 
		kk(0), 
		fp(NULL), 
		head("<!doctype html>\n<html>\n<head>\n<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>\n<title>"), 
		subHead("</title></head>\n<body>"), 
		styHead1("<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=yes\">\n\n"), 
		styHead2("<title>"), 
		styHead3("</title>\n</head>\n\n<body>\n") { }
	
	void CreateHtmlFile(MdFile mdfOut, int isSty);
	int Url(int bef, int aft);
	int DoOneLine(int bef, int aft, bool used[], int befListLevel = 0);
	void AddHead();
	void AddStyle();

	string MyCharToString(char a) {
		string s;
		s.push_back(a);
		return s;
	}

private:
	FILE* fp;
	string fileName;
	vector<string> vec;
	int ii, kk;
	const string head, subHead;
	const string styHead1;
	const string styHead2;
	const string styHead3;
};
