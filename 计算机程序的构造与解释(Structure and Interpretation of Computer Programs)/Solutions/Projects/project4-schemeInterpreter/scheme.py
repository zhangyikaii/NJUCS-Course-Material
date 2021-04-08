"""A Scheme interpreter and its read-eval-print loop."""
from __future__ import print_function  # Python 2 compatibility

import sys
import os

from scheme_builtins import *
from scheme_reader import *
from ucb import main, trace

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in environment ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        return SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 4
        procedure = scheme_eval(first, env)
        validate_procedure(procedure)
        if isinstance(procedure, MacroProcedure):
            val = procedure.apply_macro(rest, env)
            return scheme_eval(val, env)
        args = rest.map(lambda e: scheme_eval(e, env))
        return scheme_apply(procedure, args, env)
        # END PROBLEM 4


def self_evaluating(expr):
    """Return whether EXPR evaluates to itself."""
    return (scheme_atomp(expr) and not scheme_symbolp(expr)) or expr is None


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    environment ENV."""
    if isinstance(procedure, BuiltinProcedure):
        return procedure.apply(args, env)
    else:
        new_env = procedure.make_call_frame(args, env)
        return eval_all(procedure.body, new_env)


def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    environment ENV and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 7
    result = None
    while expressions is not nil:
        tail = (expressions.rest is nil)
        result = scheme_eval(expressions.first, env, tail)
        expressions = expressions.rest
    return result
    # END PROBLEM 7

################
# Environments #
################


class Frame(object):
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        # BEGIN PROBLEM 2
        self.bindings[symbol] = value
        # END PROBLEM 2

    def lookup(self, symbol):
        """Return the value bound to SYMBOL. Errors if SYMBOL is not found."""
        # BEGIN PROBLEM 2
        if symbol in self.bindings:
            return self.bindings[symbol]
        if self.parent:
            return self.parent.lookup(symbol)
        # END PROBLEM 2
        raise SchemeError('unknown identifier: {0}'.format(symbol))

    def make_child_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in a Scheme list of formal parameters FORMALS are bound to the Scheme
        values in the Scheme list VALS. Raise an error if too many or too few
        vals are given.

        >>> env = create_global_frame()
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        if len(formals) != len(vals):
            raise SchemeError('Incorrect number of arguments to function call')
        # BEGIN PROBLEM 10
        child_frame = Frame(self)
        formal, val = formals, vals
        while formal is not nil and val is not nil:
            child_frame.define(formal.first, val.first)
            formal, val = formal.rest, val.rest
        return child_frame
        # END PROBLEM 10

##############
# Procedures #
##############


class Procedure(object):
    """The supertype of all Scheme procedures."""


def scheme_procedurep(x):
    return isinstance(x, Procedure)


class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, fn, use_env=False, name='builtin'):
        self.name = name
        self.fn = fn
        self.use_env = use_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

    def apply(self, args, env):
        """Apply SELF to ARGS in ENV, where ARGS is a Scheme list (a Pair instance).

        >>> env = create_global_frame()
        >>> plus = env.bindings['+']
        >>> twos = Pair(2, Pair(2, nil))
        >>> plus.apply(twos, env)
        4
        """
        if not scheme_listp(args):
            raise SchemeError('arguments are not in a list: {0}'.format(args))
        # Convert a Scheme list to a Python list
        python_args = []
        # BEGIN PROBLEM 3
        node = args
        while node is not nil:
            python_args.append(node.first)
            node = node.rest
        if self.use_env:
            python_args.append(env)
        # END PROBLEM 3
        try:
            return self.fn(*python_args)
        except TypeError as err:
            raise SchemeError(
                'incorrect number of arguments: {0}'.format(self))


class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        assert isinstance(env, Frame), "env must be of type Frame"
        validate_type(formals, scheme_listp, 0, 'LambdaProcedure')
        validate_type(body, scheme_listp, 1, 'LambdaProcedure')
        self.formals = formals
        self.body = body
        self.env = env

    def make_call_frame(self, args, env):
        """Make a frame that binds my formal parameters to ARGS, a Scheme list
        of values, for a lexically-scoped call evaluated in environment ENV."""
        # BEGIN PROBLEM 11
        return self.env.make_child_frame(self.formals, args)
        # END PROBLEM 11

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))


class MacroProcedure(LambdaProcedure):
    """A macro: a special form that operates on its unevaluated operands to
    create an expression that is evaluated in place of a call."""

    def apply_macro(self, operands, env):
        """Apply this macro to the operand expressions."""
        return complete_apply(self, operands, env)


def add_builtins(frame, funcs_and_names):
    """Enter bindings in FUNCS_AND_NAMES into FRAME, an environment frame,
    as built-in procedures. Each item in FUNCS_AND_NAMES has the form
    (NAME, PYTHON-FUNCTION, INTERNAL-NAME)."""
    for name, fn, proc_name in funcs_and_names:
        frame.define(name, BuiltinProcedure(fn, name=proc_name))

#################
# Special Forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.


def do_define_form(expressions, env):
    """Evaluate a define form.
    >>> env = create_global_frame()
    >>> do_define_form(read_line("(x 2)"), env)
    'x'
    >>> scheme_eval("x", env)
    2
    >>> do_define_form(read_line("(x (+ 2 8))"), env)
    'x'
    >>> scheme_eval("x", env)
    10
    >>> # problem 9
    >>> env = create_global_frame()
    >>> do_define_form(read_line("((f x) (+ x 2))"), env)
    'f'
    >>> scheme_eval(read_line("(f 3)"), env)
    5
    """
    validate_form(
        expressions, 2)  # Checks that expressions is a list of length at least 2
    target = expressions.first
    if scheme_symbolp(target):
        # Checks that expressions is a list of length exactly 2
        validate_form(expressions, 2, 2)
        # BEGIN PROBLEM 5
        val = scheme_eval(expressions.rest.first, env)
        env.define(target, val)
        return target
        # END PROBLEM 5
    elif isinstance(target, Pair) and scheme_symbolp(target.first):
        # BEGIN PROBLEM 9
        name = target.first
        formals = target.rest
        body = expressions.rest
        procedure = do_lambda_form(Pair(formals, body), env)
        env.define(name, procedure)
        return name
        # END PROBLEM 9
    else:
        bad_target = target.first if isinstance(target, Pair) else target
        raise SchemeError('non-symbol: {0}'.format(bad_target))


def do_quote_form(expressions, env):
    """Evaluate a quote form.

    >>> env = create_global_frame()
    >>> do_quote_form(read_line("((+ x 2))"), env)
    Pair('+', Pair('x', Pair(2, nil)))
    """
    validate_form(expressions, 1, 1)
    # BEGIN PROBLEM 6
    return expressions.first
    # END PROBLEM 6


def do_begin_form(expressions, env):
    """Evaluate a begin form.

    >>> env = create_global_frame()
    >>> x = do_begin_form(read_line("((print 2) 3)"), env)
    2
    >>> x
    3
    """
    validate_form(expressions, 1)
    return eval_all(expressions, env)


def do_lambda_form(expressions, env):
    """Evaluate a lambda form.

    >>> env = create_global_frame()
    >>> do_lambda_form(read_line("((x) (+ x 2))"), env)
    LambdaProcedure(Pair('x', nil), Pair(Pair('+', Pair('x', Pair(2, nil))), nil), <Global Frame>)
    """
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 8
    return LambdaProcedure(formals, expressions.rest, env)
    # END PROBLEM 8


def do_if_form(expressions, env):
    """Evaluate an if form.

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env)
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env)
    3
    """
    validate_form(expressions, 2, 3)
    if is_true_primitive(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.rest.first, env, True)
    elif len(expressions) == 3:
        return scheme_eval(expressions.rest.rest.first, env, True)


def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form.

    >>> env = create_global_frame()
    >>> do_and_form(read_line("(#f (print 1))"), env)
    False
    >>> do_and_form(read_line("((print 1) (print 2) (print 3) (print 4) 3 #f)"), env)
    1
    2
    3
    4
    False
    """
    # BEGIN PROBLEM 12
    result = True
    while expressions is not nil:
        tail = (expressions.rest is nil)
        result = scheme_eval(expressions.first, env, tail)
        if is_false_primitive(result):
            return False
        expressions = expressions.rest
    return result
    # END PROBLEM 12


