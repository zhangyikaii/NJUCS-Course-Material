test = {
  'name': 'derive-product',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (make-product 2 3)
          6
          scm> (make-product 'x 0)
          0
          scm> (make-product 1 'x)
          x
          scm> (make-product 'a 'x)
          (* a x)
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      scm> (load-all ".")
      """,
      'teardown': '',
      'type': 'scheme'
    },
    {
      'cases': [
        {
          'code': r"""
          scm> (derive '(* x y) 'x)
          y
          scm> (derive '(+ x (* x y)) 'x)
          (+ 1 y)
          scm> (derive '(* (* x y) (+ x 3)) 'x)
          (+ (* y (+ x 3)) (* x y))
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      scm> (load-all ".")
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
