test = {
  'name': 'Problem 11',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'answer': 'If the insect is not watersafe, its armor is reduced to 0. Otherwise, nothing happens.',
          'choices': [
            r"""
            If the insect is not watersafe, its armor is reduced to 0.
            Otherwise, nothing happens.
            """,
            "The insect's armor is reduced to 0.",
            'Nothing happens.',
            'The insect goes for a swim.'
          ],
          'hidden': False,
          'locked': False,
          'question': 'What happens when an insect is added to a Water Place?'
        },
        {
          'answer': 'class, all ants of a subclass should either be watersafe or not',
          'choices': [
            'class, all ants of a subclass should either be watersafe or not',
            'class, all ants should be watersafe',
            'instance, the is_watersafe attribute depends on the amount of armor a given ant has left',
            'instance, the is_watersafe attribute depends on the given place of an ant'
          ],
          'hidden': False,
          'locked': False,
          'question': 'What type of attribute should "is_watersafe" be?'
        },
        {
          'answer': 'reduce_armor, in the Insect class',
          'choices': [
            'reduce_armor, in the Insect class',
            'remove_insect, in the Place class',
            'sting, in the Bee class',
            'remove_ant, in the GameState class'
          ],
          'hidden': False,
          'locked': False,
          'question': r"""
          What method deals damage to an Insect and removes it from its place
          if its armor reaches 0?
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
          >>> # Testing water with Ants
          >>> test_water = Water('Water Test1')
          >>> ant = HarvesterAnt()
          >>> test_water.add_insect(ant)
          >>> (ant.armor, test_water.ant is None)
          (0, True)
          >>> ant = Ant()
          >>> test_water.add_insect(ant)
          >>> (ant.armor, test_water.ant is None)
          (0, True)
          >>> ant = ThrowerAnt()
          >>> test_water.add_insect(ant)
          >>> (ant.armor, test_water.ant is None)
          (0, True)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing water with soggy (non-watersafe) bees
          >>> test_bee = Bee(1000000)
          >>> test_bee.is_watersafe = False    # Make Bee non-watersafe
          >>> test_water = Water('Water Test2')
          >>> test_water.add_insect(test_bee)
          >>> test_bee.armor
          0
          >>> test_water.bees
          []
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing water with watersafe bees
          >>> test_bee = Bee(1)
          >>> test_water = Water('Water Test3')
          >>> test_water.add_insect(test_bee)
          >>> test_bee.armor
          1
          >>> test_water.bees == [test_bee]
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # test proper call to death callback
          >>> original_death_callback = Insect.death_callback
          >>> Insect.death_callback = lambda x: print("insect died")
          >>> place = Water('Water Test4')
          >>> soggy_bee = Bee(1)
          >>> soggy_bee.is_watersafe = False
          >>> place.add_insect(soggy_bee)
          insect died
          >>> place.add_insect(Bee(1))
          >>> place.add_insect(ThrowerAnt())
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
          >>> # Testing water inheritance
          >>> old_add_insect = Place.add_insect
          >>> def new_add_insect(self, insect):
          ...     print("called add_insect")
          ...     old_add_insect(self, insect)
          >>> Place.add_insect = new_add_insect
          >>> test_bee = Bee(1)
          >>> test_water = Water('Water Test4')
          >>> test_water.add_insect(test_bee) # if this fails you probably didn't call `add_insect`
          called add_insect
          >>> Place.add_insect = old_add_insect
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
      >>> old_add_insect = Place.add_insect
      """,
      'teardown': r"""
      >>> Place.add_insect = old_add_insect
      """,
      'type': 'doctest'
    }
  ]
}
