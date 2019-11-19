#include <iostream>
using namespace std;

class Test
{
private:
	//1. const 成员声明
	const int a;
public:
	//2. 构造函数初始化
	Test() : a(10) { }
	Test(int tmpa) : a(tmpa) { }

	int getConst()
	{
		//3. 返回 const 成员
		return a;
	}
};


int main()
{
	// 4. 实例化 Test对象
	Test t;
	Test tmp(10);
	// 5. 输出 const 成员
	cout << t.getConst() << endl;
	cout << tmp.getConst() << endl;
	return 0;
}