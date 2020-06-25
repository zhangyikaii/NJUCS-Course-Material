#include <iostream>
using namespace std;

class Shooting
{
	float FTPercentage; // 罚球命中率
	float FGPercentage; // 投篮命中率
	float TPPercentage; // 三分命中率
public:
	Shooting()
	{
		FTPercentage = 0.2;
		FGPercentage = 0.2;
		TPPercentage = 0.2;
	}
	Shooting(float ftp, float fgp, float tpp)
	{
		FTPercentage = ftp;
		FGPercentage = fgp;
		TPPercentage = tpp;
	}
};

class NBAPlayer
{
	Shooting shoot; // 实例化 Shooting 对象 shoot
	string name;
public:
	//补全1. 调用 Shooting 的默认构造函数对 shoot 初始化;
	NBAPlayer(string n) : name(n) { };
	//补全2. 调用 Shooting(float ftp, float fgp, float tpp) 构造函数对 shoot 初始化;
	NBAPlayer(string n, float ftpp, float fgpp, float tppp) : name(n), shoot(ftpp, fgpp, tppp) { }
};

int main()
{
	//补全3. p1.name 初始化为 Curry，p1.shoot的各项命中率采用默认初始化；
	NBAPlayer p1("Curry");
	//补全4. p2.name 初始化为 Curry，p2.shoot的 FTPercentage初始化为 0.9, FGPercentage 初始化为 0.71，TPPercentage 初始化为0.44
	NBAPlayer p2("", 0.9, 0.71, 0.44);

	return 0;
}