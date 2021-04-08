## Overview and Terminology
### Expressions and Environments

Scheme works by evaluating **expressions** in **environments**. Every expression
evaluates to a **value**. Some expressions are **self-evaluating**, which means
they are both an expression and a value, and that it evaluates to itself.

A **frame** is a mapping from symbols (names) to values, as well as an optional
parent frame. The current environment refers to the current frame, as well as a
chain of parent frames up to the **global frame** (which has no parent). When
looking up a symbol in an environment, Scheme first checks the current frame and
returns the corresponding value if it exists. If it doesn't, it repeats this
process on each subsequent parent frame, until either the symbol is found, or
there are no more parent frames to check.

### Atomic Expressions

There are several **atomic** or **primitive** expressions. Numbers, booleans,
strings, and the empty list (`nil`) are all both atomic and self-evaluating.
Symbols are atomic, but are not self-evaluating (they instead evaluate to a
value that was previously bound to it in the environment).

### Call Expressions

The Scheme expressions that are not atomic are called **combinations**, and
consist of one or more **subexpressions** between parentheses. Most forms are
evaluated as **call expressions**, which has three evaluation steps:

1. Evaluate the first subexpression (the operator), which must evaluate to a
**procedure** (see below).
2. Evaluate the remaining subexpressions (the operands) in order.
3. Apply the procedure from step 1 to the evaluated operands (**arguments**) from
step 2.

These steps mirror those in Python and other languages.

### Special Forms

However, not all combinations are call expressions. Some are **special forms**.
The interpreter maintains a set of particular symbols (sometimes called
**keywords**) that signal that a combination is a special form when they are the
first subexpression. Each special form has it's own procedure for which operands
to evaluate and how (described below). The interpreter always checks the first
subexpression of a combination first. If it matches one of the keywords, the
corresponding special form is used. Otherwise, the combination is evaluated as a
call expression.

### Symbolic Programming

Scheme's core data type is the **list**, built out of pairs as described below.
Scheme code is actually built out of these lists. This means that the code
`(+ 1 2)` is constructed as a list of the `+` symbol, the number 1, and the
number 2, which is then evaluated as a call expression.

Since lists are normally evaluated as combinations, we need a special form to
get the actual, unevaluated list. `quote` is a special form that takes a single
operand expression and returns it, unevaluated. Therefore, `(quote (+ 1 2))`
returns the actual list of the symbol `+`, the number 1, and the number 2,
rather than evaluating the expression to get the number 3. This also works for
symbols. `a` is looked up in the current environment to get the corresponding
value, while `(quote a)` evaluates to the literal symbol `a`.

Because `quote` is so commonly used in Scheme, the language has a shorthand way
of writing it: just put a single quote in front of the expression you want to
leave unevaluated. `'(+ 1 2)` and `'a` are equivalent to `(quote (+ 1 2))` and
`(quote a)`, respectively.

### Miscellaneous

Like R5RS, 61A Scheme is entirely case-insensitive (aside from strings). This
specification will use lowercase characters in symbols, but the corresponding
uppercase characters may be used interchangeably.

## Types of Values

### Numbers

Numbers are built on top of Python's number types and can thus support a
combination of arbitrarily-large integers and double-precision floating points.

The web interpreter attempts to replicate this when possible, though may deviate
from Python-based versions due to the different host language and the need to
work-around the quirks of JavaScript when running in a browser.

Any valid real number literal in the interpreter's host language should be
properly read. You should not count on consistent results when floating point
numbers are involved in any calculation or on any numbers with true division.

### Booleans

There are two boolean values: `#t` and `#f`. Scheme booleans may be input either
as their canonical `#t` or `#f` or as the words `true` or `false`.

Any expression may be evaluated in a boolean context, but `#f` is the only value
that is false. All other values are treated as true in a boolean context.

Some interpreters prior to Spring 2018 displayed the words `true` and `false`
when booleans were output, but this should not longer be the case in any
interpreter released/updated since then.

### Symbols

