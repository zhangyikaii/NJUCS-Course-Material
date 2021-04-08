test = {
  'name': 'Problem 10',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'answer': 'A TankAnt does damage to all Bees in its place each turn',
          'choices': [
            'A TankAnt does damage to all Bees in its place each turn',
            'A TankAnt has greater armor than a BodyguardAnt',
            'A TankAnt can contain multiple ants',
            'A TankAnt increases the damage of the ant it contains'
          ],
          'hidden': False,
          'locked': False,
          'question': r"""
          Besides costing more to deploy, what is the only difference between a
          TankAnt and a BodyguardAnt?
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
          >>> # Testing TankAnt parameters
          >>> TankAnt.food_cost
          6
          >>> TankAnt.damage
          1
          >>> tank = TankAnt()
          >>> tank.armor
          2
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing TankAnt action
          >>> tank = TankAnt()
          >>> place = gamestate.places['tunnel_0_1']
          >>> other_place = gamestate.places['tunnel_0_2']
          >>> place.add_insect(tank)
          >>> for _ in range(3):
          ...     place.add_insect(Bee(3))
          >>> other_place.add_insect(Bee(3))
          >>> tank.action(gamestate)
          >>> [bee.armor for bee in place.bees]
          [2, 2, 2]
          >>> [bee.armor for bee in other_place.bees]
          [3]
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing TankAnt container methods
          >>> tank = TankAnt()
          >>> thrower = ThrowerAnt()
          >>> place = gamestate.places['tunnel_0_1']
          >>> place.add_insect(thrower)
          >>> place.add_insect(tank)
          >>> place.ant is tank
          True
          >>> bee = Bee(3)
          >>> place.add_insect(bee)
          >>> tank.action(gamestate)   # Both ants attack bee
          >>> bee.armor
          1
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      >>> from ants_plans import *
      >>> beehive, layout = Hive(make_test_assault_plan()), dry_layout
      >>> dimensions = (1, 9)
      >>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
      >>> #
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing TankAnt action
          >>> tank = TankAnt()
          >>> place = gamestate.places['tunnel_0_1']
          >>> place.add_insect(tank)
          >>> for _ in range(3):
          ...     place.add_insect(Bee(1))
          >>> tank.action(gamestate)
          >>> len(place.bees)
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing TankAnt.damage
          >>> tank = TankAnt()
          >>> tank.damage = 100
          >>> place = gamestate.places['tunnel_0_1']
          >>> place.add_insect(tank)
          >>> for _ in range(3):
          ...     place.add_insect(Bee(100))
          >>> tank.action(gamestate)
          >>> len(place.bees)
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Placement of ants
          >>> tank = TankAnt()
          >>> harvester = HarvesterAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> # Add tank before harvester
          >>> place.add_insect(tank)
          >>> place.add_insect(harvester)
          >>> gamestate.food = 0
          >>> tank.action(gamestate)
          >>> gamestate.food
          1
          >>> try:
          ...   place.add_insect(TankAnt())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.ant is tank
          True
          >>> tank.contained_ant is harvester
          True
          >>> try:
          ...   place.add_insect(HarvesterAnt())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.ant is tank
          True
          >>> tank.contained_ant is harvester
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Placement of ants
          >>> tank = TankAnt()
          >>> harvester = HarvesterAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> # Add harvester before tank
          >>> place.add_insect(harvester)
          >>> place.add_insect(tank)
          >>> gamestate.food = 0
          >>> tank.action(gamestate)
          >>> gamestate.food
          1
          >>> try:
          ...   place.add_insect(TankAnt())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.ant is tank
          True
          >>> tank.contained_ant is harvester
          True
          >>> try:
          ...   place.add_insect(HarvesterAnt())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.ant is tank
          True
          >>> tank.contained_ant is harvester
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Removing ants
          >>> tank = TankAnt()
          >>> test_ant = Ant()
          >>> place = Place('Test')
          >>> place.add_insect(tank)
          >>> place.add_insect(test_ant)
          >>> place.remove_insect(test_ant)
          >>> tank.contained_ant is None
          True
          >>> test_ant.place is None
          True
          >>> place.remove_insect(tank)
          >>> place.ant is None
          True
          >>> tank.place is None
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> tank = TankAnt()
          >>> place = Place('Test')
          >>> place.add_insect(tank)
          >>> tank.action(gamestate) # Action without contained ant should not error
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # test proper call to death callback
          >>> original_death_callback = Insect.death_callback
          >>> Insect.death_callback = lambda x: print("insect died")
          >>> place = gamestate.places["tunnel_0_0"]
          >>> bee = Bee(3)
          >>> tank = TankAnt()
          >>> ant = ThrowerAnt()
          >>> place.add_insect(bee)
          >>> place.add_insect(ant)
          >>> place.add_insect(tank)
          >>> bee.action(gamestate)
          >>> bee.action(gamestate)
          insect died
          >>> bee.action(gamestate) # if you fail this test you probably didn't correctly call Ant.reduce_armor or Insect.reduce_armor
          insect died
          >>> Insect.death_callback = original_death_callback
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      >>> from ants_plans import *
      >>> beehive, layout = Hive(make_test_assault_plan()), dry_layout
      >>> dimensions = (1, 9)
      >>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
      >>> #
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> from ants import *
          >>> TankAnt.implemented
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
