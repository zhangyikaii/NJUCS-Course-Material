java weka.filters.unsupervised.attribute.ReplaceMissingValues -i breast-w.arff -o breast-w_preproccess.arff
java weka.filters.unsupervised.attribute.ReplaceMissingValues -i colic.arff -o colic_preproccess.arff
java weka.filters.unsupervised.attribute.ReplaceMissingValues -i credit-a.arff -o credit-a_preproccess.arff
java weka.filters.unsupervised.attribute.ReplaceMissingValues -i credit-g.arff -o credit-g_preproccess.arff
java weka.filters.unsupervised.attribute.ReplaceMissingValues -i diabetes.arff -o diabetes_preproccess.arff
java weka.filters.unsupervised.attribute.ReplaceMissingValues -i hepatitis.arff -o hepatitis_preproccess.arff
java weka.filters.unsupervised.attribute.ReplaceMissingValues -i mozilla4.arff -o mozilla4_preproccess.arff
java weka.filters.unsupervised.attribute.ReplaceMissingValues -i pc1.arff -o pc1_preproccess.arff
java weka.filters.unsupervised.attribute.ReplaceMissingValues -i pc5.arff -o pc5_preproccess.arff
java weka.filters.unsupervised.attribute.ReplaceMissingValues -i waveform-5000.arff -o waveform-5000_preproccess.arff
java weka.classifiers.trees.J48 -t breast-w_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\breast-w_J48.csv > C:\Users\Kai\Desktop\result\Accuracy_result\breast-w_J48.txt
java weka.classifiers.bayes.NaiveBayes -t breast-w_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\breast-w_NaiveBayes.csv > C:\Users\Kai\Desktop\result\Accuracy_result\breast-w_NaiveBayes.txt
java weka.classifiers.functions.LibSVM -t breast-w_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\breast-w_SVM.csv > C:\Users\Kai\Desktop\result\Accuracy_result\breast-w_SVM.txt
java weka.classifiers.lazy.IBk -t breast-w_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\breast-w_kNN.csv > C:\Users\Kai\Desktop\result\Accuracy_result\breast-w_kNN.txt
java weka.classifiers.functions.MultilayerPerceptron -t breast-w_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\breast-w_MultilayerPerceptron.csv > C:\Users\Kai\Desktop\result\Accuracy_result\breast-w_MultilayerPerceptron.txt
java weka.classifiers.trees.RandomForest -t breast-w_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\breast-w_RandomForest.csv > C:\Users\Kai\Desktop\result\Accuracy_result\breast-w_RandomForest.txt
java weka.classifiers.lazy.KStar -t breast-w_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\breast-w_KStar.csv > C:\Users\Kai\Desktop\result\Accuracy_result\breast-w_KStar.txt
java weka.classifiers.trees.J48 -t colic_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\colic_J48.csv > C:\Users\Kai\Desktop\result\Accuracy_result\colic_J48.txt
java weka.classifiers.bayes.NaiveBayes -t colic_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\colic_NaiveBayes.csv > C:\Users\Kai\Desktop\result\Accuracy_result\colic_NaiveBayes.txt
java weka.classifiers.functions.LibSVM -t colic_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\colic_SVM.csv > C:\Users\Kai\Desktop\result\Accuracy_result\colic_SVM.txt
java weka.classifiers.lazy.IBk -t colic_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\colic_kNN.csv > C:\Users\Kai\Desktop\result\Accuracy_result\colic_kNN.txt
java weka.classifiers.functions.MultilayerPerceptron -t colic_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\colic_MultilayerPerceptron.csv > C:\Users\Kai\Desktop\result\Accuracy_result\colic_MultilayerPerceptron.txt
java weka.classifiers.trees.RandomForest -t colic_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\colic_RandomForest.csv > C:\Users\Kai\Desktop\result\Accuracy_result\colic_RandomForest.txt
java weka.classifiers.lazy.KStar -t colic_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\colic_KStar.csv > C:\Users\Kai\Desktop\result\Accuracy_result\colic_KStar.txt
java weka.classifiers.trees.J48 -t credit-a_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-a_J48.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-a_J48.txt
java weka.classifiers.bayes.NaiveBayes -t credit-a_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-a_NaiveBayes.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-a_NaiveBayes.txt
java weka.classifiers.functions.LibSVM -t credit-a_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-a_SVM.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-a_SVM.txt
java weka.classifiers.lazy.IBk -t credit-a_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-a_kNN.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-a_kNN.txt
java weka.classifiers.functions.MultilayerPerceptron -t credit-a_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-a_MultilayerPerceptron.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-a_MultilayerPerceptron.txt
java weka.classifiers.trees.RandomForest -t credit-a_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-a_RandomForest.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-a_RandomForest.txt
java weka.classifiers.lazy.KStar -t credit-a_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-a_KStar.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-a_KStar.txt
java weka.classifiers.trees.J48 -t credit-g_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-g_J48.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-g_J48.txt
java weka.classifiers.bayes.NaiveBayes -t credit-g_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-g_NaiveBayes.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-g_NaiveBayes.txt
java weka.classifiers.functions.LibSVM -t credit-g_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-g_SVM.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-g_SVM.txt
java weka.classifiers.lazy.IBk -t credit-g_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-g_kNN.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-g_kNN.txt
java weka.classifiers.functions.MultilayerPerceptron -t credit-g_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-g_MultilayerPerceptron.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-g_MultilayerPerceptron.txt
java weka.classifiers.trees.RandomForest -t credit-g_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-g_RandomForest.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-g_RandomForest.txt
java weka.classifiers.lazy.KStar -t credit-g_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\credit-g_KStar.csv > C:\Users\Kai\Desktop\result\Accuracy_result\credit-g_KStar.txt
java weka.classifiers.trees.J48 -t diabetes_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\diabetes_J48.csv > C:\Users\Kai\Desktop\result\Accuracy_result\diabetes_J48.txt
java weka.classifiers.bayes.NaiveBayes -t diabetes_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\diabetes_NaiveBayes.csv > C:\Users\Kai\Desktop\result\Accuracy_result\diabetes_NaiveBayes.txt
java weka.classifiers.functions.LibSVM -t diabetes_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\diabetes_SVM.csv > C:\Users\Kai\Desktop\result\Accuracy_result\diabetes_SVM.txt
java weka.classifiers.lazy.IBk -t diabetes_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\diabetes_kNN.csv > C:\Users\Kai\Desktop\result\Accuracy_result\diabetes_kNN.txt
java weka.classifiers.functions.MultilayerPerceptron -t diabetes_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\diabetes_MultilayerPerceptron.csv > C:\Users\Kai\Desktop\result\Accuracy_result\diabetes_MultilayerPerceptron.txt
java weka.classifiers.trees.RandomForest -t diabetes_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\diabetes_RandomForest.csv > C:\Users\Kai\Desktop\result\Accuracy_result\diabetes_RandomForest.txt
java weka.classifiers.lazy.KStar -t diabetes_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\diabetes_KStar.csv > C:\Users\Kai\Desktop\result\Accuracy_result\diabetes_KStar.txt
java weka.classifiers.trees.J48 -t hepatitis_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\hepatitis_J48.csv > C:\Users\Kai\Desktop\result\Accuracy_result\hepatitis_J48.txt
java weka.classifiers.bayes.NaiveBayes -t hepatitis_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\hepatitis_NaiveBayes.csv > C:\Users\Kai\Desktop\result\Accuracy_result\hepatitis_NaiveBayes.txt
java weka.classifiers.functions.LibSVM -t hepatitis_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\hepatitis_SVM.csv > C:\Users\Kai\Desktop\result\Accuracy_result\hepatitis_SVM.txt
java weka.classifiers.lazy.IBk -t hepatitis_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\hepatitis_kNN.csv > C:\Users\Kai\Desktop\result\Accuracy_result\hepatitis_kNN.txt
java weka.classifiers.functions.MultilayerPerceptron -t hepatitis_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\hepatitis_MultilayerPerceptron.csv > C:\Users\Kai\Desktop\result\Accuracy_result\hepatitis_MultilayerPerceptron.txt
java weka.classifiers.trees.RandomForest -t hepatitis_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\hepatitis_RandomForest.csv > C:\Users\Kai\Desktop\result\Accuracy_result\hepatitis_RandomForest.txt
java weka.classifiers.lazy.KStar -t hepatitis_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\hepatitis_KStar.csv > C:\Users\Kai\Desktop\result\Accuracy_result\hepatitis_KStar.txt
java weka.classifiers.trees.J48 -t mozilla4_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\mozilla4_J48.csv > C:\Users\Kai\Desktop\result\Accuracy_result\mozilla4_J48.txt
java weka.classifiers.bayes.NaiveBayes -t mozilla4_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\mozilla4_NaiveBayes.csv > C:\Users\Kai\Desktop\result\Accuracy_result\mozilla4_NaiveBayes.txt
java weka.classifiers.functions.LibSVM -t mozilla4_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\mozilla4_SVM.csv > C:\Users\Kai\Desktop\result\Accuracy_result\mozilla4_SVM.txt
java weka.classifiers.lazy.IBk -t mozilla4_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\mozilla4_kNN.csv > C:\Users\Kai\Desktop\result\Accuracy_result\mozilla4_kNN.txt
java weka.classifiers.functions.MultilayerPerceptron -t mozilla4_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\mozilla4_MultilayerPerceptron.csv > C:\Users\Kai\Desktop\result\Accuracy_result\mozilla4_MultilayerPerceptron.txt
java weka.classifiers.trees.RandomForest -t mozilla4_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\mozilla4_RandomForest.csv > C:\Users\Kai\Desktop\result\Accuracy_result\mozilla4_RandomForest.txt
java weka.classifiers.lazy.KStar -t mozilla4_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\mozilla4_KStar.csv > C:\Users\Kai\Desktop\result\Accuracy_result\mozilla4_KStar.txt
java weka.classifiers.trees.J48 -t pc1_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc1_J48.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc1_J48.txt
java weka.classifiers.bayes.NaiveBayes -t pc1_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc1_NaiveBayes.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc1_NaiveBayes.txt
java weka.classifiers.functions.LibSVM -t pc1_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc1_SVM.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc1_SVM.txt
java weka.classifiers.lazy.IBk -t pc1_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc1_kNN.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc1_kNN.txt
java weka.classifiers.functions.MultilayerPerceptron -t pc1_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc1_MultilayerPerceptron.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc1_MultilayerPerceptron.txt
java weka.classifiers.trees.RandomForest -t pc1_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc1_RandomForest.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc1_RandomForest.txt
java weka.classifiers.lazy.KStar -t pc1_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc1_KStar.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc1_KStar.txt
java weka.classifiers.trees.J48 -t pc5_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc5_J48.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc5_J48.txt
java weka.classifiers.bayes.NaiveBayes -t pc5_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc5_NaiveBayes.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc5_NaiveBayes.txt
java weka.classifiers.functions.LibSVM -t pc5_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc5_SVM.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc5_SVM.txt
java weka.classifiers.lazy.IBk -t pc5_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc5_kNN.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc5_kNN.txt
java weka.classifiers.functions.MultilayerPerceptron -t pc5_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc5_MultilayerPerceptron.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc5_MultilayerPerceptron.txt
java weka.classifiers.trees.RandomForest -t pc5_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc5_RandomForest.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc5_RandomForest.txt
java weka.classifiers.lazy.KStar -t pc5_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\pc5_KStar.csv > C:\Users\Kai\Desktop\result\Accuracy_result\pc5_KStar.txt
java weka.classifiers.trees.J48 -t waveform-5000_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\waveform-5000_J48.csv > C:\Users\Kai\Desktop\result\Accuracy_result\waveform-5000_J48.txt
java weka.classifiers.bayes.NaiveBayes -t waveform-5000_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\waveform-5000_NaiveBayes.csv > C:\Users\Kai\Desktop\result\Accuracy_result\waveform-5000_NaiveBayes.txt
java weka.classifiers.functions.LibSVM -t waveform-5000_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\waveform-5000_SVM.csv > C:\Users\Kai\Desktop\result\Accuracy_result\waveform-5000_SVM.txt
java weka.classifiers.lazy.IBk -t waveform-5000_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\waveform-5000_kNN.csv > C:\Users\Kai\Desktop\result\Accuracy_result\waveform-5000_kNN.txt
java weka.classifiers.functions.MultilayerPerceptron -t waveform-5000_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\waveform-5000_MultilayerPerceptron.csv > C:\Users\Kai\Desktop\result\Accuracy_result\waveform-5000_MultilayerPerceptron.txt
java weka.classifiers.trees.RandomForest -t waveform-5000_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\waveform-5000_RandomForest.csv > C:\Users\Kai\Desktop\result\Accuracy_result\waveform-5000_RandomForest.txt
java weka.classifiers.lazy.KStar -t waveform-5000_preproccess.arff -threshold-file C:\Users\Kai\Desktop\result\Complete_result\waveform-5000_KStar.csv > C:\Users\Kai\Desktop\result\Accuracy_result\waveform-5000_KStar.txt
pause
