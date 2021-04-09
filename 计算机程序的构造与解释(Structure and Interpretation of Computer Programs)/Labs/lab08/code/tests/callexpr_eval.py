test = {
  'name': 'callexpr-eval',
  'points': 200,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> new_env = global_env.copy()
          >>> new_env.update({'a': Number(1), 'b': Number(2)})
          >>> add = CallExpr(Name('add'), [Literal(3), Name('a')])
          >>> add.eval(new_env)
          Number(4)
          >>> new_env['a'] = Number(5)
          >>> add.eval(new_env)
          Number(8)
          >>> read('max(b, a, 4, -1)').eval(new_env)
          Number(5)
          >>> read('add(mul(3, 4), b)').eval(new_env)
          Number(14)
          >>> new_env['b'] = new_env['a']
          >>> read('add(mul(3, 4), b)').eval(new_env)
          Number(17)
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from reader import read
      >>> from expr import *
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
