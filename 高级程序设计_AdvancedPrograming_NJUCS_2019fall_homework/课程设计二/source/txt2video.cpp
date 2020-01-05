#include <bits/stdc++.h>
#include <windows.h>
using namespace std;

#define ROW 180
#define LINE 50

string figu[1010][100];
int cnt = 0;

void MyOutput(const int& cur) {
	for (int i = 0; i < LINE; ++i) {
		cout << figu[cur][i] << endl;
	}
}

int main() {
	FILE* fp;
	fp = fopen("start.txt", "r");
	char buf[100010] = "";
	while (!feof(fp)) {
		fgets(buf, 100000, fp);
		string s(buf);
		// system("cls");
		for (int i = 0, curBef = 0; i < LINE; ++i, curBef += ROW) {
			figu[cnt][i] = s.substr(curBef, ROW);
			// printf("%s\n", s.substr(curBef, ROW).c_str());
		}
		cnt++;
	}

	HANDLE hOutput;
	COORD coord = { 0, 0 };
	hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
	int befTime = GetTickCount(), refreshRate = 50;
	for (int i = 0; i < cnt; ++i) {
		while (GetTickCount() - refreshRate < befTime)
			;
		SetConsoleCursorPosition(hOutput, coord);
		MyOutput(i);
		befTime = GetTickCount();
	}
	return 0;
}