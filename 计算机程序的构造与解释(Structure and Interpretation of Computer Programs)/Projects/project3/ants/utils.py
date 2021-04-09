def class_method_wrapper(method, pre=None, post=None):
    """Given a class METHOD and two wrapper function, a PRE-function and
    POST-function, first calls the pre-wrapper, calls the wrapped class method,
    and then calls the post-wrapper.

    All wrappers should have the parameters (self, rv, *args). However,
    pre-wrappers will always have `None` passed in as `rv`, since a return
    value has not been evaluated yet.

    >>> def pre_wrapper(instance, rv, *args):
    ...     print('Pre-wrapper called: {0}'.format(args))
    >>> def post_wrapper(instance, rv, *args):
    ...     print('Post-wrapper called: {0} -> {1}'.format(args, rv))
    >>> class Foo(object):
    ...     def __init__(self):
    ...         self.bar = 20
    ...     def method(self, var1, var2):
    ...         print('Original method called')
    ...         return var1 + var2 + self.bar
    >>> Foo.method = class_method_wrapper(Foo.method, pre_wrapper, post_wrapper)
    >>> f = Foo()
    >>> x = f.method(1, 2)
    Pre-wrapper called: (1, 2)
    Original method called
    Post-wrapper called: (1, 2) -> 23
    >>> x
    23
    """
    def wrapped_method(self, *args):
        pre(self, None, *args) if pre else None
        rv = method(self, *args)
        post(self, rv, *args) if post else None
        return rv
    return wrapped_method

def print_expired_insects(self, rv, *args):
    """Post-wrapper for Insect.reduce_armor, and will print a message if the
    insect has expired (armor reduced to 0).

    >>> from ants import Insect, Bee, ThrowerAnt, Place
    >>> Insect.reduce_armor = class_method_wrapper(Insect.reduce_armor,
    ...         pre=print_expired_insects)
    >>> place = Place('Test')
    >>> bee = Bee(3)
    >>> place.add_insect(bee)
    >>> bee.reduce_armor(2)
    >>> bee.reduce_armor(1)
    Bee(Test) ran out of armor and expired
    >>> thrower = ThrowerAnt()
    >>> place.add_insect(thrower)
    >>> thrower.reduce_armor(1)
    ThrowerAnt(Test) ran out of armor and expired
    """
    if self.armor <= args[0]:
        print('{0}({1}) ran out of armor and expired'.format(
            type(self).__name__, self.place))

def print_thrower_target(self, rv, *args):
    """Prints the target of a ThrowerAnt, if the ThrowerAnt found a target.

    >>> from ants import *
    >>> beehive = Hive(AssaultPlan())
    >>> dimensions = (1, 9)
    >>> gamestate = GameState(None, beehive, ant_types(), dry_layout, dimensions)
    >>> ThrowerAnt.nearest_bee = class_method_wrapper(ThrowerAnt.nearest_bee,
    ...         post=print_thrower_target)
    >>> thrower = ThrowerAnt()
    >>> short = ShortThrower()
    >>> bee = Bee(5)
    >>> gamestate.places['tunnel_0_1'].add_insect(short)
    >>> gamestate.places['tunnel_0_0'].add_insect(thrower)
    >>> gamestate.places['tunnel_0_5'].add_insect(bee)
    >>> thrower.action(gamestate)
    ThrowerAnt(1, tunnel_0_0) targeted Bee(5, tunnel_0_5)
    >>> short.action(gamestate)    # Bee not in range of ShortThrower
    >>> bee.action(gamestate)      # Bee moves into range
    >>> short.action(gamestate)
    ShortThrower(1, tunnel_0_1) targeted Bee(4, tunnel_0_4)
    """
    if rv is not None:
        print('{0} targeted {1}'.format(self, rv))