def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form.

    >>> env = create_global_frame()
    >>> do_or_form(read_line("(10 (print 1))"), env)
    10
    >>> do_or_form(read_line("(#f 2 3 #t #f)"), env)
    2
    >>> do_or_form(read_line("((begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))"), env)
    1
    2
    6
    """
    # BEGIN PROBLEM 12
    result = False
    while expressions is not nil:
        tail = (expressions.rest is nil)
        result = scheme_eval(expressions.first, env, tail)
        if is_true_primitive(result):
            return result
        expressions = expressions.rest
    return result
    # END PROBLEM 12


def do_cond_form(expressions, env):
    """Evaluate a cond form.

    >>> do_cond_form(read_line("((#f (print 2)) (#t 3))"), create_global_frame())
    3
    """
    while expressions is not nil:
        clause = expressions.first
        validate_form(clause, 1)
        if clause.first == 'else':
            test = True
            if expressions.rest is not nil:
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env)
        if is_true_primitive(test):
            # BEGIN PROBLEM 13
            if clause.rest is nil:
                return test
            return eval_all(clause.rest, env)
            # END PROBLEM 13
        expressions = expressions.rest


def do_let_form(expressions, env):
    """Evaluate a let form.

    >>> env = create_global_frame()
    >>> do_let_form(read_line("(((x 2) (y 3)) (+ x y))"), env)
    5
    """
    validate_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.rest, let_env)


def make_let_frame(bindings, env):
    """Create a child frame of ENV that contains the definitions given in
    BINDINGS. The Scheme list BINDINGS must have the form of a proper bindings
    list in a let expression: each item must be a list containing a symbol
    and a Scheme expression."""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    names, values = nil, nil
    # BEGIN PROBLEM 14
    while bindings is not nil:
        binding = bindings.first
        validate_form(binding, 2, 2)
        names = Pair(binding.first, names)
        values = Pair(scheme_eval(binding.rest.first, env), values)
        bindings = bindings.rest
    validate_formals(names)
    # END PROBLEM 14
    return env.make_child_frame(names, values)


def do_define_macro(expressions, env):
    """Evaluate a define-macro form.

    >>> env = create_global_frame()
    >>> do_define_macro(read_line("((f x) (car x))"), env)
    'f'
    >>> scheme_eval(read_line("(f (1 2))"), env)
    1
    """
    # BEGIN Problem 20
    # Checks that expressions is a list of length at least 2
    validate_form(expressions, 2)
    target = expressions.first
    if not(isinstance(target, Pair) and scheme_symbolp(target.first)):
        raise SchemeError('Invalid define-macro')
    procedure = MacroProcedure(target.rest, expressions.rest, env)
    env.define(target.first, procedure)
    return target.first
    # END Problem 20


def do_quasiquote_form(expressions, env):
    """Evaluate a quasiquote form with parameters EXPRESSIONS in
    environment ENV."""
    def quasiquote_item(val, env, level):
        """Evaluate Scheme expression VAL that is nested at depth LEVEL in
        a quasiquote form in environment ENV."""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.rest
                validate_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1

        return val.map(lambda elem: quasiquote_item(elem, env, level))

    validate_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)


def do_unquote(expressions, env):
    raise SchemeError('unquote outside of quasiquote')


def do_enumerate_form(expressions, env):
    validate_form(expressions, 1, 1)
    vals = scheme_eval(expressions.first, env)

    def enumerate_rec(num, vals, env):
        if vals is nil:
            return nil
        return Pair(Pair(num, Pair(vals.first, nil)),
                    enumerate_rec(num + 1, vals.rest, env))
    return enumerate_rec(0, vals, env)


def do_merge_form(expressions, env):
    validate_form(expressions, 3, 3)
    op = scheme_eval(expressions.first, env)
    validate_procedure(op)
    lhs = scheme_eval(expressions.rest.first, env)
    rhs = scheme_eval(expressions.rest.rest.first, env)

    def merge_rec(op, lhs, rhs, env):
        if lhs is nil:
            return rhs
        if rhs is nil:
            return lhs
        if scheme_apply(op, Pair(lhs.first, Pair(rhs.first, nil)), env):
            return Pair(lhs.first, merge_rec(op, lhs.rest, rhs, env))
        else:
            return Pair(rhs.first, merge_rec(op, lhs, rhs.rest, env))
    return merge_rec(op, lhs, rhs, env)


def do_nondecreaselist_form(expressions, env):
    validate_form(expressions, 1, 1)
    vals = scheme_eval(expressions.first, env)

    def nondecreaselist_rec(vals, env):
        if vals is nil:
            return Pair(nil, nil)
        nondec_list = nondecreaselist_rec(vals.rest, env)
        if nondec_list.first is nil or nondec_list.first.first >= vals.first:
            return Pair(Pair(vals.first, nondec_list.first), nondec_list.rest)
        return Pair(Pair(vals.first, nil), nondec_list)
    return nondecreaselist_rec(vals, env)


SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'define-macro': do_define_macro,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
    'enumerate': do_enumerate_form,
    'merge': do_merge_form,
    'nondecreaselist': do_nondecreaselist_form
}

# Utility methods for checking the structure of Scheme programs


def validate_form(expr, min, max=float('inf')):
    """Check EXPR is a proper list whose length is at least MIN and no more
    than MAX (default: no maximum). Raises a SchemeError if this is not the
    case.

    >>> validate_form(read_line('(a b)'), 2)
    """
    if not scheme_listp(expr):
        raise SchemeError('badly formed expression: ' + repl_str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError('too few operands in form')
    elif length > max:
        raise SchemeError('too many operands in form')


def validate_formals(formals):
    """Check that FORMALS is a valid parameter list, a Scheme list of symbols
    in which each symbol is distinct. Raise a SchemeError if the list of
    formals is not a list of symbols or if any symbol is repeated.

    >>> validate_formals(read_line('(a b c)'))
    """
    symbols = set()

    def validate_and_add(symbol, is_last):
        if not scheme_symbolp(symbol):
            raise SchemeError('non-symbol: {0}'.format(symbol))
        if symbol in symbols:
            raise SchemeError('duplicate symbol: {0}'.format(symbol))
        symbols.add(symbol)

    while isinstance(formals, Pair):
        validate_and_add(formals.first, formals.rest is nil)
        formals = formals.rest


def validate_procedure(procedure):
    """Check that PROCEDURE is a valid Scheme procedure."""
    if not scheme_procedurep(procedure):
        raise SchemeError('{0} is not callable: {1}'.format(
            type(procedure).__name__.lower(), repl_str(procedure)))

#################
# Dynamic Scope #
#################


class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition."""
        self.formals = formals
        self.body = body

    # BEGIN PROBLEM 18
    def make_call_frame(self, args, env):
        """Make a frame that binds my formal parameters to ARGS, a Scheme list
        of values, for a dynamically-scoped call evaluated in environment ENV."""
        return Frame.make_child_frame(env, self.formals, args)
    # END PROBLEM 18

    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))


