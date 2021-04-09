from typing import List


def make_withdraw(balance, password):
    """Return a password-protected withdraw function.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> error = w(90, 'hax0r')
    >>> error
    'Insufficient funds'
    >>> error = w(25, 'hwat')
    >>> error
    'Incorrect password'
    >>> new_bal = w(25, 'hax0r')
    >>> new_bal
    50
    >>> w(75, 'a')
    'Incorrect password'
    >>> w(10, 'hax0r')
    40
    >>> w(20, 'n00b')
    'Incorrect password'
    >>> w(10, 'hax0r')
    "Your account is locked. Attempts: ['hwat', 'a', 'n00b']"
    >>> w(10, 'l33t')
    "Your account is locked. Attempts: ['hwat', 'a', 'n00b']"
    >>> type(w(10, 'l33t')) == str
    True
    """
    i = 3
    attempts = []

    def clerk(amount, hisPassword):
        nonlocal balance
        nonlocal i
        nonlocal attempts
        nonlocal password
        if password == hisPassword and i > 0:
            if amount > balance:
                return 'Insufficient funds'
            else:
                balance -= amount
                return balance
        else:
            if i > 0:
                i -= 1
                attempts.append(hisPassword)
                return 'Incorrect password'
            else:
                return f"Your account is locked. Attempts: {attempts}"

    return clerk


def make_joint(withdraw, old_pass, new_pass):
    """Return a password-protected withdraw function that has joint access to
    the balance of withdraw.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> make_joint(w, 'my', 'secret')
    'Incorrect password'
    >>> j = make_joint(w, 'hax0r', 'secret')
    >>> w(25, 'secret')
    'Incorrect password'
    >>> j(25, 'secret')
    50
    >>> j(25, 'hax0r')
    25
    >>> j(100, 'secret')
    'Insufficient funds'

    >>> j2 = make_joint(j, 'secret', 'code')
    >>> j2(5, 'code')
    20
    >>> j2(5, 'secret')
    15
    >>> j2(5, 'hax0r')
    10

    >>> j2(25, 'password')
    'Incorrect password'
    >>> j2(5, 'secret')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> j(5, 'secret')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> w(5, 'hax0r')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> make_joint(w, 'hax0r', 'hello')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    """
    passwords = []
    something = withdraw(0, old_pass)
    if type(something) == str:
        return something
    else:
        passwords.append(new_pass)

    def Joint(amount, password):
        nonlocal passwords
        if password in passwords:
            return withdraw(amount, old_pass)
        else:
            return withdraw(amount, password)

    return Joint


def permutations(seq):
    """Generates all permutations of the given sequence. Each permutation is a
    list of the elements in SEQ in a different order. The permutations may be
    yielded in any order.

    >>> perms = permutations([100])
    >>> type(perms)
    <class 'generator'>
    >>> next(perms)
    [100]
    >>> try: #this piece of code prints "No more permutations!" if calling next would cause an error
    ...     next(perms)
    ... except StopIteration:
    ...     print('No more permutations!')
    No more permutations!
    >>> sorted(permutations([1, 2, 3])) # Returns a sorted list containing elements of the generator
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> sorted(permutations((10, 20, 30)))
    [[10, 20, 30], [10, 30, 20], [20, 10, 30], [20, 30, 10], [30, 10, 20], [30, 20, 10]]
    >>> sorted(permutations("ab"))
    [['a', 'b'], ['b', 'a']]
    """
    Made = []
    if type(seq) != list:
        seq = list(seq)
    if len(seq) == 0:
        return Made
    if len(seq) == 1:
        Made += [seq]
    else:
        new = seq[:]
        insertThing = new.pop(0)
        for temp in permutations(new):
            for j in range(len(temp) + 1):
                temp2 = temp[:]
                temp2.insert(j, insertThing)
                Made.append(temp2)
    yield from Made


class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Machine is out of stock.'
    >>> v.add_funds(15)
    'Machine is out of stock. Here is your $15.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'You must add $10 more funds.'
    >>> v.add_funds(7)
    'Current balance: $7'
    >>> v.vend()
    'You must add $3 more funds.'
    >>> v.add_funds(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.add_funds(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.add_funds(15)
    'Machine is out of stock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.restock(3)
    'Current soda stock: 6'
    >>> w.add_funds(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    balance = 0
    productCount = 0
    product = ''

    def __init__(self, proName, price):
        self.product = proName
        self.price = price

    def add_funds(self, fund):
        if self.productCount == 0:
            return f'Machine is out of stock. Here is your ${fund}.'
        self.balance += fund
        return f'Current balance: ${self.balance}'

    def restock(self, stock):
        self.productCount += stock
        return f'Current {self.product} stock: {self.productCount}'

    def vend(self):
        if self.productCount == 0:
            return 'Machine is out of stock.'
        if self.balance >= self.price:
            self.productCount -= 1
            change = self.balance - self.price
            self.balance = 0
            return f'Here is your {self.product}.' if change == 0 else \
                f'Here is your {self.product} and ${change} change.'
        return f'You must add ${self.price - self.balance} more funds.'
