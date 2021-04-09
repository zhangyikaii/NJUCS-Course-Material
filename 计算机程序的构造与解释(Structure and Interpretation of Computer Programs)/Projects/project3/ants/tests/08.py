test = {
  'name': 'Problem 8',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'answer': 'Ant',
          'choices': [
            'Ant',
            'ThrowerAnt',
            'NinjaAnt',
            'The WallAnt class does not inherit from any class'
          ],
          'hidden': False,
          'locked': False,
          'question': 'What class does WallAnt inherit from?'
        },
        {
          'answer': 'A WallAnt takes no action each turn',
          'choices': [
            'A WallAnt takes no action each turn',
            'A WallAnt increases its own armor by 1 each turn',
            'A WallAnt reduces its own armor by 1 each turn',
            'A WallAnt attacks all the Bees in its place each turn'
          ],
          'hidden': False,
          'locked': False,
          'question': "What is a WallAnt's action?"
        },
        {
          'answer': 'Ant subclasses inherit the action method from the Insect class',
          'choices': [
            'Ant subclasses inherit the action method from the Insect class',
            'Ant subclasses inherit the action method from the Ant class',
            'Ant subclasses do not inherit the action method from any class'
          ],
          'hidden': False,
          'locked': False,
          'question': 'Where do Ant subclasses inherit the action method from?'
        },
        {
          'answer': 'Nothing',
          'choices': [
            'Nothing',
            'Throw a leaf at the nearest Bee',
            'Move to the next place',
            'Reduce the armor of all Bees in its place'
          ],
          'hidden': False,
          'locked': False,
          'question': r"""
          If a subclass of Ant does not override the action method, what is the
          default action?
          """
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing WallAnt parameters
          >>> wall = WallAnt()
          >>> wall.name
          'Wall'
          >>> wall.armor
          4
          >>> # `armor` should not be a class attribute
          >>> not hasattr(WallAnt, 'armor')
          True
          >>> WallAnt.food_cost
          4
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing WallAnt holds strong
          >>> beehive, layout = Hive(AssaultPlan()), dry_layout
          >>> gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))
          >>> place = gamestate.places['tunnel_0_4']
          >>> wall = WallAnt()
          >>> bee = Bee(1000)
          >>> place.add_insect(wall)
          >>> place.add_insect(bee)
          >>> for i in range(3):
          ...     bee.action(gamestate)
          ...     wall.action(gamestate)   # WallAnt does nothing
          >>> wall.armor
          1
          >>> bee.armor
          1000
          >>> wall.place is place
          True
          >>> bee.place is place
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> from ants import *
          >>> WallAnt.implemented
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
