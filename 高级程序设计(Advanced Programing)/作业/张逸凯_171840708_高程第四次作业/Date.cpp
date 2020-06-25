#include "Date.h"

void Date::display()
{
	cout << year << "-" << month << "-" << day << endl;
}

Date &operator ++(Date& self) {
	int monEnd = self.month % 2 == 0 ? 30 : 31;
	if (self.month == 2) {
		if ((self.year % 100 != 0 && self.year % 4 == 0) || (self.year % 400 == 0)) {
			monEnd = 28;
		}
		else
			monEnd = 29;
	}
	++self.day;
	if (self.day > monEnd && self.month < 12) {
		++self.month;
		self.day = 1;
	}
	else if (self.day > monEnd && self.month == 12) {
		++self.year;
		self.day = 1;
		self.month = 1;
	}

	return self;
}


const Date operator ++(Date& self, int) {
	Date ret = self;
	int monEnd = self.month % 2 == 0 ? 30 : 31;
	if (self.month == 2) {
		if ((self.year % 100 != 0 && self.year % 4 == 0) || (self.year % 400 == 0)) {
			monEnd = 28;
		}
		else
			monEnd = 29;
	}
	++self.day;
	if (self.day > monEnd && self.month < 12) {
		++self.month;
		self.day = 1;
	}
	else if (self.day > monEnd && self.month == 12) {
		++self.year;
		self.day = 1;
		self.month = 1;
	}

	return ret;
}

int main()
{
	Date d1;
	cout << "今天是：";
	d1.display();
	d1++;
	cout << "明天是：";
	d1.display();
	return 0;
}