import operator

from utils import comma_separated

class Expr:
    """
    When you type input into this interpreter, it is parsed (read) into an
    expression. This expression is represented in our code as an instance of
    this `Expr` class.

    In our interpreter, there are four types of expressions:
        - literals, which are simply numbers (e.g. 42 or 4.2)
        - names (e.g. my_awesome_variable_name)
        - call expressions (e.g. add(3, 4))
        - lambda expressions (e.g. lambda x: x)

    Call expressions and lambda expressions are built from simpler expressions.
    A lambda's body and a call expression's operator and operands are expressions
    as well. This means `Expr` is a recursive data structure, similar to a tree.
    This type of a tree is called an "abstract syntax tree".

    In our code, the four types of expressions are subclasses of the `Expr`
    class: `Literal`, `Name`, `CallExpr`, and `LambdaExpr`.
    """

    def __init__(self, *args):
        # The star (*) means that `args` will be a tuple of arguments passed to
        # this function.
        self.args = args

    def eval(self, env):
        """
        Each subclass of Expr implements its own eval method.

        `env` is a dictionary mapping strings to `Value` instances,
        representing the environment in which this expression is being
        evaluated.  This method should return a `Value` instance, the result of
        evaluating the expression.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Returns a parsable and human-readable string of this expression (i.e.
        what you would type into the interpreter).

        >>> expr = CallExpr(LambdaExpr(['x'], Name('x')), [Literal(5)])
        >>> str(expr)
        '(lambda x: x)(5)'
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Returns how this expression is written in our Python representation.

        >>> expr1 = LambdaExpr(['f'], CallExpr(Name('f'), [Literal(0)]))
        >>> expr1
        LambdaExpr(['f'], CallExpr(Name('f'), [Literal(0)]))

        >>> expr2 = CallExpr(LambdaExpr([], Literal(5)), [])
        >>> expr2
        CallExpr(LambdaExpr([], Literal(5)), [])
        """
        args = '(' + comma_separated([repr(arg) for arg in self.args]) + ')'
        return type(self).__name__ + args

class Literal(Expr):
    """A literal is notation for representing a fixed value in code. In
    PyCombinator, the only literals are numbers. A `Literal` should always
    evaluate to a `Number` value.

    The `value` attribute contains the fixed value the `Literal` refers to.
    """
    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def eval(self, env):
        return Number(self.value)

    def __str__(self):
        return str(self.value)

class Name(Expr):
    """A `Name` is a variable. When evaluated, we look up the value of the
    variable in the current environment.

    The `string` attribute contains the name of the variable (as a Python
    string).
    """
    def __init__(self, string):
        Expr.__init__(self, string)
        self.string = string

    def eval(self, env):
        """
        >>> env = {
        ...     'a': Number(1),
        ...     'b': LambdaFunction([], Literal(0), {})
        ... }
        >>> Name('a').eval(env)
        Number(1)
        >>> Name('b').eval(env)
        LambdaFunction([], Literal(0), {})
        >>> print(Name('c').eval(env))
        None
        """
        "*** YOUR CODE HERE ***"
        if self.string in env:
            return env[self.string]
        return None

    def __str__(self):
        return self.string

class LambdaExpr(Expr):
    """A lambda expression, which evaluates to a `LambdaFunction`.

    The `parameters` attribute is a list of variable names (a list of strings).
    The `body` attribute is an instance of `Expr`.

    For example, the lambda expression `lambda x, y: add(x, y)` is parsed as

    LambdaExpr(['x', 'y'], CallExpr(Name('add'), [Name('x'), Name('y')]))

    where `parameters` is the list ['x', 'y'] and `body` is the expression
    CallExpr('add', [Name('x'), Name('y')]).
    """
    def __init__(self, parameters, body):
        Expr.__init__(self, parameters, body)
        self.parameters = parameters
        self.body = body

    def eval(self, env):
        return LambdaFunction(self.parameters, self.body, env)

    def __str__(self):
        body = str(self.body)
        if not self.parameters:
            return 'lambda: ' + body
        else:
            return 'lambda ' + comma_separated(self.parameters) + ': ' + body

class CallExpr(Expr):
    """A call expression represents a function call.

    The `operator` attribute is an instance of `Expr`.
    The `operands` attribute is a list of `Expr` instances.

    For example, the call expression `add(3, 4)` is parsed as

    CallExpr(Name('add'), [Literal(3), Literal(4)])

    where `operator` is Name('add') and `operands` are [Literal(3), Literal(4)].
    """
    def __init__(self, operator, operands):
        Expr.__init__(self, operator, operands)
        self.operator = operator
        self.operands = operands

    def eval(self, env):
        """
        >>> from reader import read
        >>> new_env = global_env.copy()
        >>> new_env.update({'a': Number(1), 'b': Number(2)})
        >>> add = CallExpr(Name('add'), [Literal(3), Name('a')])
        >>> add.eval(new_env)
        Number(4)
        >>> new_env['a'] = Number(5)
        >>> add.eval(new_env)
        Number(8)
        >>> read('max(b, a, 4, -1)').eval(new_env)
        Number(5)
        >>> read('add(mul(3, 4), b)').eval(new_env)
        Number(14)
        """
        "*** YOUR CODE HERE ***"
        func = self.operator.eval(env)
        paras = [operand.eval(env) for operand in self.operands]
        return func.apply(paras)

    def __str__(self):
        function = str(self.operator)
        args = '(' + comma_separated(self.operands) + ')'
        if isinstance(self.operator, LambdaExpr):
            return '(' + function + ')' + args
        else:
            return function + args

