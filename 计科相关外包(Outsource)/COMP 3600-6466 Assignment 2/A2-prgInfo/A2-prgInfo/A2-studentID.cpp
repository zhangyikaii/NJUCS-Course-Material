#include <iostream>
#include <fstream>
// Add additional libraries you need here

using namespace std;

int main(int argc, char *argv[]) {
    if (argc < 2) {
        std::cout << "Please supply the name of the input file\n";
    } 
    else { 
		// Read input
		ifstream inFile(argv[1]);
		int n, x, y;
		inFile >> n;
		for (int i = 0; i < n; i++) {
			inFile  >> x >> y;
			// Store x and y data
		}
		inFile.close();  		

		int xh, yh;
		// Place your algorithm here
		// If you need to create a function, place the function above the main function
		// The results of your algorithm should be placed in variable xh and yh
		
		
		// Print output
        cout << xh << " " << yh << "\n";
    }

    return 0;
}
