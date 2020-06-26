# 2019 转专业到计科经验分享



#### 机试

在计拔匡院的OJ上测的.

1. 括号匹配, 用栈即可.
2. 路径异或, 树上BFS.
3. special judge.

&nbsp;

#### 笔试

1. <img src="/tex/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode&sanitize=true" align=middle width=12.32879834999999pt height=22.465723500000017pt/>: 所有无穷收敛的有理数列的集合, 若<img src="/tex/905a106044dae51eeb2d27909c60ff78.svg?invert_in_darkmode&sanitize=true" align=middle width=66.49544714999999pt height=24.65753399999998pt/>, <img src="/tex/cf73c2eda310285baf15833663e9356a.svg?invert_in_darkmode&sanitize=true" align=middle width=109.43243849999999pt height=22.831056599999986pt/>, 则<img src="/tex/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode&sanitize=true" align=middle width=9.39498779999999pt height=14.15524440000002pt/>一定是有理数吗, 还有第二小题.

**解:** 梅加强老师数学分析习题有很多类似的.

2. 二部图<img src="/tex/5201385589993766eea584cd3aa6fa13.svg?invert_in_darkmode&sanitize=true" align=middle width=12.92464304999999pt height=22.465723500000017pt/>的顶点集可以划分为两个不相交的子集<img src="/tex/6bac6ec50c01592407695ef84f457232.svg?invert_in_darkmode&sanitize=true" align=middle width=13.01596064999999pt height=22.465723500000017pt/>和<img src="/tex/a9a3a4a202d80326bda413b5562d5cd1.svg?invert_in_darkmode&sanitize=true" align=middle width=13.242037049999992pt height=22.465723500000017pt/>, 图中的每条边都有一端在<img src="/tex/6bac6ec50c01592407695ef84f457232.svg?invert_in_darkmode&sanitize=true" align=middle width=13.01596064999999pt height=22.465723500000017pt/>中, 另一端在<img src="/tex/a9a3a4a202d80326bda413b5562d5cd1.svg?invert_in_darkmode&sanitize=true" align=middle width=13.242037049999992pt height=22.465723500000017pt/>中，<img src="/tex/6bac6ec50c01592407695ef84f457232.svg?invert_in_darkmode&sanitize=true" align=middle width=13.01596064999999pt height=22.465723500000017pt/>中有2019个顶点，<img src="/tex/6bac6ec50c01592407695ef84f457232.svg?invert_in_darkmode&sanitize=true" align=middle width=13.01596064999999pt height=22.465723500000017pt/>中每个顶点的出度至少为<img src="/tex/2b30cda6d5081c4939e03b559613ea66.svg?invert_in_darkmode&sanitize=true" align=middle width=18.401941799999996pt height=33.20539859999999pt/>.

   1. 证明：$V$中一定存在一个子集$X$，$|X| \leq 10$，$U$中的每一个顶点都在$X$中有一个邻居。

   **解:** (有点难, 我证的可能是伪证)

   考虑$V$中度数最大的点$v_1$, 有$\frac{2019|V|}{2} \leq |E(G)| \leq d(v_1)$, 即$\frac{2019}{2} \text{取整} \leq d(v_1)$.

   考虑以下算法:

   令$V^{\prime} = V - v_1, G^{\prime} = G - v_1$, $E(G^{\prime}) \leq \frac{2019}{2}$. 

   取$V^{\prime}$中度数最大的点$v_2$. 有
   $$
   d(v_2)(|G^{\prime}|) = d(v_2)(|V| - 1) \geq \frac{2019(|V| - 1)}{2^2} \\ \Rightarrow d(v_2) \geq \frac{2019}{2^2} \\ \cdots
   $$
   重复到$v_{10}$, 此时$\frac{2019}{2^{10}} < 1$.

3. 8阶群一定有4阶子群吗？（证明或举反例）

**解:** 曲老师离散数学书上有证明6阶群必有3阶子群, 证明思路为使用Lagrange定理分类讨论.

