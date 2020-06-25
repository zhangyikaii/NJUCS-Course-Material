#include "Shopping.h"

int Tran::WhereCity(string findCity)
{
	for (int x = 0; x < row_; ++x)
	{
		for (int y = 0; y < line_; ++y)
		{
			if (map_[x * row_ + y].w == CITY && map_[x * row_ + y].city == findCity)
				return x * row_ + y;
		}
	}
	return -1;
}

void Tran::InitChinaMap()
{
	int start1 = 2 * row_ + 2;
	int start2 = 5 * row_ + 5;
	int start3 = 7 * row_ + 8;

	// 初始化山峰
	for (int i = 0; i < 2; ++i)
		map_[i + start1].w = MOUN;
	for (int i = 0; i < 3; ++i)
		map_[i + start2].w = MOUN;
	for (int i = 0; i < 1; ++i)
		map_[i + start3].w = MOUN;

	set_map_city(0, 8, "北京");
	set_map_city(3, 7, "上海");
	set_map_city(6, 6, "厦门");
	set_map_city(6, 1, "重庆");
	set_map_city(9, 5, "广州");
	set_map_city(9, 8, "香港");
}

int Tran::Bfs(string start, string end)
{
	int minDis = 0;
	int sta = WhereCity(start);
	que_.push(sta);
	while (!que_.empty())
	{
		int temp = que_.front();
		que_.pop();
		int tx = temp / row_, ty = temp % row_;
		for (int k = 0; k < 4; ++k)
		{
			if (tx + xWays[k] < 0 || tx + xWays[k] >= line_ || ty + yWays[k] < 0 || ty + yWays[k] >= row_)
				continue;
			int temp_xy = (tx + xWays[k]) * row_ + ty + yWays[k];
			if (map_[temp_xy].w == ROAD)
			{
				map_[temp_xy].dis = map_[temp].dis + 1;
				que_.push(temp_xy);
			}
			else if (map_[temp_xy].city == end)
			{
				minDis += map_[temp].dis + 1;
				// cout << "bfs:" << minDis << endl;
				clear(que_);
				return minDis;
			}
		}
	}
	return -1;
}

void Tran::clear(queue<int>& q)
{
	queue<int> empty;
	swap(empty, q);
}

