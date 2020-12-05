#pragma once
#include "KruskalMST.h"

class DP {
public:
	DP() { }
	DP(vector<Edge>& mst) {
		m = mst.size();
		For(i, 0, mst.size() - 1) {
			//cout << mst[i].u << " | " << mst[i].v << endl;
			a[mst[i].u][mst[i].v] = 1;
			indeg[mst[i].v]++;
			n = max(max(n, mst[i].v), mst[i].u);
		}
	}

	void topo_sort()
	{
		for (int i = 1; i <= n; i++)
			if (indeg[i] == 0)
				q.push(i);
		while (!q.empty()) {
			const int u = q.front();
			ans[++cnt] = u;
			q.pop();
			for (int i = 1; i <= n; i++)
				if (a[u][i])
				{
					indeg[i]--;
					if (indeg[i] == 0)
						q.push(i);
				}
		}
		if (cnt < n) {
			cout << "There is a loop in topological sort" << endl;
			return;
		}
		cout << "The topological sort of the minimum spanning tree is:" << endl;
		cout << ans[1];
		for (int i = 2; i <= n; i++)
			cout << " -> " << ans[i];
		cout << endl;
	}

	//int core(vector<Edge> mst, int s, int t, map<int, int>& d) {
	//	if (s == t)
	//		return 0;
	//	if (d.find(s) != d.end()) {
	//		For(i, 0, ind[s].size()) {
	//			int cur = ind[s][i];
	//			d[s] = min(d[s], mst[cur].w + core(mst, mst[cur].v, t, d));
	//			return d[s];
	//		}
	//		
	//	}
	//}

private:
	int n, m, cnt;
	bool a[105][105];
	int indeg[1005], ans[1005];
	queue<int> q;
};