4. 构造一个函数<img src="/tex/cf23450151a368a8b73be5295d28b948.svg?invert_in_darkmode&sanitize=true" align=middle width=47.95292369999999pt height=24.65753399999998pt/>, 使<img src="/tex/bc18e69939409035797b80c12b9ae5ef.svg?invert_in_darkmode&sanitize=true" align=middle width=138.7595352pt height=33.187449900000026pt/>在<img src="/tex/d168c92829058f6af31167b13cce26f0.svg?invert_in_darkmode&sanitize=true" align=middle width=36.52973609999999pt height=24.65753399999998pt/>上连续, 对任意<img src="/tex/962c64bf70430f1364bf415ee4dd9db7.svg?invert_in_darkmode&sanitize=true" align=middle width=65.31002774999997pt height=24.65753399999998pt/>, <img src="/tex/224d4a787f2b0bad65c95785e58dbbd4.svg?invert_in_darkmode&sanitize=true" align=middle width=100.07047544999998pt height=24.65753399999998pt/>在<img src="/tex/d168c92829058f6af31167b13cce26f0.svg?invert_in_darkmode&sanitize=true" align=middle width=36.52973609999999pt height=24.65753399999998pt/>上不连续.

**解:** 很有趣的题, 我当时构造了一个在<img src="/tex/7defd50098be0a3d3e6d4bf5ca764b65.svg?invert_in_darkmode&sanitize=true" align=middle width=39.96184334999999pt height=14.15524440000002pt/>上的Dirac函数, <img src="/tex/38f1e2a089e53d5c990a82f284948953.svg?invert_in_darkmode&sanitize=true" align=middle width=7.928075099999989pt height=22.831056599999986pt/>函数. 详细地说, 在定义域为<img src="/tex/65f1b48fb5f326a680b0f7393b9d8b6d.svg?invert_in_darkmode&sanitize=true" align=middle width=18.044213549999988pt height=14.15524440000002pt/>平面上当<img src="/tex/7defd50098be0a3d3e6d4bf5ca764b65.svg?invert_in_darkmode&sanitize=true" align=middle width=39.96184334999999pt height=14.15524440000002pt/>时, <img src="/tex/ff47eb715f73a82b518a0ef4303b788c.svg?invert_in_darkmode&sanitize=true" align=middle width=102.74736119999997pt height=24.65753399999998pt/>(类似Dirac function零点位置)而其他为零, 也即对于垂直于<img src="/tex/65f1b48fb5f326a680b0f7393b9d8b6d.svg?invert_in_darkmode&sanitize=true" align=middle width=18.044213549999988pt height=14.15524440000002pt/>平面且与<img src="/tex/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode&sanitize=true" align=middle width=9.39498779999999pt height=14.15524440000002pt/>轴平行的平面 与 <img src="/tex/cf23450151a368a8b73be5295d28b948.svg?invert_in_darkmode&sanitize=true" align=middle width=47.95292369999999pt height=24.65753399999998pt/>相截的图形就是一个平移后的Dirac函数, 所以<img src="/tex/bc18e69939409035797b80c12b9ae5ef.svg?invert_in_darkmode&sanitize=true" align=middle width=138.7595352pt height=33.187449900000026pt/>在<img src="/tex/d168c92829058f6af31167b13cce26f0.svg?invert_in_darkmode&sanitize=true" align=middle width=36.52973609999999pt height=24.65753399999998pt/>上连续. 与<img src="/tex/deceeaf6940a8c7a5a02373728002b0f.svg?invert_in_darkmode&sanitize=true" align=middle width=8.649225749999989pt height=14.15524440000002pt/>轴平行同理. 不连续用定义说明即可.

5. 数电简单题.

&nbsp;

#### 面试

1. 修了哪些课程, 成绩如何, 之后根据这些课程提问.
2. 数理逻辑: 谓词逻辑和一阶逻辑的区别.
3. ICS: PA做了啥.
4. 关于获奖的一些问题.
5. 然后开始唠嗑.

努力就好! :star2:

Update at 2020-2-3 19:29:42, 别怕, 武汉加油, 中国加油!

Update at 2020-6-25 23:18:00, 向阳而生, 逆风飞翔!

