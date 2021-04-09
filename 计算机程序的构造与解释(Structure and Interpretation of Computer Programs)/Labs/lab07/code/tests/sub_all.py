test = {
  'name': 'sub_all',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (sub-all '(go ((bears))) '(go bears) '(big game))
          (big ((game)))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (sub-all '((4 calling birds) (3 french hens) (2 turtle doves))
          ....     '(1 2 3 4)
          ....     '(one two three four))
          ((four calling birds) (three french hens) (two turtle doves))
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
