test = {
  'name': 'Problem 4',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> expr = read_line('(+ 2 2)')
          >>> scheme_eval(expr, create_global_frame()) # Type SchemeError if you think this errors
          4
          >>> scheme_eval(Pair('+', Pair(2, Pair(2, nil))), create_global_frame()) # Type SchemeError if you think this errors
          4
          >>> expr = read_line('(+ (+ 2 2) (+ 1 3) (* 1 4))')
          >>> scheme_eval(expr, create_global_frame()) # Type SchemeError if you think this errors
          12
          >>> expr = read_line('(yolo)')
          >>> scheme_eval(expr, create_global_frame()) # Type SchemeError if you think this errors
          SchemeError
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme_reader import *
      >>> from scheme import *
      
      >>> @builtin("print-then-return")
      ... def scheme_print_return(val1, val2):
      ...     print(repl_str(val1))
      ...     return val2
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          scm> (* (+ 3 2) (+ 1 7)) ; Type SchemeError if you think this errors
          40
          scm> (1 2) ; Type SchemeError if you think this errors
          SchemeError
          scm> (1 (print 0)) ; validate_procedure should be called before operands are evaluated
          SchemeError
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (+ 2 3) ; Type SchemeError if you think this errors
          5
          scm> (+)
          0
          scm> (odd? 13)
          #t
          scm> (car (list 1 2 3 4))
          1
          scm> (car car)
          SchemeError
          scm> (odd? 1 2 3)
          SchemeError
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (+ (+ 1) (* 2 3) (+ 5) (+ 6 (+ 7)))
          25
          scm> (*)
          1
          scm> (-)
          SchemeError
          scm> (car (cdr (cdr (list 1 2 3 4))))
          3
          scm> (car cdr (list 1))
          SchemeError
          scm> (* (car (cdr (cdr (list 1 2 3 4)))) (car (cdr (list 1 2 3 4))))
          6
          scm> (* (car (cdr (cdr (list 1 2 3 4)))) (cdr (cdr (list 1 2 3 4))))
          SchemeError
          scm> (+ (/ 1 0))
          SchemeError
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> ((/ 1 0) (print 5)) ; operator should be evaluated before operands
          SchemeError
          scm> (null? (print 5)) ; operands should only be evaluated once
          5
          #f
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'scheme'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> expr = read_line('((print-then-return 1 +) 1 2)')
          >>> scheme_eval(expr, global_frame) # operator should only be evaluated once
          1
          3
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme_reader import *
      >>> from scheme import *
      >>> global_frame = create_global_frame()     
      >>> def scheme_print_return(val1, val2):
      ...     print(repl_str(val1))
      ...     return val2
      >>> global_frame.define('print-then-return',
               BuiltinProcedure(scheme_print_return, False, 'print-then-return'))
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
