// 这个 fwrite + 二进制 真的是驾驭不了啊 可是如果只把他改为 fprintf 就都对了.....

// 注意 报类似越界的错误 可能是 内存不够了MAX 太大 或 太小 数据放不够
// wb 形式 \n 写不进去???
// 是否一定要先用字符数组的形式读写 再转换成int double之类的数据数组?
#include <iostream>
#include <stdlib.h>
using namespace std;
const int MAX = 100;
const double eps = 1e-6;

void read_dat(FILE *pf);

int main()
{
	FILE *pf, *out0, *out1;
	errno_t err;
	err = fopen_s(&pf, "D:\\wine.txt", "r");
	if (err != NULL)
	{
		cerr << "can't open" << endl;
		exit(-1);
	}
	err = fopen_s(&out0, "D:\\wine_cpl.dat", "wb");
	if (err != NULL)
	{
		cerr << "can't open" << endl;
		exit(-1);
	}
	err = fopen_s(&out1, "D:\\wine_norm.csv", "w");
	if (err != NULL)
	{
		cerr << "can't open" << endl;
		exit(-1);
	}

	char oriWine[MAX * 2][MAX];   // 原来读取的字符数据(刚开始没想到直接读取double数据)
	//int unclear[MAX] = { 0 };
	int i_re = 0;

	double wine[MAX * 2][30] = { 0 };  // 转化的double数据

	while (!feof(pf))
	{
		fgets(oriWine[i_re++], sizeof(oriWine[0]), pf);
	}

	// 提取数据
	for (int k = 0; k < i_re; ++k)
	{
		int i_wine = 0;
		bool isInte = true;
		double temp_sum = 0, temp_poi = 0.1;
		for (int i = 0;; ++i)      // 这样风格好吗?
		{
			if (oriWine[k][i] == '\n' || oriWine[k][i] == '\0')
			{
				wine[k][i_wine++] = temp_sum;
				wine[k][i_wine] = -1;
				break;
			}

			//if (oriWine[k][i] == '#')   // 记录没有属性的位置
			//{
			//	cout << k << " " << i_wine << endl;
			//	cout << "######################" << endl;
			//	unclear[k] = i_wine + 1;
			//}

			else if (oriWine[k][i] == ',')  // 逗号
			{
				wine[k][i_wine++] = temp_sum;
				isInte = true;
				temp_sum = 0;
				temp_poi = 0.1;
			}

			else if (oriWine[k][i] == '.')  // 小数点
				isInte = false;

			else if (oriWine[k][i] <= '9' && oriWine[k][i] >= '0')
			{
				if (isInte == true)
					temp_sum = temp_sum * 10 + oriWine[k][i] - '0';
				else
				{
					temp_sum += temp_poi * (oriWine[k][i] - '0');
					temp_poi *= 0.1;
				}
			}
		}
	}

	// 处理没有属性的 (处理时就输出)
	for (int k = 0; k < i_re; ++k)
	{
		for (int i = 0; wine[k][i] != -1; ++i)
		{
			if (wine[k][i] == 0)
			{
				double temp_sum = 0;
				for (int n = 0; n < i_re; ++n)
					temp_sum += wine[n][i];

				wine[k][i] = temp_sum / (i_re - 1);
			}
			
			char a[MAX];
			char dou = ',', huan = '\n';
			if (wine[k][i + 1] != -1)
			{
				fwrite(&wine[k][i], sizeof(wine[k][i]), 1, out0);
				fwrite(&dou, sizeof(dou), 1, out0);
			}
			else
			{
				fwrite(&wine[k][i], sizeof(wine[k][i]), 1, out0);
				fwrite(&huan, sizeof(huan), 1, out0);
			}
		}
	}

	// max min 归一化
	for (int i = 1, k = 0; wine[k][i] != -1; ++i, k = 0)    // 这好像风格不好
	{
		double max = wine[k][i], min = wine[k][i];
		//double* const t = &wine[k][i];

		for (; k < i_re; ++k)
		{
			if (wine[k][i] > max)
				max = wine[k][i];
			if (wine[k][i] < min)
				min = wine[k][i];
		}
		for (k = 0; k < i_re; ++k)
		{
			if (max - min < eps)
				wine[k][i] = 1.0;
			else
				wine[k][i] = (wine[k][i] - min) / (max - min);
		}
	}

	// 输出到归一的文件
	for (int k = 0; k < i_re; ++k)
	{
		for (int i = 0; wine[k][i] != -1; ++i)
		{
			if (wine[k][i + 1] != -1)
				fprintf(out1, "%.1f,", wine[k][i]);
			else
				fprintf(out1, "%.1f\n", wine[k][i]);
		}
	}

	
			
			
	/*for (int i = 0; i < i_re; ++i)
	{
		double line_sum = 0;
		int t = unclear[i];
		if (t == 0)
			continue;
		for (int k = 0; k < i_re; ++k)
		{
			cout << t - 1 << endl;
			line_sum += wine[k][t - 1];
		}
		wine[i][t - 1] = line_sum / i_re;
	}*/
	


	fclose(pf);
	fclose(out0);
	fclose(out1);
	return 0;
}

void read_dat(FILE *pf)
{
	while (!feof(pf))
	{
		char ch = fgetc(pf);
		cout << ch;
	}
}