class Value:
    """
    Values are the result of evaluating expressions. In an environment diagram,
    values appear on the right (either in a binding or off in the space to the
    right).

    In our interpreter, there are three types of values:
        - numbers (e.g. 42)
        - lambda functions, which are created by lambda expressions
        - primitive functions, which are functions that are built into the
            interpreter (e.g. add)

    In our code, the three types of values are subclasses of the `Value` class:
    Number, LambdaFunction, and PrimitiveFunction.
    """

    def __init__(self, *args):
        self.args = args

    def apply(self, arguments):
        """
        Each subclass of Value implements its own apply method.

        Note that only functions can be "applied"; attempting to apply a
        `Number` (e.g. as in 4(2, 3)) will error.

        For functions, `arguments` is a list of `Value` instances, the
        arguments to the function. It should return a `Value` instance, the
        result of applying the function to the arguments.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Returns a parsable and human-readable version of this value (i.e. the
        output of this value to be displayed in the interpreter).
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Returns how this value is written in our Python representation.
        """
        args = '(' + comma_separated([repr(arg) for arg in self.args]) + ')'
        return type(self).__name__ + args

class Number(Value):
    """A plain number. Attempting to apply a `Number` (e.g. as in 4(2, 3)) will error.

    The `value` attribute is the Python number that this represents.
    """
    def __init__(self, value):
        Value.__init__(self, value)
        self.value = value

    def apply(self, arguments):
        raise TypeError("Oof! Cannot apply number {} to arguments {}".format(
            self.value, comma_separated(arguments)))

    def __str__(self):
        return str(self.value)

class LambdaFunction(Value):
    """A lambda function. Lambda functions are created in the LambdaExpr.eval
    method. A lambda function is a lambda expression that knows the
    environment in which it was evaluated in.

    The `parameters` attribute is a list of variable names (a list of strings).
    The `body` attribute is an instance of `Expr`, the body of the function.
    The `parent` attribute is an environment, a dictionary with variable names
        (strings) as keys and instances of the class Value as values.
    """
    def __init__(self, parameters, body, parent):
        Value.__init__(self, parameters, body, parent)
        self.parameters = parameters
        self.body = body
        self.parent = parent

    def apply(self, arguments):
        """
        >>> from reader import read
        >>> add_lambda = read('lambda x, y: add(x, y)').eval(global_env)
        >>> add_lambda.apply([Number(1), Number(2)])
        Number(3)
        >>> add_lambda.apply([Number(3), Number(4)])
        Number(7)
        >>> sub_lambda = read('lambda add: sub(10, add)').eval(global_env)
        >>> sub_lambda.apply([Number(8)])
        Number(2)
        >>> add_lambda.apply([Number(8), Number(10)]) # Make sure you made a copy of env
        Number(18)
        >>> read('(lambda x: lambda y: add(x, y))(3)(4)').eval(global_env)
        Number(7)
        >>> read('(lambda x: x(x))(lambda y: 4)').eval(global_env)
        Number(4)
        """
        if len(self.parameters) != len(arguments):
            raise TypeError("Oof! Cannot apply number {} to arguments {}".format(
                comma_separated(self.parameters), comma_separated(arguments)))
        "*** YOUR CODE HERE ***"
        env = self.parent.copy()
        for i in range(len(self.parameters)):
            env[self.parameters[i]] = arguments[i]
        return self.body.eval(env)

    def __str__(self):
        definition = LambdaExpr(self.parameters, self.body)
        return '<function {}>'.format(definition)

class PrimitiveFunction(Value):
    """A built-in function. For a full list of built-in functions, see
    `global_env` at the bottom of this file.

    The `operator` attribute is a Python function takes Python numbers and
    returns a Python number.
    """
    def __init__(self, operator):
        Value.__init__(self, operator)
        self.operator = operator

    def apply(self, arguments):
        for arg in arguments:
            if type(arg) != Number:
                raise TypeError("Invalid arguments {} to {}".format(
                    comma_separated(arguments), self))
        return Number(self.operator(*[arg.value for arg in arguments]))

    def __str__(self):
        return '<primitive function {}>'.format(self.operator.__name__)

# The environment that the REPL evaluates expressions in.
global_env = {
    'abs': PrimitiveFunction(operator.abs),
    'add': PrimitiveFunction(operator.add),
    'float': PrimitiveFunction(float),
    'floordiv': PrimitiveFunction(operator.floordiv),
    'int': PrimitiveFunction(int),
    'max': PrimitiveFunction(max),
    'min': PrimitiveFunction(min),
    'mod': PrimitiveFunction(operator.mod),
    'mul': PrimitiveFunction(operator.mul),
    'pow': PrimitiveFunction(pow),
    'sub': PrimitiveFunction(operator.sub),
    'truediv': PrimitiveFunction(operator.truediv),
}