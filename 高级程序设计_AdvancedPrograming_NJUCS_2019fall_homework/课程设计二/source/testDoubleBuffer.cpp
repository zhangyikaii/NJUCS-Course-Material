#include<iostream>
#include<Windows.h>
using namespace std;
#define MAP_HEGHT 20
#define MAP_WIGHT 30
void map(int CountX, int CountY);

int main()
{
	HANDLE hOutput;
	COORD coord = { 0, 0 };
	hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
	int BeginTime = GetTickCount();
	while (true)
	{
		if (GetTickCount() - 1000 / 6 >= BeginTime)
		{
			SetConsoleCursorPosition(hOutput, coord);
			map(MAP_HEGHT, MAP_WIGHT);
			BeginTime = GetTickCount();
		}
	}
	cin.get();
}

void map(int CountX, int CountY)
{
	for (int x = 0; x < CountX; x++)
	{
		for (int y = 0; y < CountY; y++)
		{
			cout << "□";
		}
		cout << endl;
	}
}