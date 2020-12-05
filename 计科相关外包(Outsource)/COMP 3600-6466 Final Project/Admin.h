#pragma once
#include "common.h"
#include "KruskalMST.h"
#include "Graph.h"
#include "Dijkstra.h"
#include "HeapSort.h"
#include "DP.h"
class Admin {
public:
	Admin(string inputFileName): g(Graph(inputFileName)) {
		cout << "\n\n   <--- TEST FILE: " << inputFileName << " --->" << endl;
	}

	void main() {
		KruskalMST k;
		k.kruskal(g);
		k.print();
		
		Dijkstra d;
		int sourceNode = (rand() % g.n) + 1;
		cout << "Current source node(ID) is: " << sourceNode << endl;
		d.dijkstra(g, sourceNode);
		d.print();

		HeapSort h(d);
		h.run();
		h.print();

		DP dp(k.mst);
		dp.topo_sort();
	}

private:
	Graph g;
};

