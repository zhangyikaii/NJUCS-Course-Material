test = {
  'name': 'over-or-under',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (over-or-under 5 5)
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (over-or-under 5 4)
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (over-or-under 3 5)
          -1
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
