test = {
  'name': 'Problem 10',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> formals = Pair('a', Pair('b', Pair('c', nil)))
          >>> vals = Pair(1, Pair(2, Pair(3, nil)))
          >>> frame = global_frame.make_child_frame(formals, vals)
          >>> global_frame.lookup('a') # Type SchemeError if you think this errors
          ec908af60f03727428c7ee3f22ec3cd8
          # locked
          >>> frame.lookup('a')        # Type SchemeError if you think this errors
          eb892a26497f936d1f6cae54aacc5f51
          # locked
          >>> frame.lookup('b')        # Type SchemeError if you think this errors
          2b7cdec3904f986982cbd24a0bc12887
          # locked
          >>> frame.lookup('c')        # Type SchemeError if you think this errors
          3c7e8a3a2176a696c3a66418f78dff6b
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> frame = global_frame.make_child_frame(nil, nil)
          >>> frame.parent is global_frame
          b1796eff8a8e977439f97b5c6881a282
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> first = Frame(global_frame)
          >>> second = first.make_child_frame(nil, nil)
          >>> second.parent is first
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme import *
      >>> global_frame = create_global_frame()
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # More argument values than formal parameters
          >>> global_frame.make_child_frame(Pair('a', nil), Pair(1, Pair(2, Pair(3, nil))))
          SchemeError
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # More formal parameters than argument values
          >>> global_frame.make_child_frame(Pair('a', Pair('b', Pair('c', nil))), Pair(1, nil))
          SchemeError
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Values can be pairs.
          >>> formals = Pair('a', Pair('b', nil))
          >>> values = Pair(Pair(1, nil), Pair(Pair(2, nil), nil))
          >>> frame = global_frame.make_child_frame(formals, values)
          >>> frame.lookup('a')
          Pair(1, nil)
          >>> frame.lookup('b')
          Pair(2, nil)
          >>> frame2 = frame.make_child_frame(nil, nil) # Bind parents correctly
          >>> frame2.lookup('a')
          Pair(1, nil)
          >>> formals # Ensure that formals was not mutated
          Pair('a', Pair('b', nil))
          >>> values # Ensure that values was not mutated
          Pair(Pair(1, nil), Pair(Pair(2, nil), nil))
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme import *
      >>> global_frame = create_global_frame()
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
