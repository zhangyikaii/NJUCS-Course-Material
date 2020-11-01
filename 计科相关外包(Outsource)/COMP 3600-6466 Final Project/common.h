#pragma once

#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

#define For(i, a, b) for(register int i = a; i <= b; ++i)
#define re register

#define in(x) x=read()

struct Edge {
	int id;
	int u, v, w;
	int to, nex;
};

struct Node {
	int cost, id;
	Node() { }
	Node(int _cost, int _id) : cost(_cost), id(_id) { }
	bool operator <(const Node& x) const {
		return x.cost < cost;
	}
};

inline int read() {
	int X = 0, w = 1;
	char ch = getchar();
	while (ch<'0' || ch>'9') { if (ch == '-') w = -1; ch = getchar(); }
	while (ch >= '0' && ch <= '9') X = (X << 3) + (X << 1) + ch - '0', ch = getchar();
	return X * w;
}

#define CLASS_NUM 5000
#define MY_MAX_NUM 50000