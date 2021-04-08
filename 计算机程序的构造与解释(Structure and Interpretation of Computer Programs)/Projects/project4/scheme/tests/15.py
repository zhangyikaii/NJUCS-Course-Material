test = {
  'name': 'Problem 15',
  'points': 200,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (enumerate '(3 4 5 6))
          ((0 3) (1 4) (2 5) (3 6))
          scm> (enumerate '(9 8 7 6 5 4))
          ((0 9) (1 8) (2 7) (3 6) (4 5) (5 4))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (enumerate '(a b c d))
          ((0 a) (1 b) (2 c) (3 d))
          scm> (enumerate '())
          ()
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      scm> (load 'questions)
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
