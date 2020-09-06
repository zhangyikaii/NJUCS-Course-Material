function accuracy = svm_predict_primal(X, y, model)
    predictions = X * model.a - model.b > 0;
    accuracy = sum(predictions' == y) / size(predictions, 1);
end