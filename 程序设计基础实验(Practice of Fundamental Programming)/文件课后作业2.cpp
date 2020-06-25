// 哈哈老师您可以检查 quick 这个单词(在""里面)
#include <iostream>
#include <stdlib.h>
#include <cmath>
using namespace std;
const int MAX = 10000;

bool isSame(char a[], char b[], int n);
int main()
{
	char in[MAX];
	cin >> in;
	int n_in = 0;
	for (; in[n_in] != '\0'; ++n_in);

	FILE *pf;
	errno_t err;
	err = fopen_s(&pf, "D:\\sample.txt", "r");
	if (err != NULL)
	{
		cerr << "can't open" << endl;
		exit(-1);
	}

	char line[MAX];
	int ik = 0;
	while (!feof(pf))
	{
		++ik;
		char comp[MAX];
		int n_word = 0;
		fgets(line, sizeof(line), pf);

		// 截取一个单词
		for (int i = 0; i< MAX; ++i)
		{
			if ((line[i] < 'a' || line[i] > 'z') && (line[i] < 'A' || line[i] > 'Z'))
			{
				comp[n_word] = '\0';
				if (n_word == n_in && isSame(in, comp, n_in))
				{
					cout << "True" << endl;
					return 0;
				}
				if (line[i] == '\n' || line[i] == '\0')
					break;
				n_word = 0;
				continue;
			}
			comp[n_word++] = line[i];
		}
	}

	cout << "False" << endl;

	return 0;
}

bool isSame(char a[], char b[], int n)
{
	for (int i = 0; i < n; ++i)
	{
		bool flag = false;
		if (abs(a[i] - b[i]) >= 26)
		{
			flag = true;
			if (a[i] >= 'a' && a[i] <= 'z')
			{
				if (a[i] + 'A' - 'a' != b[i])
					return false;
			}
			else
			{
				if (a[i] + 'a' - 'A' != b[i])
					return false;
			}
		}

		if (flag == false && a[i] != b[i])
			return false;
	}

	return true;
}