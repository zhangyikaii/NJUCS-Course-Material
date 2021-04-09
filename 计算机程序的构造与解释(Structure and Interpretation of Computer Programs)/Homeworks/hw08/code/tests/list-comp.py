test = {
  'name': 'list-comp',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (list-of (* x x) for x in '(3 4 5) if (odd? x))
          (9 25)
          scm> (list-of (* x x) for x in '(3 4 5) if (lambda (x) x))
          (9 16 25)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (list-of (* 2 x) for x in (list-of (* y y) for y in '(1 2 3 4 5) if (lambda (x) x)) if (odd? x))
          (2 18 50)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (list-of 'hi for x in '(1 2 3 4 5 6) if (= (modulo x 3) 0))
          (hi hi)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (list-of (car e) for e in '((10) 11 (12) 13 (14 15)) if (list? e))
          (10 12 14)
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      scm> (load 'hw08)
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