def do_mu_form(expressions, env):
    """Evaluate a mu form."""
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 18
    return MuProcedure(formals, expressions.rest)
    # END PROBLEM 18


SPECIAL_FORMS['mu'] = do_mu_form

###########
# Streams #
###########


class Promise(object):
    """A promise."""

    def __init__(self, expression, env):
        self.expression = expression
        self.env = env

    def evaluate(self):
        if self.expression is not None:
            value = scheme_eval(self.expression, self.env)
            if not (value is nil or isinstance(value, Pair)):
                raise SchemeError(
                    "result of forcing a promise should be a pair or nil, but was %s" % value)
            self.value = value
            self.expression = None
        return self.value

    def __str__(self):
        return '#[promise ({0}forced)]'.format(
            'not ' if self.expression is not None else '')


def do_delay_form(expressions, env):
    """Evaluates a delay form."""
    validate_form(expressions, 1, 1)
    return Promise(expressions.first, env)


def do_cons_stream_form(expressions, env):
    """Evaluate a cons-stream form."""
    validate_form(expressions, 2, 2)
    return Pair(scheme_eval(expressions.first, env),
                do_delay_form(expressions.rest, env))


SPECIAL_FORMS['cons-stream'] = do_cons_stream_form
SPECIAL_FORMS['delay'] = do_delay_form

