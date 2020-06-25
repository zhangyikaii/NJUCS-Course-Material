#include <iostream>
#include <fstream>
using namespace std;
const int MAX = 1000;

void sort_result(int a[], int n);
int main()
{
	fstream infile, outfile;
	infile.open("D:\\ex3_data.txt", ios::in);  // ¶ÁµÄ·½Ê½
	if (!infile)
	{
		cerr << "can't" << endl;
		return -1;
	}

	char ch[MAX];
	int sum[100] = { 0 }, i_sum = 0, result[100];

	while (!infile.eof())   
	{
		infile.getline(ch, sizeof(ch));   
		int temp = 0;
		for (int i = 0;; ++i)
		{
			if (ch[i] == ' ')
			{
				sum[i_sum] += temp;
				temp = 0;
				continue;
			}
			if (ch[i] == '\0')
			{
				sum[i_sum] += temp;
				break;
			}
			temp = temp * 10 + ch[i] - '0';
		}
		result[i_sum] = sum[i_sum];
		++i_sum;
	}


	infile.close();
	sort_result(result, i_sum);

	outfile.open("D:\\result.txt", ios::out);
	int i = 0;
	while (i_sum--)
	{
		outfile << result[i++] << endl;
	}

	return 0;
}

void sort_result(int a[], int n)
{
	for (int i = 0; i < n - 1; ++i)
	{
		int min = i;
		for (int k = i + 1; k < n; ++k)
		{
			if (a[min] > a[k])
				min = k;
		}
		int temp = a[min];
		a[min] = a[i];
		a[i] = temp;
	}

}