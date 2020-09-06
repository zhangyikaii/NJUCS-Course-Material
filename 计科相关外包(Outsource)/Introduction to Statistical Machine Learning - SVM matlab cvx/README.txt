
# Each train / test files have the same data - only the format differs - choose the one that you prefer working with

## Dataset description

The label (y) can take one of two classes - 0, 1;
In total, there are 200 features (X);
Trainset consists of 8500 samples, testset has 1500;

## Format description

data/*.csv - first column represents the label (i.e., y) and all other columns represent features (i.e., X); comma-separated
data/*.mat - matlab-file with 'X' (features) and 'y' (label) elements
data/*.libsvm - LIBSVM-format (first column is the label, all others are non-zero features together with their indices; more info is available here: https://www.csie.ntu.edu.tw/~r94100/libsvm-2.8/README) 
