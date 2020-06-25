#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#include <iostream>
using namespace std;
bool check_word(char *p1, char *p2);
void exchange(char *p1, char *p2);


//字符串长度
#define MAX_LEN 101 
// 数组大小 
#define SIZE 201

void sort(char (*strings)[MAX_LEN], int n)
{
	// NOTE: 你需要在下面实现代码 
	int output[MAX_LEN] = { 0 }, outp = 0;
	int nword[MAX_LEN] = { 0 };
	bool used[MAX_LEN] = { 0 };

	for (int i = 0; i < n; ++i)
	{
		int num = 0;
		for (num = 0; strings[i][num] != '\0'; ++num);
		nword[i] = num;
	}

	for (int k = 0; k < n; ++k)
	{
		int min = k, i = 0;

		for (; i < n; ++i)
		{
			if (nword[i] < nword[min])
				min = i;
			else if (nword[i] == nword[min] && check_word(&strings[min][0], &strings[i][0]) != true)
				min = i;
		}

		exchange(strings[min], strings[k]);
	}
}


//int main()
//{
//	//NOTE:你自己测试使用
//	char str[SIZE][MAX_LEN];
//	int n = 1;
//	for (int i = 0; i < n; ++i)
//	{
//		int m = 3;
//		for (int j = 0; j < m; ++j)
//			cin >> str[j];
//
//		sort(str, m);
//
//	}
//
//
//	return 0;	
//}


// NOTE: 以下注释片段是测试代码，请勿修改，若修改后，助教测试出现错误， 后果自负 


int main()
{
	char str[SIZE][MAX_LEN];
	int n;
	cin >> n;
	for(int i = 0 ; i < n ; i++)
	{
		int m;
		cin >> m;
		for(int j = 0 ; j < m ; j++)
		{
			cin >> str[j];
		}
		sort(str, m);
		puts("*************");
		for(int j = 0 ; j < m ; j++)
		{
			cout << str[j] << endl;
		}
		puts("*************");
	}
	return 0;	
}



bool check_word(char *p1, char *p2)
{
	for (int i = 0; p1[i] != '\0' && p2[i] != '\0'; ++i)
	{
		if (p1[i] < p2[i])
			return true;
		else if (p1[i] > p2[i])
			return false;
	}
}

void exchange(char *p1, char *p2)
{
	bool flag1 = false, flag2 = false;
	while (flag1 == false || flag2 == false)
	{
		char temp = *p1;
		*p1 = *p2;
		*p2 = temp;

		++p1;
		++p2;
		if (*(p1 - 1) == '\0')
			flag1 = true;
		if (*(p2 - 1)== '\0')
			flag2 = true;
	}

}

