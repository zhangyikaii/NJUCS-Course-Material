test = {
  'name': 'Problem 2',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> global_frame = create_global_frame()
          >>> global_frame.define("x", 3)
          >>> global_frame.parent is None
          b1796eff8a8e977439f97b5c6881a282
          # locked
          >>> global_frame.lookup("x")
          3c7e8a3a2176a696c3a66418f78dff6b
          # locked
          >>> global_frame.define("x", 2)
          >>> global_frame.lookup("x")
          2b7cdec3904f986982cbd24a0bc12887
          # locked
          >>> global_frame.lookup("foo")
          ec908af60f03727428c7ee3f22ec3cd8
          # locked
          # choice: None
          # choice: SchemeError
          # choice: 3
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> first_frame = create_global_frame()
          >>> first_frame.define("x", 3)
          >>> first_frame.define("y", False)
          >>> second_frame = Frame(first_frame)
          >>> second_frame.parent == first_frame
          b1796eff8a8e977439f97b5c6881a282
          # locked
          >>> second_frame.lookup("x")
          3c7e8a3a2176a696c3a66418f78dff6b
          # locked
          >>> second_frame.lookup("y")
          96ae38315990d5fb27de4225d8b470ba
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> first_frame = create_global_frame()
          >>> first_frame.define("x", 3)
          >>> second_frame = Frame(first_frame)
          >>> third_frame = Frame(second_frame)
          >>> fourth_frame = Frame(third_frame)
          >>> fourth_frame.lookup("x")
          3
          >>> second_frame.define("y", 1)
          >>> fourth_frame.lookup("y")
          1
          >>> first_frame.define("y", 0)
          >>> fourth_frame.lookup("y")
          1
          >>> fourth_frame.define("y", 2)
          >>> fourth_frame.lookup("y")
          2
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> first_frame = create_global_frame()
          >>> first_frame.define("x", 1)
          >>> second_frame = Frame(first_frame)
          >>> third_frame = Frame(second_frame)
          >>> fourth_frame = Frame(first_frame)
          >>> fifth_frame = Frame(fourth_frame)
          >>> fifth_frame.lookup("x")
          1
          >>> third_frame.lookup("x")
          1
          >>> second_frame.define("x", 2)
          >>> third_frame.lookup("x")
          2
          >>> fifth_frame.lookup("x")
          1
          >>> fifth_frame.define("x", 5)
          >>> fifth_frame.lookup("x")
          5
          >>> fourth_frame.lookup("x")
          1
          >>> first_frame.define("x", 4)
          >>> fourth_frame.lookup("x")
          4
          >>> third_frame.lookup("x")
          2
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme import *
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          scm> +
          #[+]
          scm> display
          #[display]
          scm> hello
          SchemeError
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
