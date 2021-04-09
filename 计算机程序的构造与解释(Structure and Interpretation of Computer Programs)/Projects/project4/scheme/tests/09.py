test = {
  'name': 'Problem 9',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (define (f x y) (+ x y))
          715124391110b4a3beec8c9ba1ec3097
          # locked
          scm> f
          1456de84c3edf333b6f7aee0c0624b20
          # locked
          # choice: (lambda (x y) (+ x y))
          # choice: (lambda (f x y) (+ x y))
          # choice: (f (x y) (+ x y))
          # choice: (define f (lambda (x y) (+ x y)))
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          scm> (define (f) (+ 2 2))
          f
          scm> f
          (lambda () (+ 2 2))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (f x) (* x x))
          f
          scm> f
          (lambda (x) (* x x))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (foo x) 1 2 3 4 5)
          foo
          scm> foo
          (lambda (x) 1 2 3 4 5)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (foo) (/ 1 0))
          foo
          scm> foo
          (lambda () (/ 1 0))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (f 1 2 3) 4) ; check that you have valid formals
          SchemeError
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
          >>> inp = read_line("(define (f x) x)")
          >>> scheme_eval(inp, env)
          'f'
          >>> scheme_eval('f', env)
          LambdaProcedure(Pair('x', nil), Pair('x', nil), <Global Frame>)
          >>> inp == read_line("(define (f x) x)") # Don't mutate the input expression!
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme_reader import *
      >>> from scheme import *
      >>> env = create_global_frame()
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
