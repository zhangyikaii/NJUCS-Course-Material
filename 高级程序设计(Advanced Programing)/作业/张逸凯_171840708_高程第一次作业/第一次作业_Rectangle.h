#ifndef  __RECTANGLE_H__

#define   __RECTANGLE_H__

#include <iostream>

using namespace std;

class Rectangle
{
public:
	Rectangle() : width(0), height(0) { }
	Rectangle(int w, int h) : width(w), height(h) { }
	void setWH(int w, int h);
	int CRectangle();
private:
	int width, height;
};

#endif