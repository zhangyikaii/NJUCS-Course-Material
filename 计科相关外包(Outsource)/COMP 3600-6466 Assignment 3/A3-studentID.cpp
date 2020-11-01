#include <iostream>
#include <algorithm>
#include <numeric>

#include <fstream>
#include <vector>

using namespace std;
int B, n;
int weight[1010][1010];
int dp[100010];
int* grpNum = NULL;
int i, k, j;

void dynamic_programming()
{
	for (i = 1; i <= n; ++i)
	{
		k = B;
		while (k >= 0)
		{
			for (j = 1; j <= grpNum[i]; ++j)
			{
				if (dp[k - weight[i][j]] + weight[i][j] >= dp[k] && k >= weight[i][j])
				{
					dp[k] = dp[k - weight[i][j]] + weight[i][j];
				}
			}
			--k;
		}
	}
}

int main(int argc, char* argv[]) {
	if (argc < 2) {
		std::cout << "Please supply the name of the input file\n";
	}
	else {
		ifstream inFile(argv[1]);
		
		inFile >> B >> n;
		B = B * 10;

		grpNum = new int[n + 1];
		for (i = 1; i <= n; i++)
		{
			inFile >> grpNum[i];

			for (j = 1; j <= grpNum[i]; j++)
			{
				inFile >> weight[i][j];
			}
		}
		inFile.close();

		int totSalaries = -1;
		vector<int> selApplicants(n + 1);
		vector<int> sumMin;
		for (i = 1; i <= n; ++i)
		{
			vector<int> tGrpVec(&weight[i][1], &weight[i][1 + grpNum[i]]);
			int minVal = *min_element(tGrpVec.begin(), tGrpVec.end());
			sumMin.push_back(minVal);
		}

		if (accumulate(sumMin.begin(), sumMin.end(), 0) > B)
		{
			cout << "no solution" << endl;
		}
		else
		{
			dynamic_programming();

			totSalaries = dp[B] * 1000;
			
			// set_path(selApplicants);

			cout << totSalaries << " ";
			for (i = 0; i < n; i++)
			{
				cout << selApplicants[i] << " ";
			}
			cout << "\n";
		}
	}

	return 0;
}