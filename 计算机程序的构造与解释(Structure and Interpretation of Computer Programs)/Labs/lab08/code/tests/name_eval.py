test = {
  'name': 'name_eval',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> env = {
          ...     'a': Number(1),
          ...     'b': LambdaFunction([], Literal(0), {})
          ... }
          >>> Name('a').eval(env)
          Number(1)
          >>> Name('b').eval(env)
          LambdaFunction([], Literal(0), {})
          >>> print(Name('c').eval(env))
          None
          >>> env['a']
          Number(1)
          >>> env['b']
          LambdaFunction([], Literal(0), {})
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
