test = {
  'name': 'Problem 17',
  'points': 200,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (define s (list 1 2 3 1 2 2 1))
          s
          scm> (nondecreaselist s)
          ((1 2 3) (1 2 2) (1))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define s2 (list 1 2 3 4 1 2 3 4 1 1 1 2 1 1 0 4 3 2 1))
          s2
          scm> (nondecreaselist s2)
          ((1 2 3 4) (1 2 3 4) (1 1 1 2) (1 1) (0 4) (3) (2) (1))
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
