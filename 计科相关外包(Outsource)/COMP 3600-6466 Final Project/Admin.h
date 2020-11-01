#pragma once
#include "common.h"
#include "KruskalMST.h"
#include "Graph.h"
#include "Dijkstra.h"
#include "HeapSort.h"
class Admin {
public:
	Admin(string inputFileName): g(Graph(inputFileName)) { }

	void main() {
		KruskalMST k;
		k.kruskal(g);
		k.print();

		
		
		Dijkstra d;
		int sourceNode = 4;
		cout << "Current source node(ID) is: " << sourceNode << endl;
		d.dijkstra(g, sourceNode);
		d.print();

		HeapSort h(d);
		h.run();
		h.print();
	}

private:
	Graph g;
};

