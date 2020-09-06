function accuracy = svm_predict_dual(X, y, model)
    predictions = X * model.X' * (model.a .* model.Y') - model.b > 0;
    accuracy = sum(predictions' == y) / size(predictions, 1);
end