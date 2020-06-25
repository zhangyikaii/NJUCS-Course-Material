import math
ri, k, N = [3.2, 3.8, 1.2, 4, 2.8], 5, 5
alpha, F_test_threshold = 0.05, 3.007
q_alpha = 2.728 # for Nemenyi Test

tau_chi_square = 0
for i in ri:
    tau_chi_square += i * i
tau_chi_square = 12 * N / k / (k + 1) * (tau_chi_square - k * (k + 1) * (k + 1) / 4)

tau_F = (N - 1) * tau_chi_square / (N * (k - 1) - tau_chi_square)
print("\\tau_F = {}".format(tau_F))

assert k == 5 and N == 5 and alpha == 0.05

if tau_F <= F_test_threshold:
    print("Above algorithms have the same performance (fail to reject H0)")
else:
    print("Above algorithms have different performance (reject H0)")
    print("Continue to Nemenyi Test..")
    CD = q_alpha * math.sqrt(k * (k + 1) / 6 / N)

    diffTrue, diffFalse = [], []
    maxRiIndex = ri.index(max(ri))
    print("The best performing algorithms is {}, whose r_i = {}".format(maxRiIndex + 1, ri[maxRiIndex]))
    for i in range(len(ri)):
        if i != maxRiIndex:
            if abs(ri[i] - ri[maxRiIndex]) <= CD:
                diffTrue.append(i + 1)
            else:
                diffFalse.append(i + 1)

    print("The best performing algorithms differ significantly from the following: ")
    print(diffTrue)
    print("The best performing algorithms are not significantly different from the following: ")
    print(diffFalse)
    print("The index starts at one")