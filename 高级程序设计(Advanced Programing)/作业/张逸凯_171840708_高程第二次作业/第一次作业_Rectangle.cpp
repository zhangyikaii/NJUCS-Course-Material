#include "Rectangle.h"

// 设置长方形宽和高的 setWH() 方法
void Rectangle::setWH(int w, int h) {
	width = w;
	height = h;
}

// 计算长方形周长的 CRectangle() 方法
int Rectangle::CRectangle() {
	return width * 2 + height * 2;
}

int main() {
	Rectangle rectangle(3, 4); // 实例化 rectangle 对象
	cout << "The perimeter of the rectangle is: " << rectangle.CRectangle() << endl;
	rectangle.setWH(5, 6); // 修改宽和高的值
	cout << "The perimeter of the rectangle is: " << rectangle.CRectangle() << endl;


	return 0;
}


