#include "Admin.h"

int main() {
	srand(time(NULL));

	int testNum = 5;
	For(i, 1, testNum) {
		string fileName = "test-fi-" + to_string(i) + ".txt";
		Admin a(fileName);
		a.main();
	}

	return 0;
}