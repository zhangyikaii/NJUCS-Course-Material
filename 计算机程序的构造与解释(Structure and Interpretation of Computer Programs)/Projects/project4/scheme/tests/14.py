test = {
  'name': 'Problem 14',
  'points': 200,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (define x 1)
          38ba916dc1f41eb239567ee41a251ecd
          # locked
          scm> (let ((x 5))
          ....    (+ x 3))
          c0601ee237917e38c49efbb7371235c5
          # locked
          scm> x
          eb892a26497f936d1f6cae54aacc5f51
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          scm> (let ((a 1) (b a)) b)
          ec908af60f03727428c7ee3f22ec3cd8
          # locked
          # choice: SchemeError
          # choice: 1
          # choice: x
          # choice: y
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          scm> (let ((x 5))
          ....    (let ((x 2)
          ....          (y x))
          ....        (+ y (* x 2))))
          27c11fef0d1b8697654b38bb53c550c8
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          scm> (define (square x) (* x x))
          square
          scm> (define (f x y)
          ....    (let ((a (+ 1 (* x y)))
          ....          (b (- 1 y)))
          ....        (+ (* x (square a))
          ....           (* y b)
          ....           (* a b))))
          f
          scm> (f 3 4)
          456
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
          >>> # Incorrectly formatted bindings
          >>> bindings = Pair(Pair('x', Pair(2, nil)), Pair(Pair('y', nil), nil)) # equivalent to ((x 2) (y))
          >>> make_let_frame(bindings, global_frame) 
          SchemeError
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Improper formals list - used same variable name twice
          >>> bindings = Pair(Pair('x', Pair(2, nil)), Pair(Pair('x', Pair(3, nil)), nil)) # equivalent to ((x 2) (x 3))
          >>> make_let_frame(bindings, global_frame) 
          SchemeError
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> bindings = Pair(Pair('x', Pair(2, nil)), Pair(Pair('y', Pair(3, nil)), nil)) # equivalent to ((x 2) (y 3))
          >>> f1 = make_let_frame(bindings, global_frame)
          >>> f1.lookup('x')
          2
          >>> bindings # make sure bindings isn't mutated
          Pair(Pair('x', Pair(2, nil)), Pair(Pair('y', Pair(3, nil)), nil))
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme import *
      >>> global_frame = create_global_frame()
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          scm> (define x 3)
          x
          scm> (define y 4)
          y
          scm> (let ((x (+ y 2))
          ....       (y (+ x 2)))
          ....      (cons x (cons y nil)))
          (6 5)
          scm> (let ((x 'hello)) x)
          hello
          scm> (let ((a 1) (b 2) (c 3)) (+ a b c))
          6
          scm> (define z 0)
          z
          scm> (let ((a (define z (+ z 1)))) z)
          1
          scm> (let ((x 1)
          ....       (y 3))
          ....    (define x (+ x 1))
          ....    (list x y))
          (2 3)
          scm> (let ((a 1 1)) a)
          SchemeError
          scm> (let ((a 1) (2 2)) a)
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
    }
  ]
}
