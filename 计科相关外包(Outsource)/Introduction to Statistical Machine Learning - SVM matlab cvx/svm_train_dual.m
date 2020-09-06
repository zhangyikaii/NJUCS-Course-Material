function model = svm_train_dual(data_train, label_train, regularisation_para_C)

% dual form
[n, ~] = size(data_train);
e = ones(n, 1);
K = data_train * data_train';

cvx_begin
    cvx_precision low
    variable a(n)
    minimize (0.5 * a' * K * a - e' * a);
    subject to
        a >= 0;
        label_train * a == 0;
        a <= regularisation_para_C;
cvx_end

a(a < 10^-5) = 0;
data_train_t = data_train(a > 0, :);
label_train_t = label_train(a > 0);
a = a(a > 0);

b = mean(label_train' - (data_train * data_train_t') * (a .* label_train_t));

model = get_model(data_train_t, label_train_t, a, b);
end