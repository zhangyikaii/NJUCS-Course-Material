function model = svm_train_primal(data_train, label_train, regularisation_para_C)

% primal form
[n, dim] = size(data_train);

cvx_begin
   cvx_precision low
   variables slack(n) w(dim) b
   minimize(w' * w + regularisation_para_C * sum(slack))
   subject to
        label_train' .* (data_train * w + b) >= 1 - slack;
        slack >= 0;
cvx_end

model = get_model(data_train, label_train, w, b);
end