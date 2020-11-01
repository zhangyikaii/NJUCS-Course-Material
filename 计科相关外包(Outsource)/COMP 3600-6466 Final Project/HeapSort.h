#pragma once
#include "Dijkstra.h"
class HeapSort {
public:
	HeapSort() { }
	HeapSort(Dijkstra d) {
		int idx = 1;
		n = d.dst.size() - 1;
		For(i, 1, n) {
			nodeVec.push_back(Node(d.dst[i], idx));
			++idx;
		}
	}

	void run() {
		for (int i = n / 2 - 1; i >= 0; i--)
			heapify(n, i);

		for (int i = n - 1; i >= 0; i--) {
			swap(0, i);

			heapify(i, 0);
		}
	}

	void swap(int x, int y) {
		Node t = nodeVec[x];
		nodeVec[x] = nodeVec[y];
		nodeVec[y] = t;
	}

	void heapify(int n, int i) {
		int largest = i;
		int l = 2 * i + 1; // left = 2*i + 1
		int r = 2 * i + 2; // right = 2*i + 2

		if (l < n && nodeVec[l].cost > nodeVec[largest].cost)
			largest = l;

		if (r < n && nodeVec[r].cost > nodeVec[largest].cost)
			largest = r;

		if (largest != i) {
			swap(i, largest);

			heapify(n, largest);
		}
	}

	void print() {
		cout << "After heap sort, the path from the source point to the destination results in: (id, cost format)" << endl;
		for (auto i : nodeVec) {
			cout << "to: " << i.id << ", cost: " << i.cost << " | ";
		}

		cout << endl << endl;
	}

	vector<Node> nodeVec;

private:
	int n;
};

