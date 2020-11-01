#pragma once
#include "Graph.h"
#include "common.h"
class KruskalMST {
public:
	KruskalMST(): mstVal(0) { }

	void kruskal(Graph g) {
		sort(g.edge.begin(), g.edge.end(), cmp);

		int eu = 0, ev = 0, cnt = 0;
		For(i, 1, g.m) {
			eu = g.find(g.edge[i].u), ev = g.find(g.edge[i].v);
			if (eu == ev)
				continue;

			mstVal += g.edge[i].w;
			mst.push_back(g.edge[i]);

			g.fa[ev] = eu;
			if (++cnt == g.n - 1)
				break;
		}
	}

	void print() {
		cout << "Here are the edges that have been selected for the minimum spanning tree (<id, u, v, weight> format):" << endl;
		For(i, 0, mst.size() - 1)
			cout << "< " << mst[i].id << ", " << mst[i].u << ", " << mst[i].v << ", " << mst[i].w << " >, ";
		cout << endl << endl;
		cout << "The minimum total weight is: " << endl;
		cout << mstVal << endl << endl;
	}

	vector<Edge> mst;
	int mstVal;
private:
	static bool cmp(const Edge &a, const Edge &b) {
		return a.w < b.w;
	}
};