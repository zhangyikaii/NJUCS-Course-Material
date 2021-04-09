test = {
  'name': 'What Would Scheme Print?',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (cons 1 (cons 2 nil))
          5ceacf97ccefe7d64916c8d72dfb2b48
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          scm> (car (cons 1 (cons 2 nil)))
          7cd20da6435c318b417f99ab831ac85e
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          scm> (cdr (cons 1 (cons 2 nil)))
          36f31b0ebd049141c21558b1c3b4894d
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          scm> (list 1 2 3)
          31df56b0e4230528bca8a8edc01115c8
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          scm> '(1 2 3)
          31df56b0e4230528bca8a8edc01115c8
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          scm> (cons 1 '(list 2 3))  ; Recall quoting
          9b9cf94f8db477d48f973c67acf1842a
          # locked
          """,
          'hidden': False,
          'locked': True
        }
      ],
      'scored': True,
      'setup': r"""
      
      """,
      'teardown': '',
      'type': 'scheme'
    },
    {
      'cases': [
        {
          'code': r"""
          scm> '(cons 4 (cons (cons 6 8) ()))
          beed0382fff95ecdd5f05fad62b13daf
          # locked
          """,
          'hidden': False,
          'locked': True
        }
      ],
      'scored': True,
      'setup': r"""
      
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
