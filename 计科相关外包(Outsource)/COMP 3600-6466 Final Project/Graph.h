#pragma once
#include "common.h"
class Graph {
public:
	Graph(string inputFileName) :
		inputFileName(inputFileName),
		n(0),
		m(0),
		edgeNum(0) {
		// ¶ÁÈ¡Êý¾Ý:
		freopen(inputFileName.c_str(), "r", stdin);
		in(n), in(m);
		fa = vector<int>(CLASS_NUM + 10);
		head = vector<int>(n + 1);
		for (re int i = 1; i <= n; i++) {
			fa[i] = i;
			head[i] = 0;
		}
		head[0] = 0;

		edge = vector<Edge>(m + 1);
		For(i, 1, m) {
			edge[i].id = i;
			in(edge[i].u), in(edge[i].v), in(edge[i].w);
			addEdge(edge[i].u, edge[i].v, i);
		}
	}

	void addEdge(int u, int v, int idx) {
		edge[idx].to = v;
		edge[idx].nex = head[u];
		head[u] = idx;
	}

	int find(int x) {
		while (x != fa[x]) x = fa[x] = fa[fa[x]];
		return x;
	}
	int n, m;
	vector<int> fa, head;
	vector<Edge> edge;

	int edgeNum;

private:
	string inputFileName;
};