##################
# Tail Recursion #
##################


class Thunk(object):
    """An expression EXPR to be evaluated in environment ENV."""

    def __init__(self, expr, env):
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not a Thunk."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Thunk):
        return scheme_eval(val.expr, val.env)
    else:
        return val


def optimize_tail_calls(original_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in environment ENV. If TAIL,
        return a Thunk containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Thunk(expr, env)

        result = Thunk(expr, env)
        # BEGIN
        while isinstance(result, Thunk):
            result = original_scheme_eval(result.expr, result.env)
        return result
        # END
    return optimized_eval


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
scheme_eval = optimize_tail_calls(scheme_eval)


####################
# Extra Procedures #
####################

def scheme_map(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'map')
    validate_type(s, scheme_listp, 1, 'map')
    return s.map(lambda x: complete_apply(fn, Pair(x, nil), env))


def scheme_filter(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'filter')
    validate_type(s, scheme_listp, 1, 'filter')
    head, current = nil, nil
    while s is not nil:
        item, s = s.first, s.rest
        if complete_apply(fn, Pair(item, nil), env):
            if head is nil:
                head = Pair(item, nil)
                current = head
            else:
                current.rest = Pair(item, nil)
                current = current.rest
    return head


def scheme_reduce(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'reduce')
    validate_type(s, lambda x: x is not nil, 1, 'reduce')
    validate_type(s, scheme_listp, 1, 'reduce')
    value, s = s.first, s.rest
    while s is not nil:
        value = complete_apply(fn, scheme_list(value, s.first), env)
        s = s.rest
    return value

################
# Input/Output #
################


def read_eval_print_loop(next_line, env, interactive=False, quiet=False,
                         startup=False, load_files=(), report_errors=False):
    """Read and evaluate input until an end of file or keyboard interrupt."""
    if startup:
        for filename in load_files:
            scheme_load(filename, True, env)
    while True:
        try:
            src = next_line()
            while src.more_on_line:
                expression = scheme_read(src)
                result = scheme_eval(expression, env)
                if not quiet and result is not None:
                    print(repl_str(result))
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as err:
            if report_errors:
                if isinstance(err, SyntaxError):
                    err = SchemeError(err)
                    raise err
            if (isinstance(err, RuntimeError) and
                    'maximum recursion depth exceeded' not in getattr(err, 'args')[0]):
                raise
            elif isinstance(err, RuntimeError):
                print('Error: maximum recursion depth exceeded')
            else:
                print('Error:', err)
        except KeyboardInterrupt:  # <Control>-C
            if not startup:
                raise
            print()
            print('KeyboardInterrupt')
            if not interactive:
                return
        except EOFError:  # <Control>-D, etc.
            print()
            return


def scheme_load(*args):
    """Load a Scheme source file. ARGS should be of the form (SYM, ENV) or
    (SYM, QUIET, ENV). The file named SYM is loaded into environment ENV,
    with verbosity determined by QUIET (default true)."""
    if not (2 <= len(args) <= 3):
        expressions = args[:-1]
        raise SchemeError('"load" given incorrect number of arguments: '
                          '{0}'.format(len(expressions)))
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if (scheme_stringp(sym)):
        sym = eval(sym)
    validate_type(sym, scheme_symbolp, 0, 'load')
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)

    def next_line():
        return buffer_lines(*args)

    read_eval_print_loop(next_line, env, quiet=quiet, report_errors=True)