Symbols are used as identifiers in Scheme. Valid symbols consist of some
combination of alphanumeric characters and/or the following special characters:

    !$%&*/:<=>?@^_~+-.

All symbols should be internally stored with lowercase letters. Symbols must not
form a valid integer or floating-point number.

### Strings

Unlike other implementations, 61A Scheme has no concept of individual
characters. Strings are considered atomic data types in their own right. Strings
can be entered into the intepreter as a sequence of characters inside double
quotes, with certain characters, such as line breaks and double quotes escaped.
As a general rule, if a piece of text would be valid as a JSON key, it should
work as a string in 61A Scheme. Strings in 61A Scheme are immutable, in contrast
to most other Scheme implementations.

These differences in how strings behave are due to the status of strings in the
host languages: Python and Dart both have immutable strings with no concept of
individual characters.

Because the Python-based interpreter has little use for strings, it lacks proper
support for their manipulation. The web interpreter, which requires strings for
JS interop (among other things), it supports a `string-append` built-in, which
takes in an arbitrary number of values or any type and combines them into a
string. Additional string manipulation can be done through JS interop.

### Pairs and Lists

Pairs are a built-in data structure consisting of two fields, a `car` and a
`cdr` (also sometimes called first and second, or first and rest). The first
value can contain any scheme datatype. However, the second value must contain
nil, a pair, or a stream promise.

`nil` is a special value in Scheme which represents the empty list. It can be
inputted by typing `nil` or `()` into the interpreter.

A **list** is defined as either `nil` or a pair whose `cdr` is another list.
Pairs are displayed as a parenthesized, space separated, sequence of the elements
in the sequence they represent. For example, `(cons (cons 1 nil) (cons 1 nil))`
is displayed as `((1) 2)`. Note that this means that `cons` is asymmetric.

