#include <iostream> 
#include <cstdio> 
#include <algorithm> 
#include <cstring>
#include <cmath>
#include <cstdlib>
#include <string>
#include <string.h>
#include <vector>
#include <queue>
#include <stack>
#include <map>
#include <set>
#include <functional>
#include <assert.h>

using namespace std;

#define in(x) x=read()

#define FOR(i, s, n) for(int i = s; i < n; ++i)

typedef long long ll;

inline int read() {
	int X = 0, w = 1;
	char ch = getchar();
	while (ch<'0' || ch>'9') { if (ch == '-') w = -1; ch = getchar(); }
	while (ch >= '0' && ch <= '9') X = (X << 3) + (X << 1) + ch - '0', ch = getchar();
	return X*w;
}

int main() {
	FILE *pf;
	pf = fopen("CommandLine.bat", "w");
	vector<string> arffFileName = {
		"breast-w",
		"colic",
		"credit-a",
		"credit-g",
		"diabetes",
		"hepatitis",
		"mozilla4",
		"pc1",
		"pc5",
		"waveform-5000"
	};

	vector<string> method = {
		".trees.J48",
		".bayes.NaiveBayes",
		".functions.LibSVM",
		".lazy.IBk",
		".functions.MultilayerPerceptron",
		".trees.RandomForest",
		".lazy.KStar"
	};

	vector<string> methodName = {
		"_J48",
		"_NaiveBayes",
		"_SVM",
		"_kNN",
		"_MultilayerPerceptron",
		"_RandomForest",
		"_KStar"
	};


	assert(methodName.size() == method.size());

	string res;

	string pre0 = "java weka.filters.unsupervised.attribute.ReplaceMissingValues -i ", /*arffFileName*/ pre1 = ".arff -o ", /*arffFileName*/ pre2 = "_preproccess.arff\n";

	FOR(i, 0, arffFileName.size()) {
		res = pre0 + arffFileName[i] + pre1 + arffFileName[i] + pre2;
		fputs(res.c_str(), pf);
		cout << res << endl;
	}
	string comm0 = "java weka.classifiers", /*method*/ comm1 = " -t ", /*arffFileName*/ comm2 = "_preproccess.arff -threshold-file C:\\Users\\Kai\\Desktop\\result\\Complete_result\\", /*arffFileName + methodName*/ comm3 = ".csv > C:\\Users\\Kai\\Desktop\\result\\Accuracy_result\\", /*arffFileName + methodName*/ comm4 = ".txt\n";


	FOR(i, 0, arffFileName.size()) {
		FOR(j, 0, method.size()) {
			res = comm0 + method[j] + comm1 + arffFileName[i] + comm2 + arffFileName[i] + methodName[j] + comm3 + arffFileName[i] + methodName[j] + comm4;
			fputs(res.c_str(), pf);
			cout << res << endl;
		}
	}

	fputs("pause\n", pf);

	fclose(pf);
	
	return 0;
}


/*

-h or -help
Output help information.
-synopsis or -info
Output synopsis for classifier (use in conjunction  with -h)
-t <name of training file>
Sets training file.
-T <name of test file>
Sets test file. If missing, a cross-validation will be performed
on the training data.
-c <class index>
Sets index of class attribute (default: last).
-x <number of folds>
Sets number of folds for cross-validation (default: 10).
-no-cv
Do not perform any cross validation.
-force-batch-training
Always train classifier in batch mode, never incrementally.
-split-percentage <percentage>
Sets the percentage for the train/test set split, e.g., 66.
-preserve-order
Preserves the order in the percentage split.
-s <random number seed>
Sets random number seed for cross-validation or percentage split
(default: 1).
-m <name of file with cost matrix>
Sets file with cost matrix.
-toggle <comma-separated list of evaluation metric names>
Comma separated list of metric names to toggle in the output.
All metrics are output by default with the exception of 'Coverage' and 'Region size'.
Available metrics:
Correct,Incorrect,Kappa,Total cost,Average cost,KB relative,KB information,
Correlation,Complexity 0,Complexity scheme,Complexity improvement,
MAE,RMSE,RAE,RRSE,Coverage,Region size,TP rate,FP rate,Precision,Recall,
F-measure,MCC,ROC area,PRC area
-l <name of input file>
Sets model input file. In case the filename ends with '.xml',
a PMML file is loaded or, if that fails, options are loaded
from the XML file.
-d <name of output file>
Sets model output file. In case the filename ends with '.xml',
only the options are saved to the XML file, not the model.
-v
Outputs no statistics for training data.
-o
Outputs statistics only, not the classifier.
-output-models-for-training-splits
Output models for training splits if cross-validation or percentage-split evaluation is used.
-do-not-output-per-class-statistics
Do not output statistics for each class.
-k
Outputs information-theoretic statistics.
-classifications "weka.classifiers.evaluation.output.prediction.AbstractOutput + options"
Uses the specified class for generating the classification output.
E.g.: weka.classifiers.evaluation.output.prediction.PlainText
-p range
Outputs predictions for test instances (or the train instances if
no test instances provided and -no-cv is used), along with the
attributes in the specified range (and nothing else).
Use '-p 0' if no attributes are desired.
Deprecated: use "-classifications ..." instead.
-distribution
Outputs the distribution instead of only the prediction
in conjunction with the '-p' option (only nominal classes).
Deprecated: use "-classifications ..." instead.
-r
Only outputs cumulative margin distribution.
-xml filename | xml-string
Retrieves the options from the XML-data instead of the command line.
-threshold-file <file>
The file to save the threshold data to.
The format is determined by the extensions, e.g., '.arff' for ARFF
format or '.csv' for CSV.
-threshold-label <label>
The class label to determine the threshold data for
(default is the first label)
-no-predictions
Turns off the collection of predictions in order to conserve memory.

Options specific to weka.classifiers.bayes.NaiveBayes:

-K
Use kernel density estimator rather than normal
distribution for numeric attributes
-D
Use supervised discretization to process numeric attributes

-O
Display model in old format (good when there are many classes)

-output-debug-info
If set, classifier is run in debug mode and
may output additional info to the console
-do-not-check-capabilities
If set, classifier capabilities are not checked before classifier is built
(use with caution).
-num-decimal-places
The number of decimal places for the output of numbers in the model (default 2).
-batch-size
The desired batch size for batch prediction  (default 100).

*/