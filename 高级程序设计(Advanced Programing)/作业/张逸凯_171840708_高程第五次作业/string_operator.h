#pragma once
#include <iostream>
#include <string.h>

using namespace std;

class CustomString
{
public:
	//构造函数
	CustomString();
	CustomString(const char* str);
	CustomString(const CustomString& a);		// 不要忘了拷贝构造函数.
	CustomString operator +(const CustomString& a);
	CustomString operator +=(const CustomString& a);
	bool operator ==(const CustomString& a);
	bool operator !=(const CustomString& a);
	friend ostream& operator <<(ostream& os, const CustomString& a);
	friend istream& operator >>(istream& in, CustomString& a);

	CustomString& operator=(const CustomString& a) {
		delete[]this->p;

		p = new char[a.len];
		strcpy(p, a.p);
		len = a.len;

		return *this;
	}


	//析构函数
	~CustomString();


	// 自己写的部分:
	char& operator [](int idx);
private:
	char* p; // 字符串的起始地址
	int len; // 字符串的长度
};
