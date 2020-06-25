#include <bits/stdc++.h>
using namespace std;

class Component
{
public:
	Component() : Weight(0) { }
	Component(int w) : Weight(w) {
		TotalWeights += Weight;
	}
	~Component();

	int GetWeights();

	static int TotalWeights;
private:
	int Weight;
};

int Component::TotalWeights = 0;	// ³õÊ¼»¯.

int Component::GetWeights() {
	return this->Weight;
}

Component::~Component() {
	TotalWeights -= Weight;
}

int main() {
	int a, b;
	cin >> a >> b;
	Component A(a);
	Component B(b);

	cout << B.TotalWeights << endl;
	return 0;
}