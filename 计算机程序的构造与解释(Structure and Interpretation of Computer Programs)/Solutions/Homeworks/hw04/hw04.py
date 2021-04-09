from math import sqrt
LAB_SOURCE_FILE = "hw04.py"


def couple(lst1, lst2):
    """Return a list that contains lists with i-th elements of two sequences
    coupled together.
    >>> lst1 = [1, 2, 3]
    >>> lst2 = [4, 5, 6]
    >>> couple(lst1, lst2)
    [[1, 4], [2, 5], [3, 6]]
    >>> lst3 = ['c', 6]
    >>> lst4 = ['s', '1']
    >>> couple(lst3, lst4)
    [['c', 's'], [6, '1']]
    """
    assert len(lst1) == len(lst2)
    return [[lst1[i], lst2[i]] for i in range(len(lst1))]


def distance(city1, city2):
    """
    >>> city1 = make_city('city1', 0, 1)
    >>> city2 = make_city('city2', 0, 2)
    >>> distance(city1, city2)
    1.0
    >>> city3 = make_city('city3', 6.5, 12)
    >>> city4 = make_city('city4', 2.5, 15)
    >>> distance(city3, city4)
    5.0
    """
    return sqrt((get_lat(city1)-get_lat(city2))**2 + (get_lon(city1)-get_lon(city2))**2)


def closer_city(lat, lon, city1, city2):
    """
    Returns the name of either city1 or city2, whichever is closest to
    coordinate (lat, lon).

    >>> berkeley = make_city('Berkeley', 37.87, 112.26)
    >>> stanford = make_city('Stanford', 34.05, 118.25)
    >>> closer_city(38.33, 121.44, berkeley, stanford)
    'Stanford'
    >>> bucharest = make_city('Bucharest', 44.43, 26.10)
    >>> vienna = make_city('Vienna', 48.20, 16.37)
    >>> closer_city(41.29, 174.78, bucharest, vienna)
    'Bucharest'
    """
    anon_city = make_city('', lat, lon)
    if distance(anon_city, city1) < distance(anon_city, city2):
        return get_name(city1)
    return get_name(city2)


# Treat all the following code as being behind an abstraction layer, you shouldn't need to look at it!

def make_city(name, lat, lon):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_name(city)
    'Berkeley'
    >>> get_lat(city)
    0
    >>> get_lon(city)
    1
    """
    if change_abstraction.changed:
        return {"name": name, "lat": lat, "lon": lon}
    else:
        return [name, lat, lon]


def get_name(city):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_name(city)
    'Berkeley'
    """
    if change_abstraction.changed:
        return city["name"]
    else:
        return city[0]


