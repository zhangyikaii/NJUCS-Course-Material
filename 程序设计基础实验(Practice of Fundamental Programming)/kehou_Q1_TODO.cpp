#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stack>
using namespace std;

struct QSORT
{
	int _left;
	int _right;
	QSORT()
	{
		_left = 0;
		_right = 0;
	}
	QSORT(int l, int r)
	{
		_left = l;
		_right = r;
	}
};

stack<QSORT> s;

//数组大小 
#define MAX_SIZE 1000

//#define sort(data, m)\
//for (int i = 0; i < m - 1; ++i)\
//{\
//	int min = i;for (int k = min + 1; k < m; ++k)\
//	{\
//		if (data[k] < data[min])\
//		min = k;\
//	}\
//	int temp = data[min];\
//	data[min] = data[i];\
//	data[i] = temp;\
//}


#define sort(arr, m)\
s.push(QSORT(0, m - 1)); \
while (!s.empty())\
{\
	QSORT temp = s.top(); \
	s.pop(); \
	int left = temp._left, right = temp._right; \
	int stan_temp = 0; \
	if (left <= right)\
	{\
		stan_temp = arr[left]; \
	while (left != right)\
	{\
		while (left < right && arr[right] >= stan_temp)\
			--right; \
		arr[left] = arr[right]; \
		while (left < right && arr[left] <= stan_temp)\
			++left; \
		arr[right] = arr[left]; \
	}\
		arr[right] = stan_temp; \
		s.push(QSORT(right + 1, temp._right)); \
		s.push(QSORT(temp._left, left - 1)); \
	}\
}



int main()
{
	//NOTE:你可以在这里进行测试 
	

	/*********************************/

	int data[MAX_SIZE], n;
	scanf_s("%d", &n);
	for (int i = 0; i < n; ++i)
	{
		int m;
		puts("*****************");
		scanf_s("%d", &m);
		for (int j = 0; j < m; j++)
			scanf_s("%d", data + j);
		sort(data, m);
		puts("after sorting:");
		for (int j = 0; j < m; j++)
		{
			printf_s("%d ", data[j]);
		}
		puts("\n*****************");
	}

	return 0;	
}

// NOTE: 以下注释片段是测试代码，请勿修改，若修改后，助教测试出现错误， 后果自负 
/*

int main()
{
	int data[MAX_SIZE] , n;
	scanf("%d",&n);
	for(int i = 0 ; i < n ; i++)
	{
		int m;
		puts("*****************");
		scanf("%d",&m);
		for(int j = 0 ; j < m ; j++)
			scanf("%d",data+j); 
		sort(data, m);
		puts("after sorting:");
		for(int j = 0 ; j < m ; j++)
		{
			printf("%d ",data[j]);
		}
		puts("\n*****************");
	}
	
	return 0;	
}
*/

