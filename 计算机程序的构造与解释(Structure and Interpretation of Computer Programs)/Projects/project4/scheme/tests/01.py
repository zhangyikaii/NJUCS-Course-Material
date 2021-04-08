test = {
  'name': 'Problem 1',
  'points': 200,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> scheme_read(Buffer(tokenize_lines(['nil'])))
          nil
          >>> scheme_read(Buffer(tokenize_lines(['1'])))
          1
          >>> scheme_read(Buffer(tokenize_lines(['true'])))
          True
          >>> read_tail(Buffer(tokenize_lines(['2)'])))
          Pair(2, nil)
          >>> read_tail(Buffer(tokenize_lines(['(2)'])))
          SyntaxError
          >>> read_line('3')
          3
          >>> read_line('-123')
          -123
          >>> read_line('1.25')
          1.25
          >>> read_line('true')
          True
          >>> read_line('(a)')
          Pair('a', nil)
          >>> read_line(')')
          SyntaxError
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> tokens = tokenize_lines(["(+ 1 ", "(23 4)) ("])
          >>> src = Buffer(tokens)
          >>> src.current()
          2562c1ff5c2fd136738cec508425ad6e
          # locked
          >>> src.pop_first()
          2562c1ff5c2fd136738cec508425ad6e
          # locked
          >>> src.current()
          7cb705e44890ff0de05e8ac610e43827
          # locked
          >>> src.pop_first()
          7cb705e44890ff0de05e8ac610e43827
          # locked
          >>> src.pop_first()
          eb892a26497f936d1f6cae54aacc5f51
          # locked
          >>> scheme_read(src)  # Removes the next complete expression in src and returns it as a Pair
          e4aaa1bb82547d5c561e01aa92ee3d6f
          # locked
          >>> src.current()
          94a32bedd6cf1898cd8986f0b4e2d011
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> scheme_read(Buffer(tokenize_lines(['(18 6)']))) # Type SyntaxError if you think this errors
          050a33077bbae4f681a23354ffb49a9e
          # locked
          >>> read_line('(18 6)')  # Shorter version of above!
          050a33077bbae4f681a23354ffb49a9e
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> read_tail(Buffer(tokenize_lines([')'])))
          c24ff8c9a7d7a50f82648d25a4d8fbb1
          # locked
          >>> read_tail(Buffer(tokenize_lines(['1 2 3)'])))
          4ced98984f008e5161274d6481e4b568
          # locked
          >>> read_tail(Buffer(tokenize_lines(['2 (3 4))'])))
          b27a7ad8eaed5119cfd16136ceb9ea5a
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> read_tail(Buffer(tokenize_lines(['(1 2 3)']))) # Type SyntaxError if you think this errors
          8c2bf83bd06967ba8dd8731d41d13081
          # locked
          >>> read_line('((1 2 3)') # Type SyntaxError if you think this errors
          8c2bf83bd06967ba8dd8731d41d13081
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> src = Buffer(tokenize_lines(["(+ 1 2)"]))
          >>> scheme_read(src)
          Pair('+', Pair(1, Pair(2, nil)))
          >>> src.current() # Don't forget to remove the closing parenthesis!
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> read_line("(+ (- 2 3) 1)")
          569af9099ed6ccade3e79b6d955b0405
          # locked
          # choice: Pair('+', Pair('-', Pair(2, Pair(3, Pair(1, nil)))))
          # choice: Pair('+', Pair('-', Pair(2, Pair(3, nil))), Pair(1, nil))
          # choice: Pair('+', Pair(Pair('-', Pair(2, Pair(3, nil))), Pair(1, nil)))
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> read_line("()")
          nil
          >>> read_line("((a))")
          Pair(Pair('a', nil), nil)
          >>> read_line("(+ 1 (- 2 3) 8)")
          Pair('+', Pair(1, Pair(Pair('-', Pair(2, Pair(3, nil))), Pair(8, nil))))
          # choice: Pair('+', Pair(1, Pair('-', Pair(2, 3), Pair(8, nil))))
          # choice: Pair('+', Pair(1, Pair(Pair('-', Pair(2, 3)), Pair(8, nil))))
          # choice: Pair('+', Pair(1, Pair('-', Pair(2, Pair(3, nil)), Pair(8, nil))))
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme_reader import *
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