def get_lat(city):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_lat(city)
    0
    """
    if change_abstraction.changed:
        return city["lat"]
    else:
        return city[1]


def get_lon(city):
    """
    >>> city = make_city('Berkeley', 0, 1)
    >>> get_lon(city)
    1
    """
    if change_abstraction.changed:
        return city["lon"]
    else:
        return city[2]


def change_abstraction(change):
    change_abstraction.changed = change


change_abstraction.changed = False


def nut_finder(t):
    """Returns True if t contains a node with the value 'nut' and
    False otherwise.

    >>> scrat = tree('nut')
    >>> nut_finder(scrat)
    True
    >>> sproul = tree('roots', [tree('branch1', [tree('leaf'), tree('nut')]), tree('branch2')])
    >>> nut_finder(sproul)
    True
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> nut_finder(numbers)
    False
    >>> t = tree(1, [tree('nut',[tree('not nut')])])
    >>> nut_finder(t)
    True
    """
    return label(t) == 'nut' or any([nut_finder(subtree) for subtree in branches(t)])


# Nut Finder: Solution 2
# 我们介绍使用Python的内置函数any()的解法。
# any()函数接受一个可迭代的对象，如果其中有个元素为True则返回True，否则返回False.
# 下面是一个简单的实现:
def my_any(iterable):
    for x in iterable:
        if x:
            return True
    return False
# 可以看到any()是上面Solution 1中循环(135-138行)的抽象，因此可以把上面的代码改写成：
def nut_finder2(t):
    if label(t) == 'nut':
        return True
    return any([nut_finder2(subtree) for subtree in branches(t)])
# 再进一步精简，就是以下代码：
def nut_finder3(t):
    return label(t) == 'nut' or any([nut_finder3(subtree) for subtree in branches(t)])


def sprout_leaves(t, values):
    """Sprout new leaves containing the data in values at each leaf in
    the original tree t and return the resulting tree.

    >>> t1 = tree(1, [tree(2), tree(3)])
    >>> print_tree(t1)
    1
      2
      3
    >>> new1 = sprout_leaves(t1, [4, 5])
    >>> print_tree(new1)
    1
      2
        4
        5
      3
        4
        5

    >>> t2 = tree(1, [tree(2, [tree(3)])])
    >>> print_tree(t2)
    1
      2
        3
    >>> new2 = sprout_leaves(t2, [6, 1, 2])
    >>> print_tree(new2)
    1
      2
        3
          6
          1
          2
    """
    if is_leaf(t):
        return tree(label(t), [tree(val) for val in values])
    return tree(label(t), [sprout_leaves(subtree, values) for subtree in branches(t)])


def add_trees(t1, t2):
    """
    >>> numbers = tree(1,
    ...                [tree(2,
    ...                      [tree(3),
    ...                       tree(4)]),
    ...                 tree(5,
    ...                      [tree(6,
    ...                            [tree(7)]),
    ...                       tree(8)])])
    >>> print_tree(add_trees(numbers, numbers))
    2
      4
        6
        8
      10
        12
          14
        16
    >>> print_tree(add_trees(tree(2), tree(3, [tree(4), tree(5)])))
    5
      4
      5
    >>> print_tree(add_trees(tree(2, [tree(3)]), tree(2, [tree(3), tree(4)])))
    4
      6
      4
    >>> print_tree(add_trees(tree(2, [tree(3, [tree(4), tree(5)])]), \
    tree(2, [tree(3, [tree(4)]), tree(5)])))
    4
      6
        8
        5
      5
    """
    br_1 = branches(t1)
    br_2 = branches(t2)
    new_subtrees = []
    for i in range(max(len(br_1), len(br_2))):
        if i < len(br_1):
            if i < len(br_2):
                new_subtrees.append(add_trees(br_1[i], br_2[i]))
            else:
                new_subtrees.append(br_1[i])
        else:
            assert i < len(br_2)
            new_subtrees.append(br_2[i])
    return tree(label(t1) + label(t2), new_subtrees)

# Add Trees: Solution 2
# 补全的写法：
def add_trees2(t1, t2):
    assert t1 or t2
    if not t2:
        return t1
    if not t1:
        return t2
    t1_subtrees, t2_subtrees = branches(t1), branches(t2)
    max_len = max(len(t1_subtrees), len(t2_subtrees))
    if len(t1_subtrees) < max_len:
        t1_subtrees += [None] * (max_len - len(t1_subtrees))
    if len(t2_subtrees) < max_len:
        t2_subtrees += [None] * (max_len - len(t2_subtrees))
    return tree(label(t1) + label(t2), [add_trees2(subtree1, subtree2)
                                        for subtree1, subtree2 in zip(t1_subtrees, t2_subtrees)])

# Solution 3
def add_trees3(t1, t2):
    assert t1 or t2
    if not t2:
        return t1
    if not t1:
        return t2

    def get_subtree(t, i):
        if i < len(branches(t)):
            return branches(t)[i]
        return None

    return tree(label(t1) + label(t2),
                [add_trees3(get_subtree(t1, i), get_subtree(t2, i))
                 for i in range(max(len(branches(t1)), len(branches(t2))))])


# Tree ADT

def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)


def label(tree):
    """Return the label value of a tree."""
    return tree[0]


def branches(tree):
    """Return the list of branches of the given tree."""
    return tree[1:]


def is_tree(tree):
    """Returns True if the given tree is a tree, and False otherwise."""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True


def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)


def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)


def copy_tree(t):
    """Returns a copy of t. Only for testing purposes.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])
