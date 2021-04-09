test = {
  'name': 'Problem 9',
  'points': 4,
  'suites': [
    {
      'cases': [
        {
          'answer': 'The Ant instance that is in the same place as itself',
          'choices': [
            'The Ant instance that is in the same place as itself',
            'The Ant instance in the place closest to its own place',
            'A random Ant instance in the gamestate',
            'All the Ant instances in the gamestate'
          ],
          'hidden': False,
          'locked': False,
          'question': 'Which Ant does a BodyguardAnt guard?'
        },
        {
          'answer': 'By hiding the ant from Bees and allowing it to perform its original action',
          'choices': [
            'By hiding the ant from Bees and allowing it to perform its original action',
            'By attacking Bees that try to attack it',
            "By increasing the ant's armor",
            'By allowing Bees to pass without attacking'
          ],
          'hidden': False,
          'locked': False,
          'question': 'How does a BodyguardAnt guard its ant?'
        },
        {
          'answer': "In the BodyguardAnt's contained_ant instance attribute",
          'choices': [
            "In the BodyguardAnt's contained_ant instance attribute",
            "In the BodyguardAnt's contained_ant class attribute",
            "In its place's ant instance attribute",
            "Nowhere, a BodyguardAnt has no knowledge of the ant that it's protecting"
          ],
          'hidden': False,
          'locked': False,
          'question': 'Where is the ant contained by a BodyguardAnt stored?'
        },
        {
          'answer': 'When exactly one of the Ant instances is a container and the container ant does not already contain another ant',
          'choices': [
            r"""
            When exactly one of the Ant instances is a container and the
            container ant does not already contain another ant
            """,
            'When exactly one of the Ant instances is a container',
            'When both Ant instances are containers',
            'There can never be two Ant instances in the same place'
          ],
          'hidden': False,
          'locked': False,
          'question': 'When can a second Ant be added to a place that already contains an Ant?'
        },
        {
          'answer': 'The container Ant',
          'choices': [
            'The container Ant',
            'The Ant being contained',
            'A list containing both Ants',
            'Whichever Ant was placed there first'
          ],
          'hidden': False,
          'locked': False,
          'question': r"""
          If two Ants occupy the same Place, what is stored in that place's ant
          instance attribute?
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
          >>> # Testing BodyguardAnt parameters
          >>> bodyguard = BodyguardAnt()
          >>> BodyguardAnt.food_cost
          4
          >>> bodyguard.armor
          2
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
          >>> bodyguard = BodyguardAnt()
          >>> bodyguard.action(gamestate) # Action without contained ant should not error
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing bodyguard performs thrower's action
          >>> bodyguard = BodyguardAnt()
          >>> thrower = ThrowerAnt()
          >>> bee = Bee(2)
          >>> # Place bodyguard before thrower
          >>> gamestate.places["tunnel_0_0"].add_insect(bodyguard)
          >>> gamestate.places["tunnel_0_0"].add_insect(thrower)
          >>> gamestate.places["tunnel_0_3"].add_insect(bee)
          >>> bodyguard.action(gamestate)
          >>> bee.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing bodyguard performs thrower's action
          >>> bodyguard = BodyguardAnt()
          >>> thrower = ThrowerAnt()
          >>> bee = Bee(2)
          >>> # Place thrower before bodyguard
          >>> gamestate.places["tunnel_0_0"].add_insect(thrower)
          >>> gamestate.places["tunnel_0_0"].add_insect(bodyguard)
          >>> gamestate.places["tunnel_0_3"].add_insect(bee)
          >>> bodyguard.action(gamestate)
          >>> bee.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing removing a bodyguard doesn't remove contained ant
          >>> place = gamestate.places['tunnel_0_0']
          >>> bodyguard = BodyguardAnt()
          >>> test_ant = Ant(1)
          >>> # add bodyguard first
          >>> place.add_insect(bodyguard)
          >>> place.add_insect(test_ant)
          >>> gamestate.remove_ant('tunnel_0_0')
          >>> place.ant is test_ant
          True
          >>> bodyguard.place is None
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing removing a bodyguard doesn't remove contained ant
          >>> place = gamestate.places['tunnel_0_0']
          >>> bodyguard = BodyguardAnt()
          >>> test_ant = Ant(1)
          >>> # add ant first
          >>> place.add_insect(test_ant)
          >>> place.add_insect(bodyguard)
          >>> gamestate.remove_ant('tunnel_0_0')
          >>> place.ant is test_ant
          True
          >>> bodyguard.place is None
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing bodyguarded ant keeps instance attributes
          >>> test_ant = Ant()
          >>> def new_action(gamestate):
          ...     test_ant.armor += 9000
          >>> test_ant.action = new_action
          >>> place = gamestate.places['tunnel_0_0']
          >>> bodyguard = BodyguardAnt()
          >>> place.add_insect(test_ant)
          >>> place.add_insect(bodyguard)
          >>> place.ant.action(gamestate)
          >>> place.ant.contained_ant.armor
          9001
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing single BodyguardAnt cannot hold two other ants
          >>> bodyguard = BodyguardAnt()
          >>> first_ant = ThrowerAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> place.add_insect(bodyguard)
          >>> place.add_insect(first_ant)
          >>> second_ant = ThrowerAnt()
          >>> place.add_insect(second_ant)
          Traceback (most recent call last):
          ...
          AssertionError: Two ants in tunnel_0_0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing BodyguardAnt cannot hold another BodyguardAnt
          >>> bodyguard1 = BodyguardAnt()
          >>> bodyguard2 = BodyguardAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> place.add_insect(bodyguard1)
          >>> place.add_insect(bodyguard2)
          Traceback (most recent call last):
          ...
          AssertionError: Two ants in tunnel_0_0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing BodyguardAnt takes all the damage
          >>> thrower = ThrowerAnt()
          >>> bodyguard = BodyguardAnt()
          >>> bee = Bee(1)
          >>> place = gamestate.places['tunnel_0_0']
          >>> place.add_insect(thrower)
          >>> place.add_insect(bodyguard)
          >>> place.add_insect(bee)
          >>> bodyguard.armor
          2
          >>> bee.action(gamestate)
          >>> (bodyguard.armor, thrower.armor)
          (1, 1)
          >>> bee.action(gamestate)
          >>> (bodyguard.armor, thrower.armor)
          (0, 1)
          >>> bodyguard.place is None
          True
          >>> place.ant is thrower
          True
          >>> bee.action(gamestate)
          >>> thrower.armor
          0
          >>> place.ant is None
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
          >>> place = gamestate.places["tunnel_0_0"]
          >>> bee = Bee(3)
          >>> bodyguard = BodyguardAnt()
          >>> ant = ThrowerAnt()
          >>> place.add_insect(bee)
          >>> place.add_insect(ant)
          >>> place.add_insect(bodyguard)
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
      >>> beehive, layout = Hive(AssaultPlan()), dry_layout
      >>> gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))
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
          >>> BodyguardAnt.implemented
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
