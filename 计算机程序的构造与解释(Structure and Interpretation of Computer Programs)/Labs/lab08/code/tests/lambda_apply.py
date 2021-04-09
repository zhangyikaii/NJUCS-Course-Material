test = {
  'name': 'lambda-apply',
  'points': 200,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> add_lambda = read('lambda x, y: add(x, y)').eval(global_env)
          >>> add_lambda.apply([Number(1), Number(2)])
          Number(3)
          >>> add_lambda.apply([Number(3), Number(4)])
          Number(7)
          >>> sub_lambda = read('lambda add: sub(10, add)').eval(global_env)
          >>> sub_lambda.apply([Number(8)])
          Number(2)
          >>> add_lambda.apply([Number(8), Number(10)]) # Make sure you made a copy of env
          Number(18)
          >>> read('(lambda x: lambda y: add(x, y))(3)(4)').eval(global_env)
          Number(7)
          >>> read('(lambda x: x(x))(lambda y: 4)').eval(global_env)
          Number(4)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> max_lambda = read('lambda x, y: max(x, y)').eval(global_env)
          >>> new_env = global_env.copy()
          >>> new_env.update({'max_lambda': Number(4), 'a': Number(2)})
          >>> new_env['a'] = max_lambda.apply([Number(4), Number(-2)])
          >>> read('add(a, max_lambda)').eval(new_env)
          Number(8)
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