> There is one exception to the above rule in the case of streams. Streams are
> represented as the `car` of the stream, followed by a dot, followed by the
> promise that makes up its cdr. For example
    scm> (cons-stream 1 nil)
    (1 . #[promise (not forced)])

List literals can be constructed through the quote special form, so
`(cons 1 (cons 'a nil))` and `'(1 a)` are equivalent.

### Procedures

Procedures represent some subroutine within a Scheme program. Procedures are
first-class in Scheme, meaning that they can be bound to names and passed
around just like any other Scheme value. Procedures are equivalent to functions
in most other languages, and the two terms are sometimes used interchangeably.

Procedures can be called on some number of arguments, performing some number
of actions and then returning some Scheme value.

A procedure call can be performed with the syntax `(<operator> <operand> ...)`,
where `<operator>` is some expression that evaluates to a procedure and each
`<operand>` (of which there can be any number, including 0) evaluates to one of
the procedure's arguments. The term "procedure call" is used interchangeably
with the term "call expression."

There are several types of procedures. Built-in procedures (or just built-ins)
are built-in to the interpreter and already bound to names when it is started
(though it is still possible for you to rebind these names). A list of all the
built-in procedures in the Python-based interpreter is available in the
[Scheme built-ins][] document.

Lambda procedures are defined using the `lambda` or `define` special forms (see
below) and create a new frame whose parent is the frame in which the lambda was
defined in when called. The expressions in the lambda's body are than evaluated
in this new environment. Mu procedures are similar, but the new frame's parent
is the frame in which the `mu` is called, not the frame in which it was created.

61A Scheme also has macro procedures, which must be defined with the
`define-macro` special form. Macros work similarly to lambdas, except that they
pass the argument expressions in the call expression into the macro instead of
the evaluated arguments and they then evaluate the expression the macro returns
in the calling environment afterwards. The modified process for evaluating
macro call expressions is:

1. Evaluate the operator. If it is not a macro procedure, follow the normal call
expression steps.
2. Apply the macro procedure from step 1 to the unevaluated operands.
3. Once the macro returns, evaluate that value in the calling environment.

Macros effectively let the user define new special forms. Macro procedures take
in unevaluated operand expressions and should generally return a piece of Scheme
code that the macro is equivalent to.

### Promises and Streams

Promises represent the delayed evaluation of an expression in an environment.
They can be constructed by passing an expression into the `delay` special form.
The evaluation of a promise can be forced by passing it into the `force`
built-in. The expression of a promise will only ever be evaluated once. The
first call of `force` will store the result, which will be immediately returned
on subsequent calls of `force` on the same promise.

A promise must contain a pair or nil since it is used as the `cdr` of a stream. If
it is found to contain something else when forced, `force` will error. If `force`
errors for any reason, the promise remains unforced.

For example

    scm> (define p (delay (begin (print "hi") (/ 1 0))))
    p
    scm> p
    #[promise (unforced)]
    scm> (force p)
    hi
    Error
    scm> p
    #[promise (unforced)]
    scm> (force p)
    hi
    Error

Or, for an example with type errors:

    scm> (define p (delay (begin (print "hi") 2)))
    p
    scm> p
    #[promise (unforced)]
    scm> (force p)
    hi
    Error
    scm> p
    #[promise (unforced)]
    scm> (force p)
    hi
    Error

Promises are used to define **streams**, which are to lists what promises are to
regular values. A stream is defined as a pair where the cdr is a promise that
evaluates to another stream or `nil`. The `cons-stream` special form and the
`cdr-stream` built-in are provided make the construction and manipulation of
streams easier. `(cons-stream a b)` is equivalent to `(cons a (delay b))`
while `(cdr-stream x)` is equivalent to `(force (cdr x))`.

> A note for those familiar with promises in languages like JavaScript: although
Scheme promises and JS-style promises originate from the
[same general concept][promise wiki], JS promises are best described as a
placeholder for a value that is computed asynchronously. The Python-based 61A
Scheme interpreter has no concept of asynchrony, so its promises only represent
delayed evaluation. The web interpreter continues to use promises in this way,
but adds a "future" type to stand in place for JS promises.

  [promise wiki]: https://en.wikipedia.org/wiki/Futures_and_promises

## Special Forms

In all of the syntax definitions below, `<x>` refers to a required element `x`
that can vary, while `[x]` refers to an optional element `x`. Ellipses
indicate that there can be more than one of the preceding element.

The following special forms are included in all versions of 61A Scheme.

### **`define`**

    (define <name> <expression>)

Evaluates `<expression>` and binds the value to `<name>` in the current
environment. `<name>` must be a valid Scheme symbol.

    (define (<name> [param] ...) <body> ...)

Constructs a new lambda procedure with `param`s as its parameters and the `body`
expressions as its body and binds it to `name` in the current environment.
`name` must be a valid Scheme symbol. Each `param` must be a unique valid Scheme
symbol. This shortcut is equivalent to:

    (define <name> (lambda ([param] ...) <body> ...))

However, some interpreters may give lambdas created using the shortcut an
intrinsic name of `name` for the purpose of visualization or debugging.

In either case, the return value is the symbol `<name>`.

    scm> (define x 2)
    x
    scm> (define (f x) x)
    f

#### Variadic functions

In staff implementations of the scheme language, you can define a function that takes a variable number of arguments by using the `variadic` special form. The construct `variadic` constructs a "variadic symbol" that is bound to multiple rather than a single variable. This is only allowed at the end of an arguments list

    scm> (define (f x (variadic y)) (append y (list x)))
    f
    scm> (f 1 2 3)
    (2 3 1)
    scm> (define (f (variadic y) x) (append y (list x)))
    Error

This is also possible in lambdas:

    scm> (define f (lambda (x (variadic y)) (append y (list x))))
    f
    scm> (f 1 2 3)
    (2 3 1)
    scm> (define my-list (lambda ((variadic x)) x))
    my-list
    scm> (my-list 2 3 4)
    (2 3 4)

You can use the special symbol `.` to construct the `variadic` special form:

    scm> (define (f x . y) (append y (list x)))
    f
    scm> (f 1 2 3)
    (2 3 1)
    scm> '. x
    (variadic x)

This is analogous to `,` for `unquote`.

> Note: this is pretty much the same as `*args` in python, except that you can't call a function using `variadic`, you instead have to use the `#[apply]` built-in function.

### **`if`**

    (if <predicate> <consequent> [alternative])

Evaluates `predicate`. If true, the `consequent` is evaluated and returned.
Otherwise, the `alternative`, if it exists, is evaluated and returned (if no
`alternative` is present in this case, the return value is undefined).

### **`cond`**

    (cond <clause> ...)

Each `clause` may be of the following form:

    (<test> [expression] ...)

The last `clause` may instead be of the form `(else [expression] ...)`, which
is equivalent to `(#t [expression] ...)`.

Starts with the first `clause`. Evaluates `test`. If true, evaluate the
`expression`s in order, returning the last one. If there are none, return what
`test` evaluated to instead. If `test` is false, proceed to the next `clause`.
If there are no more `clause`s, the return value is undefined.

### **`and`**

    (and [test] ...)

Evaluate the `test`s in order, returning the first false value. If no `test`
is false, return the last `test`. If no arguments are provided, return `#t`.

### **`or`**

    (or [test] ...)

Evaluate the `test`s in order, returning the first true value. If no `test`
is true and there are no more `test`s left, return `#f`.

### **`let`**

    (let ([binding] ...) <body> ...)

Each `binding` is of the following form:

    (<name> <expression>)

First, the `expression` of each `binding` is evaluated in the current frame.
Next, a new frame that extends the current environment is created and each
`name` is bound to its corresponding evaluated `expression` in it.

Finally the `body` expressions are evaluated in order, returning the evaluated
last one.

### **`begin`**

    (begin <expression> ...)

Evaluates each `expression` in order in the current environment, returning the
evaluated last one.

### **`lambda`**

    (lambda ([param] ...) <body> ...)

Creates a new lambda with `param`s as its parameters and the `body` expressions
as its body. When the procedure this form creates is called, the call frame
will extend the environment this lambda was defined in.

### **`mu`**

    (mu ([param] ...) <body> ...)

Creates a new mu procedure with `param`s as its parameters and the `body`
expressions as its body. When the procedure this form creates is called, the
call frame will extend the environment the mu is called in.

### **`quote`**

    (quote <expression>)

Returns the literal `expression` without evaluating it.

`'<expression>` is equivalent to the above form.

### **`delay`**

    (delay <expression>)

Returns a promise of `expression` to be evaluated in the current environment.

### **`cons-stream`**

    (cons-stream <first> <rest>)

Shorthand for `(cons <first> (delay <rest>))`.

### **`set!`**

    (set! <name> <expression>)

Evaluates `expression` and binds the result to `name` in the first frame it can
be found in from the current environment. If `name` is not bound in the current
environment, this causes an error.

The return value is undefined.

### **`quasiquote`**

    (quasiquote <expression>)

Returns the literal `expression` without evaluating it, unless a subexpression
of `expression` is of the form:

    (unquote <expr2>)

in which case that `expr2` is evaluated and replaces the above form in the
otherwise unevaluated `expression`.

```<expression>`` is equivalent to the above form.

### **`unquote`**

See above. `,<expr2>` is equivalent to the form mentioned above.

### **`unquote-splicing`**

    (unquote-splicing <expr2>)

> Note: This special form is included in the staff interpreter and the web
> interpreter, but it is not in scope for the course and is not included in the
> project.

Similar to `unquote`, except that `expr2` must evaluate to a list, which is
then spliced into the structure containing it in `expression`.

`,@<expr2>` is equivalent to the above form.

### **`define-macro`**

    (define-macro (<name> [param] ...) <body> ...)

> Note: This special form is implemented as part of an extra credit problem.

Constructs a new macro procedure with `param`s as its parameters and the `body`
expressions as its body and binds it to `name` in the current environment.
`name` must be a valid Scheme symbol. Each `param` must be a unique valid Scheme
symbol. `(<name> [param] ...)` can be [variadic](#variadic-functions).

Macro procedures should be lexically scoped, like lambda procedures.

## Core Interpreter

<a class='builtin-header' id='apply'>**`apply`**</a>

    (apply <procedure> <args>)

Calls `procedure` with the given list of `args`.

    scm> (apply + '(1 2 3))
    6

<a class='builtin-header' id='display'>**`display`**</a>

    (display <val>)

Prints `val`. If `val` is a Scheme string, it will be output without quotes.

A new line will not be automatically included.

<a class='builtin-header' id='error'>**`error`**</a>

    (error <msg>)

Raises an `SchemeError` with `msg` as it's message. If there is no `msg`,
the error's message will be empty.

<a class='builtin-header' id='eval'>**`eval`**</a>

    (eval <expression>)

Evaluates `expression` in the current environment.

    scm> (eval '(cons 1 (cons 2 nil)))
    (1 2)

<a class='builtin-header' id='exit'>**`exit`**</a>

    (exit)

Exits the interpreter. In the web interpreter, this does nothing.

<a class='builtin-header' id='load'>**`load`**</a>

    (load <filename>)

Loads the contents of the file with `filename` and evaluates the code within.
`filename` must be a symbol. If that file is not found, `filename`.scm will
be attempted.

The web interpreter's does not currently support `load`. The closest analog is
`import-inline`, which takes a URL and evaluates the Scheme code in the current
environment.

<a class='builtin-header' id='newline'>**`newline`**</a>

    (newline)

Prints a new line.

<a class='builtin-header' id='print'>**`print`**</a>

    (print <val>)

Prints the Scheme representation of `val`. Unlike `display`, this will include
the outer quotes on a Scheme string and will print a new line.

## Type Checking

<a class='builtin-header' id='atom?'>**`atom?`**</a>

    (atom? <arg>)

Returns true if `arg` is a boolean, number, symbol, string, or nil;
false otherwise.

<a class='builtin-header' id='boolean?'>**`boolean?`**</a>

    (boolean? <arg>)

Returns true if `arg` is a boolean; false otherwise.

<a class='builtin-header' id='integer?'>**`integer?`**</a>

    (integer? <arg>)

Returns true if `arg` is a integer; false otherwise.

<a class='builtin-header' id='list?'>**`list?`**</a>

    (list? <arg>)

Returns true if `arg` is a well-formed list (i.e., it doesn't contain
a stream); false otherwise. If the list has a cycle, this may cause an
error or infinite loop.

    scm> (list? '(1 2 3))
    True
    scm> (list? (cons-stream 1 nil))
    False

<a class='builtin-header' id='number?'>**`number?`**</a>

    (number? <arg>)

Returns true if `arg` is a number; false otherwise.

<a class='builtin-header' id='null?'>**`null?`**</a>

    (null? <arg>)

Returns true if `arg` is `nil` (the empty list); false otherwise.

<a class='builtin-header' id='pair?'>**`pair?`**</a>

    (pair? <arg>)

Returns true if `arg` is a pair; false otherwise.

<a class='builtin-header' id='procedure?'>**`procedure?`**</a>

    (procedure? <arg>)

Returns true if `arg` is a procedure; false otherwise.

<a class='builtin-header' id='promise?'>**`promise?`**</a>

    (promise? <arg>)

Returns true if `arg` is a promise; false otherwise.

<a class='builtin-header' id='string?'>**`string?`**</a>

    (string? <arg>)

Returns true if `arg` is a string; false otherwise.

<a class='builtin-header' id='symbol?'>**`symbol?`**</a>

    (symbol? <arg>)

Returns true if `arg` is a symbol; false otherwise.

## Pair and List Manipulation

<a class='builtin-header' id='append'>**`append`**</a>

    (append [lst] ...)

Returns the result of appending the items of all `lst`s in order into a single
list. Returns `nil` if no `lst`s.

    scm> (append '(1 2 3) '(4 5 6))
    (1 2 3 4 5 6)
    scm> (append)
    ()
    scm> (append '(1 2 3) '(a b c) '(foo bar baz))
    (1 2 3 a b c foo bar baz)
    scm> (append '(1 2 3) 4)
    Error

<a class='builtin-header' id='car'>**`car`**</a>

    (car <pair>)

Returns the `car` of `pair`. Errors if `pair` is not a pair.

<a class='builtin-header' id='cdr'>**`cdr`**</a>

    (cdr <pair>)

Returns the `cdr` of `pair`. Errors if `pair` is not a pair.

<a class='builtin-header' id='cons'>**`cons`**</a>

    (cons <first> <rest>)

Returns a new pair with `first` as the `car` and `rest` as the `cdr`

<a class='builtin-header' id='length'>**`length`**</a>

    (length <arg>)

Returns the length of `arg`. If `arg` is not a list, this
will cause an error.

<a class='builtin-header' id='list'>**`list`**</a>

    (list <item> ...)

Returns a list with the `item`s in order as its elements.

<a class='builtin-header' id='map'>**`map`**</a>

    (map <proc> <lst>)

Returns a list constructed by calling `proc` (a one-argument
procedure) on each item in `lst`.

<a class='builtin-header' id='filter'>**`filter`**</a>

    (filter <pred> <lst>)

Returns a list consisting of only the elements of `lst` that
return true when called on `pred` (a one-argument
procedure).

<a class='builtin-header' id='reduce'>**`reduce`**</a>

    (reduce <combiner> <lst>)

Returns the result of sequentially combining each element in `lst`
using `combiner` (a two-argument procedure). `reduce` works
from left-to-right, with the existing combined value passed as the first
argument and the new value as the second argument. `lst` must contain at least
one item.

### Mutation

<a class='builtin-header' id='set-car!'>**`set-car!`**</a>

    (set-car! <pair> <value>)

Sets the `car` of `pair` to `value`. `pair` must be a pair.

<a class='builtin-header' id='set-cdr!'>**`set-cdr!`**</a>

    (set-cdr! <pair> <value>)

Sets the `cdr` of `pair` to `value`. `pair` must be a pair.

## Arithmetic Operations

<a class='builtin-header' id='+'>**`+`**</a>

    (+ [num] ...)

Returns the sum of all `num`s. Returns 0 if there are none. If any `num` is not
a number, this will error.

<a class='builtin-header' id='-'>**`-`**</a>

    (- <num> ...)

If there is only one `num`, return its negation. Otherwise, return the first
`num` minus the sum of the remaining `num`s. If any `num` is not a number, this
will error.

<a class='builtin-header' id='*'>**`*`**</a>

    (* [num] ...)

Returns the product of all `num`s. Returns 1 if there are none. If any `num` is
not a number, this will error.

<a class='builtin-header' id='/'>**`/`**</a>

    (/ <dividend> [divisor] ...)

If there are no `divisor`s, return 1 divided by `dividend`. Otherwise, return
`dividend` divided by the product of the `divisors`. This built-in does true
division, not floor division. `dividend` and all `divisor`s must be numbers.

    scm> (/ 4)
    0.25
    scm> (/ 7 2)
    3.5
    scm> (/ 16 2 2 2)
    2

<a class='builtin-header' id='abs'>**`abs`**</a>

    (abs <num>)

Returns the absolute value of `num`, which must be a number.

<a class='builtin-header' id='expt'>**`expt`**</a>

    (expt <base> <power>)

Returns the `base` raised to the `power` power. Both must be numbers.

<a class='builtin-header' id='modulo'>**`modulo`**</a>

    (modulo <a> <b>)

Returns `a` modulo `b`. Both must be numbers.

    scm> (modulo 7 3)
    1
    scm> (modulo -7 3)
    2

<a class='builtin-header' id='quotient'>**`quotient`**</a>

    (quotient <dividend> <divisor>)

Returns `dividend` integer divided by `divisor`. Both must be numbers.

    scm> (quotient 7 3)
    2

<a class='builtin-header' id='remainder'>**`remainder`**</a>

    (remainder <dividend> <divisor>)

Returns the remainder that results when `dividend` is integer divided by
`divisor`. Both must be numbers. Differs from `modulo` in behavior when
negative numbers are involved.

    scm> (remainder 7 3)
    1
    scm> (remainder -7 3)
    -1

### Additional Math Procedures

The Python-based interpreter adds the following additional procedures whose
behavior exactly match the corresponding Python functions in the
[math module](https://docs.python.org/3/library/math.html).

- acos
- acosh
- asin
- asinh
- atan
- atan2
- atanh
- ceil
- copysign
- cos
- cosh
- degrees
- floor
- log
- log10
- log1p
- log2
- radians
- sin
- sinh
- sqrt
- tan
- tanh
- trunc

## Boolean Operations

### General

<a class='builtin-header' id='eq?'>**`eq?`**</a>

    (eq? <a> <b>)

If `a` and `b` are both numbers, booleans, symbols, or strings, return true if
they are equivalent; false otherwise.

Otherwise, return true if `a` and `b` both refer to the same object in memory;
false otherwise.

    scm> (eq? '(1 2 3) '(1 2 3))
    False
    scm> (define x '(1 2 3))
    scm> (eq? x x)
    True

<a class='builtin-header' id='equal?'>**`equal?`**</a>

    (equal? <a> <b>)

Returns true if `a` and `b` are equivalent. For two pairs, they are equivalent
if their `car`s are equivalent and their `cdr`s are equivalent.

    scm> (equal? '(1 2 3) '(1 2 3))
    True

<a class='builtin-header' id='not'>**`not`**</a>

    (not <arg>)

Returns true if `arg` is false-y or false if `arg` is truthy.

### On Numbers

<a class='builtin-header' id='='>**`=`**</a>

    (= <a> <b>)

Returns true if `a` equals `b`. Both must be numbers.

<a class='builtin-header' id='<'>**`<`**</a>

    (< <a> <b>)

Returns true if `a` is less than `b`. Both must be numbers.

<a class='builtin-header' id='>'>**`>`**</a>

    (> <a> <b>)

Returns true if `a` is greater than `b`. Both must be numbers.

<a class='builtin-header' id='<='>**`<=`**</a>

    (<= <a> <b>)

Returns true if `a` is less than or equal to `b`. Both must be numbers.

<a class='builtin-header' id='>='>**`>=`**</a>

    (>= <a> <b>)

Returns true if `a` is greater than or equal to `b`. Both must be numbers.

<a class='builtin-header' id='even?'>**`even?`**</a>

    (even? <num>)

Returns true if `num` is even. `num` must be a number.

<a class='builtin-header' id='odd?'>**`odd?`**</a>

    (odd? <num>)

Returns true if `num` is odd. `num` must be a number.

<a class='builtin-header' id='zero?'>**`zero?`**</a>

    (zero? <num>)

Returns true if `num` is zero. `num` must be a number.

## Promises and Streams

<a class='builtin-header' id='force'>**`force`**</a>

    (force <promise>)

Returns the evaluated result of `promise`. If `promise` has already been
forced, its expression will not be evaluated again. Instead, the result from
the previous evaluation will be returned. `promise` must be a promise.

<a class='builtin-header' id='cdr-stream'>**`cdr-stream`**</a>

    (cdr-stream <stream>)

Shorthand for `(force (cdr <stream>))`.

## Turtle Graphics

<a class='builtin-header' id='backward'>**`backward`**</a>

    (backward <n>)

Moves the turtle backward `n` units in its current direction from its current
position.

*Aliases: `back`, `bk`*

<a class='builtin-header' id='begin_fill'>**`begin_fill`**</a>

    (begin_fill)

Starts a sequence of moves that outline a shape to be filled.
Call `end_fill` to complete the fill.

<a class='builtin-header' id='bgcolor'>**`bgcolor`**</a>

    (bgcolor <c>)

Sets the background color of the turtle window to a color `c` (same rules as
when calling `color`).

<a class='builtin-header' id='circle'>**`circle`**</a>

    (circle <r> [extent])

Draws a circle of radius `r`, centered `r` units to the turtle's left.
If `extent` exists, draw only the first `extent` degrees of the circle.
If `r` is positive, draw in the counterclockwise direction. Otherwise, draw
in the clockwise direction.

The web interpreter has trouble accurately drawing partial circles.

<a class='builtin-header' id='clear'>**`clear`**</a>

    (clear)

Clears the drawing, leaving the turtle unchanged.

<a class='builtin-header' id='color'>**`color`**</a>

    (color <c>)

Sets the pen color to `c`, which is a Scheme string such as "red" or "#ffc0c0".

The web interpreter also allows `c` to be a symbol. Available named colors may
vary depending on the interpreter.

<a class='builtin-header' id='end_fill'>**`end_fill`**</a>

    (end_fill)

Fill in shape drawn since last call to `begin_fill`.

<a class='builtin-header' id='exitonclick'>**`exitonclick`**</a>

    (exitonclick)

Sets the turtle window to close when it is clicked. This has no effect on the
web interpreter. Call `(exit_turtle)` or `(exitturtle)` to close the turtle
canvas on the web.

<a class='builtin-header' id='forward'>**`forward`**</a>

    (forward <n>)

Moves the turtle forward `n` units in its current direction from its current
position.

*Alias: `fd`*

<a class='builtin-header' id='hideturtle'>**`hideturtle`**</a>

    (hideturtle)

Makes the turtle invisible.

This procedure has no effect on the web interpreter, as the turtle is always
invisible.

*Alias: `ht`*

<a class='builtin-header' id='left'>**`left`**</a>

    (left <n>)

Rotates the turtle's heading `n` degrees counterclockwise.

*Alias: `lt`*

<a class='builtin-header' id='pendown'>**`pendown`**</a>

    (pendown)

Lowers the pen so that the turtle starts drawing.

*Alias: `pd`*

<a class='builtin-header' id='penup'>**`penup`**</a>

    (penup)

Raises the pen so that the turtle does not draw.

*Alias: `pu`*

<a class='builtin-header' id='pixel'>**`pixel`**</a>

    (pixel <x> <y> <c>)

Draws a box filled with pixels starting at (`x`, `y`) in color `c` (same rules
as in `color`). By default the box is one pixel, though this can be changed
with `pixelsize`.

<a class='builtin-header' id='pixelsize'>**`pixelsize`**</a>

    (pixelsize <size>)

Changes the size of the box drawn by `pixel` to be `size`x`size`.

<a class='builtin-header' id='rgb'>**`rgb`**</a>

    (rgb <r> <g> <b>)

Returns a color string formed from `r`, `g`, and `b` values between 0 and 1.

<a class='builtin-header' id='right'>**`right`**</a>

    (right <n>)

Rotates the turtle's heading `n` degrees clockwise.

*Alias: `rt`*

<a class='builtin-header' id='screen_width'>**`screen_width`**</a>

    (screen_width)

Returns the width of the turtle screen in pixels of the current size.

<a class='builtin-header' id='screen_height'>**`screen_height`**</a>

    (screen_height)

Returns the height of the turtle screen in pixels of the current size.

<a class='builtin-header' id='setheading'>**`setheading`**</a>

    (setheading <h>)

Sets the turtle's heading `h` degrees clockwise from the north.

*Alias: `seth`*

<a class='builtin-header' id='setposition'>**`setposition`**</a>

    (setposition <x> <y>)

Moves the turtle to position (`x`, `y`) without changing its heading.

*Aliases: `setpos`, `goto`*

<a class='builtin-header' id='showturtle'>**`showturtle`**</a>

    (showturtle)

Makes the turtle visible.

This procedure has no effect on the web interpreter, as the turtle is always
invisible.

*Alias: `st`*

<a class='builtin-header' id='speed'>**`speed`**</a>

    (speed <s>)

Sets the turtle's animation speed to some value between 0 and 10 with 0
indicating no animation and 1-10 indicating faster and faster movement.

This has no effect on the web interpreter, as everything is drawn immediately.