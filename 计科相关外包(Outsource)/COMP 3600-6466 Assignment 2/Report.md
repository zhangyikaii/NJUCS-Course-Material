# Report

### 2. [5 pt] Suppose n 6-sided fair dice are rolled independently. What is the expected sum of the outcome of these dice? Please provide the derivation.

解: 令 $X_i$ 为第 $i$ 个骰子投出的点数, 我们有:
$$
\mathbb{E}[\sum_i X_i] = \sum_i \mathbb{E}[X_i] \\= n \times \frac{1}{6} \times (1 + \cdots + 6) \\= \frac{7 n}{2}
$$

### 3.

解:

+ 稳定的排序算法定义为: 一个排序算法是稳定的, 如果具有相等键值的两个对象在排序输出后, 与它们在要排序的输入数组中以相同的顺序出现.

  插入排序、归并排序、计数排序是稳定的, 快速排序是不稳定的.

+ 原地算法的定义为: 基本上不需要额外辅助的数据结构完成, 或者说额外辅助的存储空间是与输入 $n$ 无关的常数大小 $\mathcal{O}(c)$ 空间.



### 4.

解: 

**(a)** 使用计数排序, 时间复杂度为 $\mathcal{O}(n + m)$, 空间复杂度为 $\mathcal{O}(n + m)$:

1. 设置从0 ~ m个桶, 这里存放这相应ID的文件. 可以用一次遍历找出当前文件的最小和最大的元素ID: $\mathcal{O}(n)$ 的查找复杂度.
2. 将每个文件移动到对应ID的桶内, 比如文件序列是: `2, 1, 0, 0, 3, 1`, 那么最后的桶序列就是: `0: 2, 1: 2, 2: 1, 3: 1`: $\mathcal{O}(n)$ 的移动复杂度.
3. 将每个桶内元素扩展成有序的排序: $\mathcal{O}(m)$ 的移动复杂度.

所以总复杂度为 $\mathcal{O}(n + m)$

**(b)** 要访问某一范围的文件, 只需访问对应的0~m个桶映射的有序排列即可, 比如(a)题中的例子, 0~m个桶为: 0: 2, 1: 2, 2: 1, 3: 1

需要访问ID为 1~2 的文件时, 则取出 `1: 2, 2: 1` 这两个桶映射的文件, 由于这里的取出桶即对应元素是 $\mathcal{O}(1)$ 的, 所以时间复杂度为 $\mathcal{O}(1)$ 即可找到需要的文件们.



### 5.

解: 

**(a)** 注意到所有元素是有区别的, 并且 $n = 2^k, \forall k > 0$, 考虑算法执行到 `Return unsuccessful`, 此时比较次数达到最大, 为worst case:

+ 以下证明, 算法第三行: `while s <= e do` 循环最多执行 $k + 1$ 次:

  注意到, 当 `e = s` 时进入循环, 有`m = s`, 此时如果 `A[m] != v`, 那么下一次循环即结束并跳出.

  + 问题等价于证明, 执行 $k$ 次后, $e - s = 1$ 为最坏情况:

    对于 $2^k$ 的序列, 算法的while循环每执行一次, `s`和`e`之间的范围就变为原来的$\frac{1}{2}$, 该性质由 `m = floor((s + e) / 2))` 可得.

    所以经过 $k$ 次执行后, s和e之间的范围变为1, 即 $k + 1$ 次执行后跳出循环, 最坏情况即为执行 $k$ 次.

+ 综上所述, 在跳出循环之前最后一次找到该元素, 则需要执行 $k$ 次, 即时间复杂度: $\mathcal{O}(k) = \mathcal{O}(\log n)$.

**(b)**

分析递归树, 我们有:
$$
\begin{array}{l}
\sum_{i=1}^{\log n}(\text {number of iterations in case i}) \times \text {(number of nodes in case i) } \div n \\
=\sum_{i=1}^{\log n} i \times \frac{1}{2^{i}} \\
=\frac{1}{2^{\log n}}+\cdots+\frac{1}{2^{2}}(\log (n-1)) +\frac{1}{2} \log N \\
\sim \mathcal{O}(log n)
\end{array}
$$



### 6.

**(a)** **不存在这样的随机算法**, 因为由题意我们有:
$$
0.3n < 4n - k < 0.6n \\
\Rightarrow 3.4n < k < 3.7n
$$
因为每个字符都是独立分布的, 则最坏情况为每个字母都是猜了5次才猜中, 概率为:
$$
\left( \frac{5}{6} \cdot \frac{4}{5} \cdot \frac{3}{4} \cdot \frac{2}{3} \cdot \frac{1}{2} \right)^n = \left( \frac{1}{6} \right)^n
$$
此时 $P = 4n - 5n = -n \notin (3.4n, \ 3.7n)$.

由adversary argument(对手论证), 不管算法设计者提出什么样的算法, 最坏情况总为每个字符猜5次, 这样总能达到最坏情况使 $P \notin (3.4n, \ 3.7n)$, 所以不存在得证.

**(b)**




### 7.

**(a)** 因为X, Y是两个独立的坐标/维度, 不妨讨论X坐标, Y坐标同理可证:

+ 当Town的个数为奇数, 即 $2k + 1$ 时, 注意到以下性质:

  + 对于任意Town点对 A, B, 且A的位置与B的位置不同, 则最优策略为Helipad建在A, B中间, 此时最优策略距离为 $|A - B|$(因为题中说了是曼哈顿距离).

    反证法: 反之若Helipad建在AB两点之间连线之外, 则有 $|A - Helipad| + |B - Helipad| > |A - B|$ 这由三角不等式可以得到. 所以原命题成立.

  + 不妨设 $2k + 1$ 个Town中距离中位数最近的左右两个Town为 $T_1, T_2$, 则由上述性质知道, 对于除了中位数的 $2k$ 个Town pair, Helipad必须建在 $T_1, T_2$ 之间, 此时优化问题转化为 ($H_{\theta}$ 为Helipad位置):
    $$
    \arg \min_{H_{\theta}} |H_\theta - median| + C
    $$
    其中$C$为常数, 即 $H_{\theta} = median$ 为中位数位置, 得证.

**(b)** 问题化归为modifying RandQuickSort实现数组的中位数查找算法.

+ 分析Quick Sort的Partition部分, 每次Partition数组中比median小的元素被放在前面, 比median大的元素被放在后面, 此时如果前后元素个数相同(或绝对值相差1), 则可以得到此时的pivot就是中位数.
+ 由上讨论我们可以发现, 每次Partition之后, 如果当前median前面的元素更多, 那么整个数组的中位数在当前median的前面. 依次类推, 算法每次在数组中随机选择一个数作为pivot, 在partition后判断整个数组中位数的位置, 递归地进行下一次partition.
+ 由随机算法的讨论分析得到, 且一次partition的时间复杂度为 $\mathcal{O}(n)$, 总时间复杂度为 $\mathcal{O}(n)$.