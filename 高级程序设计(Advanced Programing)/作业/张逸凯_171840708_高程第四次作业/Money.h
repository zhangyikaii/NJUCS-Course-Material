#pragma once
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

class Money
{
public:
	Money() {
		cout << "请输入元、角 分：" << endl;
		cin >> yuan >> jiao >> fen;
	}
	Money(int y, int j, int f) : yuan(y), jiao(j), fen(f) { }

	// 前置
	friend const Money operator +(const Money& a, const Money& b);
	friend const Money operator -(const Money& a, const Money& b);

	void display() {
		if (yuan < 0) {
			cout << "-";
			cout << -yuan << "元" << -jiao << "角" << -fen << "分" << endl;
		}
		else {
			cout << yuan << "元" << jiao << "角" << fen << "分" << endl;
		}
	}
private:
	int yuan, jiao, fen;
};