test = {
  'name': 'Problem 11',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (define (square x) (* x x))
          square
          scm> square
          (lambda (x) (* x x))
          scm> (square 21)
          441
          scm> square ; check to make sure lambda body hasn't changed
          (lambda (x) (* x x))
          scm> (define square (lambda (x) (* x x)))
          square
          scm> (square (square 21))
          194481
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> ((lambda (x) (list x (list (quote quote) x))) (quote (lambda (x) (list x (list (quote quote) x)))))
          ((lambda (x) (list x (list (quote quote) x))) (quote (lambda (x) (list x (list (quote quote) x)))))
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
          >>> double = do_lambda_form(read_line("((n) (* 2 n))"), env) # make double a LambdaProcedure that doubles a number
          >>> f1 = double.make_call_frame(Pair(10, nil), env)
          >>> f1.lookup('n')
          10
          >>> env.define('n', 5)
          >>> add_n = do_lambda_form(read_line("((x) (+ x n))"), env)
          >>> f2 = add_n.make_call_frame(Pair(5, nil), f1) # pass in a different environment as env
          >>> f2.lookup('x')
          5
          >>> f2.lookup('n') # Hint: make sure you're using self.env not env
          5
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> do_twice = do_lambda_form(read_line("((f x) (f (f x)))"), env) # make do_twice a LambdaProcedure that takes f, x, and returns f(f(x))
          >>> double = do_lambda_form(read_line("((x) (* 2 x))"), env) # make double a LambdaProcedure that doubles a number
          >>> call_frame = do_twice.make_call_frame(Pair(double, Pair(3, nil)), env) # Hint: make sure you're not evaluating args again in make_call_frame
          >>> call_frame.lookup('x') # Check that x is properly defined
          3
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme import *
      >>> env = create_global_frame()
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          scm> (define (outer x y)
          ....   (define (inner z x)
          ....     (+ x (* y 2) (* z 3)))
          ....   (inner x 10))
          71fe94b728b1cb1923a1c51c2533bcd8
          # locked
          scm> (outer 1 2)
          5d3ec98dabcf5b4a06694ccc93722cfb
          # locked
          scm> (define (outer-func x y)
          ....   (define (inner z x)
          ....     (+ x (* y 2) (* z 3)))
          ....   inner)
          0b6323ff730faa1f7ac702f64f4cbfcb
          # locked
          scm> ((outer-func 1 2) 1 10)
          5d3ec98dabcf5b4a06694ccc93722cfb
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          scm> (define square (lambda (x) (* x x)))
          square
          scm> (define (sum-of-squares x y) (+ (square x) (square y)))
          sum-of-squares
          scm> (sum-of-squares 3 4)
          25
          scm> (define double (lambda (x) (* 2 x)))
          double
          scm> (define compose (lambda (f g) (lambda (x) (f (g x)))))
          compose
          scm> (define apply-twice (lambda (f) (compose f f)))
          apply-twice
          scm> ((apply-twice double) 5)
          20
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
