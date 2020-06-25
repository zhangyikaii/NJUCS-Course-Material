#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

#define MAX_SIZE 500
#define MAX_LEN 500 
// TEST = 1 是整型测试，TEST = 2是字符串测试 
#define TEST 1

// ********************************请在下方实现你的代码 ************* 

int int_cmp(const void *a,const void *b)
{
	// 请在下方实现你的代码
	int *aa = (int *)a, *bb = (int *)b;

	return *aa < *bb;
}

int str_cmp(const void *a,const void *b)
{
	// 请在下方实现你的代码
	char *aa = (char *)a, *bb = (char *)b;
	int na = 0, nb = 0;
	for (; *(aa + na) != '\0'; ++na);
	for (; *(bb + nb) != '\0'; ++nb);
	if (na == nb)
	{
		while (*aa != '\0' && *bb != '\0')
		{
			if (*aa < *bb)
				return 1;
			else if (*aa > *bb)
				return 0;
			++aa;
			++bb;
		}
	}
	else if (na < nb)
		return 1;
	else
		return 0;
}

/*
void sort(void *base, size_t num, size_t size, int (*comparator)(const void *, const void * ) )
{
	// 请在下方实现你的代码
	int i, j, gap;

	for (gap = num / 2; gap > 0; gap /= 2)
	{
		// gap个组执行插入排序
		for (i = 0; i < gap; i++)
		{
			for (j = i + gap; j < num; j += gap)
			{
				// 开始插入排序
				if (base[j] < base[j - gap])
				{
					int temp = base[j];
					int k = j - gap;
					while (k >= 0 && base[k] > temp)
					{
						base[k + gap] = base[k];
						k -= gap;
					}
					base[k + gap] = temp;
				}
			}
		}
	}
} 
*/

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
		if (*(p2 - 1) == '\0')
			flag2 = true;
	}

}

void sort(void *base, size_t num, size_t size, int(*comparator)(const void *, const void *))
{
	cout << "size:" << size << endl;
	cout << num << endl;

	int *pa = NULL;
	char *pb = NULL;
	if (size == (size_t)4)
	{
		pa = (int *)base;
		for (int i = 0; i < (int)num - 1; ++i)
		{
			int min = i;
			for (int k = min + 1; k < (int)num; ++k)
			{
				if (comparator(&pa[k], &pa[min]) == 1)
					min = k;
			}
			int temp = pa[min];
			pa[min] = pa[i];
			pa[i] = temp;
		}
	}
	else if (size == (size_t)500)
	{
		pb = (char *)base;
		for (int i = 0; i < (int)num * (int)size; i += size)
		{
			int min = i;
			for (int k = min + size; k < (int)num * (int)size; k += size)
			{
				if (comparator(&pb[k], &pb[min]) == 1)
					min = k;
			}
			exchange(&pb[min], &pb[i]);
		}
	}
}



// ********************************main供你自己测试使用*************** 
#if TEST==1

int main()
{
	int data[MAX_SIZE], n;
	cin >> n;
	for (int i = 0; i < n; i++)
	{
		int m;
		puts("*****************");
		cin >> m;
		for (int j = 0; j < m; j++)
			cin >> data[j];
		sort(data, m, sizeof(data[0]), int_cmp);
		puts("after sorting:");
		for (int j = 0; j < m; j++)
		{
			cout << data[j] << " ";
		}
		puts("\n*****************");
	}

	return 0;
}
#endif

#if TEST==2

int main()
{
	char str[500][MAX_LEN];
	int n;
	cin >> n;
	for (int i = 0; i < n; i++)
	{
		int m;
		cin >> m;
		for (int j = 0; j < m; j++)
		{
			cin >> str[j];
		}
		sort(str, m, sizeof(str[0]), str_cmp);
		cout << "*************" << endl;
		for (int j = 0; j < m; j++)
		{
			cout << str[j] << endl;
		}
		cout << "*************" << endl;
	}
	return 0;
}
#endif 
// NOTE: 以下注释片段是整型数据排序的测试代码，请勿修改，若修改后，助教测试出现错误， 后果自负 

/*
#if TEST==1

int main()
{
	int data[MAX_SIZE] , n;
	cin>>n;
	for(int i = 0 ; i < n ; i++)
	{
		int m;
		puts("*****************");
		cin>>m;
		for(int j = 0 ; j < m ; j++)
			cin>>data[j]; 
		sort(data, m, sizeof(data[0]), int_cmp);
		puts("after sorting:");
		for(int j = 0 ; j < m ; j++)
		{
			cout<<data[j]<<" ";
		}
		puts("\n*****************");
	}
	
	return 0;	
}
#endif

#if TEST==2

int main()
{
	char str[500][MAX_LEN];
	int n;
	cin>>n;
	for(int i = 0 ; i < n ; i++)
	{
		int m;
		cin>>m;
		for(int j = 0 ; j < m ; j++)
		{
			cin>>str[j];
		}
		sort(str, m, sizeof(str[0]), str_cmp);
		cout<<"*************"<<endl;
		for(int j = 0 ; j < m ; j++)
		{
			cout<<str[j]<<endl;
		}
		cout<<"*************"<<endl;
	}
	return 0;	
}
#endif 
*/


