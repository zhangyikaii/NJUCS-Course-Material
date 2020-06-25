#include "admin.h"
#include <windows.h>
#pragma comment(lib,"winmm.lib") // 导入声音头文件库

HANDLE hOutput;
COORD coord;
CONSOLE_CURSOR_INFO CursorInfo;
int TEST_MODE;

int main() {
	// 控制台参数配置.
	PlaySound(TEXT("BTS.wav"), NULL, SND_FILENAME | SND_ASYNC | SND_LOOP);
	hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
	coord = { 0, 0 };
	CursorInfo.bVisible = false;
	CursorInfo.dwSize = 1;
	TEST_MODE = 1;

	// 添加管理类并执行.
	admin a;
	a.AdminMain();
	return 0;
}
