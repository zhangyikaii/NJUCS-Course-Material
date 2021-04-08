test = {
  'name': 'Problem 18 (Optional)',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (define y 1)
          y
          scm> (define f (mu (x) (+ x y)))
          f
          scm> (define g (lambda (x y) (f (+ x x))))
          g
          scm> (g 3 7)
          13
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
          scm> (define h (mu () x))
          h
          scm> (define (high fn x) (fn))
          high
          scm> (high h 2)
          2
          scm> (define (f x) (mu () (lambda (y) (+ x y))))
          f
          scm> (define (g x) (((f (+ x 1))) (+ x 2)))
          g
          scm> (g 3)
          8
          scm> (mu ())
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
