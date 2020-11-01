#pragma once
#include "Graph.h"
class Dijkstra {
public:
	Dijkstra() { }

	void print() {
		For(i, 1, dst.size() - 1)
			cout << "to: " << i << ", cost: " << dst[i] << " | ";
		cout << endl << endl;
	}
	void dijkstra(const Graph &g, int s) {
		dst = vector<int>(g.n + 1);
		vector<int> vis(g.n + 1);
		For(i, 0, g.n) {
			dst[i] = 0x7fffffff;
			vis[i] = 0;
		}

		dst[s] = 0;
		q.push(Node(0, s));
		while (!q.empty()) {
			Node tmp = q.top();
			q.pop();
			int x = tmp.id, d = tmp.cost;
			if (vis[x])
				continue;
			vis[x] = 1;
			for (int i = g.head[x]; i; i = g.edge[i].nex) {
				int y = g.edge[i].to;
				if (dst[y] > dst[x] + g.edge[i].w) {
					dst[y] = dst[x] + g.edge[i].w;
					if (!vis[y])
						q.push(Node(dst[y], y));
				}
			}
		}
	}

	vector<int> dst;
	std::priority_queue<Node> q;
};

