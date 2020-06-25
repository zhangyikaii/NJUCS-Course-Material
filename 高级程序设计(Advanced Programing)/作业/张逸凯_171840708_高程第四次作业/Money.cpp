#include "Money.h"

const Money operator +(const Money& a, const Money& b) {
	Money tmp(0, 0, 0);
	int goNum = (a.fen + b.fen) / 10, cur = 0;
	tmp.fen = (a.fen + b.fen) % 10;

	cur = a.jiao + b.jiao + goNum;
	tmp.jiao = cur % 10;
	goNum = cur / 10;

	tmp.yuan = a.yuan + b.yuan + goNum;

	return tmp;
}


const Money operator -(const Money& a, const Money& b) {
	Money tmp(0, 0, 0);
	int flag = 1;
	ll res = a.yuan * 100 + a.jiao * 10 + a.fen - b.yuan * 100 - b.jiao * 10 - b.fen;
	if (res < 0) {
		res = -res;
		flag = -1;
	}

	tmp.fen = flag * (res % 10);
	tmp.jiao = flag * (res / 10 % 10);
	tmp.yuan = flag * (res / 100);

	return tmp;
}

int main()
{
	Money m1, m2;
	Money sum = m1 + m2, sub = m1 - m2;
	cout << "ºÍ: ";
	sum.display();

	cout << "²î: ";
	sub.display();

	return 0;
}