test = {
  'name': 'Problem 13',
  'points': 200,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (cond ((> 2 3) 5)
          ....       ((> 2 4) 6)
          ....       ((< 2 5) 7)
          ....       (else 8))
          55f5a4841f9c1eacb1796dc6b0ba6ee9
          # locked
          scm> (cond ((> 2 3) 5)
          ....       ((> 2 4) 6)
          ....       (else 8))
          c0601ee237917e38c49efbb7371235c5
          # locked
          scm> (cond ((= 1 1))
          ....       ((= 4 4) 'huh) 
          ....       (else 'no))
          c65729b823194bffbccc4a162f8653bd
          # locked
          """,
          'hidden': False,
          'locked': True
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
          scm> (cond ((> 2 3) 5)
          ....       ((> 2 4) 6)
          ....       ((< 2 5) 7))
          7
          scm> (cond ((> 2 3) (display 'oops) (newline))
          ....       (else 9))
          9
          scm> (cond ((< 2 1))
          ....       ((> 3 2))
          ....       (else 5))
          #t
          scm> (cond (#f 1))
          scm> (cond ((= 4 3) 'nope)
          ....       ((= 4 4) 'hi)
          ....       (else 'wat))
          hi
          scm> (cond ((= 4 4) (+ 40 2))
          ....       (else 'wat 0))
          42
          scm> (cond (12))
          12
          scm> (cond ((= 4 3))
          ....       ('hi))
          hi
          scm> (eval (cond (False 1) (False 2)))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (cond (0 'yea)
          ....       (else 'nay))
          yea
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define x 0)
          x
          scm> (define y 0)
          y
          scm> (define z 0)
          z
          scm> (cond (#t
          ....        (define x (+ x 1))
          ....        (define y (+ y 1))
          ....        (define z (+ z 1)))
          ....       (else
          ....        (define x (- x 5))
          ....        (define y (- y 5))
          ....        (define z (- z 5))))
          z
          scm> (list x y z)
          (1 1 1)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define x 0)
          x
          scm> (cond ((define x (+ x 1)) 'a)
          ....       ((define x (+ x 100)) 'b))
          a
          scm> x
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (print-and-false val)
          ....         (print val)
          ....         #f)
          print-and-false
          scm> (cond ((print-and-false 'cond1))
          ....       ((print-and-false 'cond2))
          ....       ((print-and-false 'cond3))
          ....       ((print-and-false 'cond4)))
          cond1
          cond2
          cond3
          cond4
          scm> (define (print-and-true val)
          ....         (print val)
          ....         #t)
          print-and-true
          scm> (cond ((print-and-false 'cond1))
          ....       ((print-and-false 'cond2))
          ....       ((print-and-true 'cond3))
          ....       ((print-and-false 'cond4)))
          cond1
          cond2
          cond3
          #t
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
