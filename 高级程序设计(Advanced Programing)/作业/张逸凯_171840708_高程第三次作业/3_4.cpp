#include <bits/stdc++.h>
using namespace std;

class Lion;

class Tiger {
public:
	Tiger() : weight(0) { }
	Tiger(int w) : weight(w) { }
	friend int totalWeights(const Lion& l, const Tiger& t);
private:
	int weight;
};

class Lion {
public:
	Lion() : weight(0) { }
	Lion(int w) : weight(w) { }
	friend int totalWeights(const Lion& l, const Tiger& t);
private:
	int weight;
};

int totalWeights(const Lion& l, const Tiger& t) {
	return l.weight + t.weight;
}

int main() {
	int w1, w2;
	cin >> w1 >> w2;
	Lion L(w1);
	Tiger T(w2);
	cout << totalWeights(L, T) << endl;

	return 0;
}