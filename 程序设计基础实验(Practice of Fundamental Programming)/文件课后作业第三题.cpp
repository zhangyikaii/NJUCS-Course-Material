#include <iostream>
#include <stdlib.h>
using namespace std;
const int MAX = 101;

int main()
{
	// 打开文件
	FILE *pf;
	errno_t err;
	err = fopen_s(&pf, "D:\\sample.txt", "r+");
	if (err != NULL)
	{
		cerr << "can't open" << endl;
		exit(-1);
	}

	// 更改
	char a[MAX];
	int b;
	cin >> b >> a;
	fseek(pf, b - 1, SEEK_SET);
	fputs(a, pf);

	fclose(pf);

	return 0;
}