def scheme_load_all(directory, env):
    """
    Loads all .scm files in the given directory, alphabetically. Used only
        in tests/ code.
    """
    assert scheme_stringp(directory)
    directory = eval(directory)
    import os
    for x in sorted(os.listdir(".")):
        if not x.endswith(".scm"):
            continue
        scheme_load(x, env)


def scheme_open(filename):
    """If either FILENAME or FILENAME.scm is the name of a valid file,
    return a Python file opened to it. Otherwise, raise an error."""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))


def create_global_frame():
    """Initialize and return a single-frame environment with built-in names."""
    env = Frame(None)
    env.define('eval',
               BuiltinProcedure(scheme_eval, True, 'eval'))
    env.define('apply',
               BuiltinProcedure(complete_apply, True, 'apply'))
    env.define('load',
               BuiltinProcedure(scheme_load, True, 'load'))
    env.define('load-all',
               BuiltinProcedure(scheme_load_all, True, 'load-all'))
    env.define('procedure?',
               BuiltinProcedure(scheme_procedurep, False, 'procedure?'))
    env.define('map',
               BuiltinProcedure(scheme_map, True, 'map'))
    env.define('filter',
               BuiltinProcedure(scheme_filter, True, 'filter'))
    env.define('reduce',
               BuiltinProcedure(scheme_reduce, True, 'reduce'))
    env.define('undefined', None)
    add_builtins(env, BUILTINS)
    return env


@main
def run(*argv):
    import argparse
    parser = argparse.ArgumentParser(description='CS 61A Scheme Interpreter')
    parser.add_argument('--pillow-turtle', action='store_true',
                        help='run with pillow-based turtle. This is much faster for rendering but there is no GUI')
    parser.add_argument('--turtle-save-path', default=None,
                        help='save the image to this location when done')
    parser.add_argument('-load', '-i', action='store_true',
                        help='run file interactively')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help='Scheme file to run')
    args = parser.parse_args()

    import builtins
    builtins.TK_TURTLE = not args.pillow_turtle
    builtins.TURTLE_SAVE_PATH = args.turtle_save_path
    sys.path.insert(0, '')

    next_line = buffer_input
    interactive = True
    load_files = []

    if args.file is not None:
        if args.load:
            load_files.append(getattr(args.file, 'name'))
        else:
            lines = args.file.readlines()

            def next_line():
                return buffer_lines(lines)
            interactive = False

    read_eval_print_loop(next_line, create_global_frame(), startup=True,
                         interactive=interactive, load_files=load_files)
    tscheme_exitonclick()
