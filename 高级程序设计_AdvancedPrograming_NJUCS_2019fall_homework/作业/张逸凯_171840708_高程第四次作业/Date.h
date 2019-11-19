#pragma once
#include <bits/stdc++.h>
using namespace std;

class Date
{
public:
	Date() { 
		cout << "请输入年、月、日：" << endl;
		cin >> year >> month >> day;
	}
	Date(int y, int m, int d) : year(y), month(m), day(d) { }
	void display();

	// 前置
	friend Date& operator++(Date& self);
	friend const Date operator++(Date& self, int);
	
private:
	int year, month, day;
};