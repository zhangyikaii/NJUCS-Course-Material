this_file = 'lab05.py'


def make_adder_inc(n):
    """
    >>> adder1 = make_adder_inc(5)
    >>> adder2 = make_adder_inc(6)
    >>> adder1(2) 
    7
    >>> adder1(2) # 5 + 2 + 1
    8
    >>> adder1(10) # 5 + 10 + 2
    17
    >>> [adder1(x) for x in [1, 2, 3]]
    [9, 11, 13]
    >>> adder2(5)
    11
    """
    def adder(x):
        nonlocal n
        result = n + x
        n += 1
        return result
    return adder


def make_fib():
    """Returns a function that returns the next Fibonacci number
    every time it is called.

    >>> fib = make_fib()
    >>> fib()
    0
    >>> fib()
    1
    >>> fib()
    1
    >>> fib()
    2
    >>> fib()
    3
    >>> fib2 = make_fib()
    >>> fib() + sum([fib2() for _ in range(5)])
    12
    >>> from construct_check import check
    >>> # Do not use lists in your implementation
    >>> check(this_file, 'make_fib', ['List'])
    True
    """
    a, b = 0, 1
    def fib():
        nonlocal a, b
        result = a
        a, b = b, a+b
        return result
    return fib

# Generators

def naturals():
    """A generator function that yields the infinite sequence of natural
    numbers, starting at 1.

    >>> m = naturals()
    >>> type(m)
    <class 'generator'>
    >>> [next(m) for _ in range(10)]
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    i = 1
    while True:
        yield i
        i += 1


def scale(it, multiplier):
    """Yield elements of the iterable it scaled by a number multiplier.

    >>> m = scale([1, 5, 2], 5)
    >>> type(m)
    <class 'generator'>
    >>> list(m)
    [5, 25, 10]

    >>> m = scale(naturals(), 2)
    >>> [next(m) for _ in range(5)]
    [2, 4, 6, 8, 10]
    """
    for elem in it:
        yield elem * multiplier

# Solution 2
# 不能写：yield from [elem * multiplier for elem in it]
# 因为it可能是个无穷序列，这时候计算[elem * multiplier for elem in it]就不会终止。
# 怎么办？
# 
# map函数在手册上是这样描述的：
#   map(function, iterable, ...):
#     Return an iterator that applies function to every item of iterable, yielding the results.
# 也就是说，map函数是个“懒汉”：
#   它仅会在需要的时候调用x = next(iterable)读取iterable中的下一个值x，
#   接着计算function(x)，然后把结果yield给你，就不继续工作了。
# 相比而言，[elem * multiplier for elem in it]就很“勤快”：
#   它会试图把it中所有的值都读出来，然后组装成列表给你。
# 结果是，当it是一个无穷序列时（比如这里的naturals），
# 勤快的list comprehesion就永远无法完成工作了，
# 而懒惰的map能给你尽快提供结果。
# 
# “懒惰”这件事本质上还是通过yield来实现的。
# 所以各位现在应该会自己实现map函数了，下面给个参考实现：
# def map(function, iterable):
#     for x in iterable:
#         yield function(x)
# 使用样例：
# >>> it = map(lambda x: x * 2, naturals())
# >>> it is iter(it)
# True
# >>> next(it)
# 2
# >>> next(it)
# 4
# >>> next(it)
# 6
def scale2(it, multiplier):
    yield from map(lambda x: x * multiplier, it)

# 仔细想想，yield from其实为我们做抽象做了个很有意思的事情。
# 我们先举个例子来回顾一下关于抽象的知识。下面是两个简单的打印函数：
def mult_print(it, multiplier):
    for x in it:
        print(x * multiplier)

def add_print(it, adder):
    for x in it:
        print(x + adder)

# 学了SICP这门课后，大家应该会有意识的觉得这两个函数结构差不多，
# 所以应该把共通的地方抽象出来，变成新的函数foreach：
def foreach(it, do):
    for x in it:
        do(x)

# 于是:
def mult_print2(it, multiplier):
    foreach(it, lambda x: print(x * multiplier))

def add_print2(it, adder):
    foreach(it, lambda x: print(x + adder))

# 那么，对于generator如何抽象呢？比如我实现了两个generator：
def mult_gen(it, multiplier):
    for x in it:
        yield x * multiplier

def add_gen(it, adder):
    for x in it:
        yield x + adder

# 我想把共同的地方抽象出来，得到：
def foreach_yield(it, do):
    for x in it:
        yield do(x)

# 然而这样写肯定是错误的（Why?）：
def wrong_mult_gen2(it, multiplier):
    foreach_yield(it, lambda x: x * multiplier)

def wrong_add_gen2(it, adder):
    foreach_yield(it, lambda x: x + adder)

# 但这样写就对了（Why?）：
def mult_gen2(it, multiplier):
    yield from foreach_yield(it, lambda x: x * multiplier)

def add_gen2(it, adder):
    yield from foreach_yield(it, lambda x: x + adder)

# 仔细体会一下yield from在抽象中的作用：
# 它把一个generator中一段涉及yield的子代码代理给另一个generator去了，
# 就像先前的普通函数通过call expression把一段子代码代理给另一个普通函数去做一样。


def hailstone(n):
    """
    >>> for num in hailstone(10):
    ...     print(num)
    ...
    10
    5
    16
    8
    4
    2
    1
    """
    while True:
        yield n
        if n == 1:
            return
        if n % 2 == 0:
            n //= 2
        else:
            n = n * 3 + 1

# Solution2
# 首先把hailstone搞成递归的，并用list返回序列：
def hailstone_list(n):
    if n == 1:
        return [n]
    if n % 2 == 0:
        return [n] + hailstone_list(n // 2)
    return [n] + hailstone_list(n * 3 + 1)

# 然后很容易就改写成yield from形式:
def hailstone2(n):
    yield n
    if n == 1:
        return
    if n % 2 == 0:
        yield from hailstone2(n // 2)
    else:
        yield from hailstone2(n * 3 + 1)

# 当然你也可以直接通过前面一题讲的yield from的“代理”语义直接写出上面这个代码。