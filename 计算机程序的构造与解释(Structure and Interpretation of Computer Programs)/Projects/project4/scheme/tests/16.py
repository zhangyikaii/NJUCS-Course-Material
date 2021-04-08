test = {
  'name': 'Problem 16',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (merge < '(1 4 6) '(2 5 8))
          (1 2 4 5 6 8)
          scm> (merge > '(6 4 1) '(8 5 2))
          (8 6 5 4 2 1)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (merge < '(1) '(2 3 5))
          (1 2 3 5)
          scm> (merge > '(2 4 5) '())
          (2 4 5)
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
