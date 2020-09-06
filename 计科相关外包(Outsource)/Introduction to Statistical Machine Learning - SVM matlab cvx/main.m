%import the train data
clear
load train
data_train = X;
label_train = y;
load test;
data_test = X;
label_test = y;

%transform label to 1 and -1
label_train(label_train == 0) = -1;

regularisation_para_C = 0.5;

%train my svm in the primal
svm_model_primal = svm_train_primal(data_train, label_train, regularisation_para_C);

%train my svm in the dual
svm_model_dual = svm_train_dual(data_train, label_train, regularisation_para_C);
%test on your test data
test_accuracy = svm_predict_primal(data_test, label_test, svm_model_primal);
fprintf("SVM (Primal) Accuracy: %f\n", test_accuracy);

test_accuracy = svm_predict_dual(data_test, label_test, svm_model_dual);

fprintf("SVM (Dual) Accuracy: %f\n", test_accuracy);
