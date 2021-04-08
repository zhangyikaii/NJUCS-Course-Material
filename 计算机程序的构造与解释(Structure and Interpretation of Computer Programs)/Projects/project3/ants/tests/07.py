test = {
  'name': 'Problem 7',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'answer': 'All Ant types have a blocks_path attribute that is inherited from the Ant superclass',
          'choices': [
            r"""
            All Ant types have a blocks_path attribute that is inherited from
            the Ant superclass
            """,
            'Only the NinjaAnt has a blocks_path attribute',
            'None of the Ant subclasses have a blocks_path attribute',
            'All Ant types except for NinjaAnt have a blocks_path attribute'
          ],
          'hidden': False,
          'locked': False,
          'question': 'Which Ant types have a blocks_path attribute?'
        },
        {
          'answer': 'blocks_path is True for every Ant subclass except NinjaAnt',
          'choices': [
            'blocks_path is True for every Ant subclass except NinjaAnt',
            'blocks_path is False for every Ant subclass except NinjaAnt',
            'blocks_path is True for all Ants',
            'blocks_path is False for all Ants'
          ],
          'hidden': False,
          'locked': False,
          'question': 'What is the value of blocks_path for each Ant subclass?'
        },
        {
          'answer': "When there is an Ant whose blocks_path attribute is True in the Bee's place",
          'choices': [
            "When there is an Ant in the Bee's place",
            r"""
            When there is an Ant whose blocks_path attribute is True in the
            Bee's place
            """,
            "When there is not an NinjaAnt in the Bee's place",
            "When there are no Ants in the Bee's place"
          ],
          'hidden': False,
          'locked': False,
          'question': 'When is the path of a Bee blocked?'
        },
        {
          'answer': "Reduces the Bee's armor by the NinjaAnt's damage attribute",
          'choices': [
            "Reduces the Bee's armor by the NinjaAnt's damage attribute",
            "Reduces the Bee's armor to 0",
            "Nothing, the NinjaAnt doesn't damage Bees",
            "Blocks the Bee's path"
          ],
          'hidden': False,
          'locked': False,
          'question': 'What does a NinjaAnt do to each Bee that flies in its place?'
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing NinjaAnt parameters
          >>> ninja = NinjaAnt()
          >>> ninja.armor
          1
          >>> NinjaAnt.food_cost
          5
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing blocks_path
          >>> NinjaAnt.blocks_path
          False
          >>> HungryAnt.blocks_path
          True
          >>> FireAnt.blocks_path
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing NinjaAnts do not block bees
          >>> p0 = gamestate.places["tunnel_0_0"]
          >>> p1 = gamestate.places["tunnel_0_1"]  # p0 is p1's exit
          >>> bee = Bee(2)
          >>> ninja = NinjaAnt()
          >>> thrower = ThrowerAnt()
          >>> p0.add_insect(thrower)            # Add ThrowerAnt to p0
          >>> p1.add_insect(bee)
          >>> p1.add_insect(ninja)              # Add the Bee and NinjaAnt to p1
          >>> bee.action(gamestate)
          >>> bee.place is ninja.place          # Did NinjaAnt block the Bee from moving?
          False
          >>> bee.place is p0
          True
          >>> ninja.armor
          1
          >>> bee.action(gamestate)
          >>> bee.place is p0                   # Did ThrowerAnt block the Bee from moving?
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing non-blocking ants do not block bees
          >>> p0 = gamestate.places["tunnel_0_0"]
          >>> p1 = gamestate.places["tunnel_0_1"]  # p0 is p1's exit
          >>> bee = Bee(2)
          >>> ninja_fire = FireAnt(1)
          >>> ninja_fire.blocks_path = False
          >>> thrower = ThrowerAnt()
          >>> p0.add_insect(thrower)            # Add ThrowerAnt to p0
          >>> p1.add_insect(bee)
          >>> p1.add_insect(ninja_fire)              # Add the Bee and NinjaAnt to p1
          >>> bee.action(gamestate)
          >>> bee.place is ninja_fire.place          # Did the "ninjaish" FireAnt block the Bee from moving?
          False
          >>> bee.place is p0
          True
          >>> ninja_fire.armor
          1
          >>> bee.action(gamestate)
          >>> bee.place is p0                   # Did ThrowerAnt block the Bee from moving?
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing NinjaAnt strikes all bees in its place
          >>> test_place = gamestate.places["tunnel_0_0"]
          >>> for _ in range(3):
          ...     test_place.add_insect(Bee(2))
          >>> ninja = NinjaAnt()
          >>> test_place.add_insect(ninja)
          >>> ninja.action(gamestate)   # should strike all bees in place
          >>> [bee.armor for bee in test_place.bees]
          [1, 1, 1]
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing NinjaAnt doesn't hardcode damage
          >>> test_place = gamestate.places["tunnel_0_0"]
          >>> for _ in range(3):
          ...     test_place.add_insect(Bee(100))
          >>> ninja = NinjaAnt()
          >>> ninja.damage = 50
          >>> test_place.add_insect(ninja)
          >>> ninja.action(gamestate)   # should strike all bees in place
          >>> [bee.armor for bee in test_place.bees]
          [50, 50, 50]
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing NinjaAnt strikes all bees, even if some expire
          >>> test_place = gamestate.places["tunnel_0_0"]
          >>> for _ in range(3):
          ...     test_place.add_insect(Bee(1))
          >>> ninja = NinjaAnt()
          >>> test_place.add_insect(ninja)
          >>> ninja.action(gamestate)   # should strike all bees in place
          >>> len(test_place.bees)
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing damage is looked up on the instance
          >>> place = gamestate.places["tunnel_0_0"]
          >>> bee = Bee(900)
          >>> place.add_insect(bee)
          >>> buffNinja = NinjaAnt()
          >>> buffNinja.damage = 500  # Sharpen the sword
          >>> place.add_insect(buffNinja)
          >>> buffNinja.action(gamestate)
          >>> bee.armor
          400
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing Ninja ant does not crash when left alone
          >>> ninja = NinjaAnt()
          >>> gamestate.places["tunnel_0_0"].add_insect(ninja)
          >>> ninja.action(gamestate)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing Bee does not crash when left alone
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_1"].add_insect(bee)
          >>> bee.action(gamestate)
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      >>> beehive, layout = Hive(AssaultPlan()), dry_layout
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
          >>> NinjaAnt.implemented
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
