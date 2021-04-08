test = {
  'name': 'substitute',
  'points': 300,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (substitute '(c a b) 'b 'l)
          (c a l)
          scm> (substitute '(f e a r s) 'f 'b)
          (b e a r s)
          scm> (substitute '(g (o) o (o)) 'o 'r)
          (g (r) r (r))
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (substitute '((lead guitar) (bass guitar) (rhythm guitar) drums)
          ....               'guitar 'axe)
          ((lead axe) (bass axe) (rhythm axe) drums)
          scm> (substitute '(romeo romeo wherefore art thou romeo) 'romeo 'paris)
          (paris paris wherefore art thou paris)
          scm> (substitute '((to be) or not (to (be))) 'be 'eat)
          ((to eat) or not (to (eat)))
          scm> (substitute '(a b (c) d e) 'foo 'bar)
          (a b (c) d e)
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
