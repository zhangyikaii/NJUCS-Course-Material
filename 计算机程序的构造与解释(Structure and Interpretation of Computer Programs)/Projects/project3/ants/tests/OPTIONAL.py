test = {
  'name': 'Problem OPTIONAL',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing status parameters
          >>> slow = SlowThrower()
          >>> scary = ScaryThrower()
          >>> SlowThrower.food_cost
          c9452203eb0b0f0bd2454586a6c2fc5c
          # locked
          >>> ScaryThrower.food_cost
          50ae32be3e31df6c59633df7fdfb3a72
          # locked
          >>> slow.armor
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> scary.armor
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> # Testing Slow
          >>> slow = SlowThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(slow)
          >>> gamestate.places["tunnel_0_4"].add_insect(bee)
          >>> slow.action(gamestate)
          >>> gamestate.time = 1
          >>> bee.action(gamestate)
          >>> bee.place.name # SlowThrower should cause slowness on odd turns
          040b6ad98a7360eba8d493c250a9b82e
          # locked
          >>> gamestate.time += 1
          >>> bee.action(gamestate)
          >>> bee.place.name # SlowThrower should cause slowness on odd turns
          8344c19df8015306b462119efc8419cb
          # locked
          >>> for _ in range(3):
          ...    gamestate.time += 1
          ...    bee.action(gamestate)
          >>> bee.place.name
          7f44338412808161209e944b1ee0f78c
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> # Testing Scare
          >>> scary = ScaryThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(scary)
          >>> gamestate.places["tunnel_0_4"].add_insect(bee)
          >>> scary.action(gamestate)
          >>> bee.action(gamestate)
          >>> bee.place.name # ScaryThrower should scare for two turns
          46f9851313dc368f747e69f1670450da
          # locked
          >>> bee.action(gamestate)
          >>> bee.place.name # ScaryThrower should scare for two turns
          32a5320f2c5021a9b66582af8b364dc7
          # locked
          >>> bee.action(gamestate)
          >>> bee.place.name
          46f9851313dc368f747e69f1670450da
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> # Scary stings an ant
          >>> scary = ScaryThrower()
          >>> harvester = HarvesterAnt()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(scary)
          >>> gamestate.places["tunnel_0_4"].add_insect(bee)
          >>> gamestate.places["tunnel_0_5"].add_insect(harvester)
          >>> scary.action(gamestate)
          >>> bee.action(gamestate)
          >>> bee.place.name # ScaryThrower should scare for two turns
          46f9851313dc368f747e69f1670450da
          # locked
          >>> harvester.armor
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> bee.action(gamestate)
          >>> harvester.armor
          73b94a1326ae2e803c3421016112207b
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> # Testing if effects stack
          >>> slow = SlowThrower()
          >>> bee = Bee(3)
          >>> slow_place = gamestate.places["tunnel_0_0"]
          >>> bee_place = gamestate.places["tunnel_0_8"]
          >>> slow_place.add_insect(slow)
          >>> bee_place.add_insect(bee)
          >>> slow.action(gamestate)    # slow bee two times
          >>> slow.action(gamestate)
          >>> gamestate.time = 1
          >>> bee.action(gamestate) # do nothing. The outer slow has 2 turns to go, the inner one still has 3 turns
          >>> bee.place.name
          'tunnel_0_8'
          >>> gamestate.time = 2
          >>> bee.action(gamestate) # moves forward. The outer slow has 1 turn to go, the inner one has 2 turns
          >>> bee.place.name
          'tunnel_0_7'
          >>> gamestate.time = 3
          >>> bee.action(gamestate) # do nothing. The outer slow has no turns left, the inner one has 2 turns
          >>> bee.place.name
          'tunnel_0_7'
          >>> gamestate.time = 4
          >>> bee.action(gamestate) # moves forward. The inner slow has 1 turn
          >>> bee.place.name
          'tunnel_0_6'
          >>> gamestate.time = 5
          >>> bee.action(gamestate) # does nothing. The inner slow has no turns
          >>> bee.place.name
          'tunnel_0_6'
          >>> gamestate.time = 6      # slow effects have worn off
          >>> bee.action(gamestate)
          >>> bee.place.name
          'tunnel_0_5'
          >>> gamestate.time = 7      # slow effects have worn off
          >>> bee.action(gamestate)
          >>> bee.place.name
          'tunnel_0_4'
          >>> gamestate.time = 8      # slow effects have worn off
          >>> bee.action(gamestate)
          >>> bee.place.name
          'tunnel_0_3'
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing multiple scared bees
          >>> scare1 = ScaryThrower()
          >>> scare2 = ScaryThrower()
          >>> bee1 = Bee(3)
          >>> bee2 = Bee(3)
          
          >>> gamestate.places["tunnel_0_0"].add_insect(scare1)
          >>> gamestate.places["tunnel_0_1"].add_insect(bee1)
          >>> gamestate.places["tunnel_0_4"].add_insect(scare2)
          >>> gamestate.places["tunnel_0_5"].add_insect(bee2)
          
          >>> scare1.action(gamestate)
          >>> scare2.action(gamestate)
          >>> bee1.action(gamestate)
          >>> bee2.action(gamestate)
          
          >>> bee1.place.name
          'tunnel_0_2'
          >>> bee2.place.name
          'tunnel_0_6'
          
          >>> bee1.action(gamestate)
          >>> bee2.action(gamestate)
          
          >>> bee1.place.name
          'tunnel_0_3'
          >>> bee2.place.name
          'tunnel_0_7'
          
          >>> bee1.action(gamestate)
          >>> bee2.action(gamestate)
          
          >>> bee1.place.name
          'tunnel_0_2'
          >>> bee2.place.name
          'tunnel_0_6'
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> scare = ScaryThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(scare)
          >>> gamestate.places["tunnel_0_1"].add_insect(bee)
          
          >>> scare.action(gamestate)
          >>> bee.action(gamestate)
          
          >>> bee.place.name
          ba5c35f55ba3229d1eb021382d9d19c5
          # locked
          
          >>> bee.action(gamestate)
          
          >>> bee.place.name
          8344c19df8015306b462119efc8419cb
          # locked
          
          >>> #
          >>> # Same bee should not be scared more than once
          >>> scare.action(gamestate)
          >>> bee.action(gamestate)
          
          >>> bee.place.name
          ba5c35f55ba3229d1eb021382d9d19c5
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> # Testing long effect stack
          >>> scary = ScaryThrower()
          >>> slow = SlowThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(scary)
          >>> gamestate.places["tunnel_0_1"].add_insect(slow)
          >>> gamestate.places["tunnel_0_3"].add_insect(bee)
          
          >>> scary.action(gamestate) # scare bee once
          
          >>> gamestate.time = 0
          >>> bee.action(gamestate) # scared
          >>> bee.place.name
          'tunnel_0_4'
          
          >>> for _ in range(3): # slow bee three times
          ...    slow.action(gamestate)
          
          >>> gamestate.time = 1
          >>> bee.action(gamestate) # scared, but also slowed thrice
          >>> bee.place.name
          'tunnel_0_4'
          
          >>> gamestate.time = 2
          >>> bee.action(gamestate) # scared and slowed thrice
          >>> bee.place.name
          'tunnel_0_5'
          
          >>> gamestate.time = 3
          >>> bee.action(gamestate) # slowed thrice
          >>> bee.place.name
          'tunnel_0_5'
          
          >>> gamestate.time = 4
          >>> bee.action(gamestate) # slowed twice
          >>> bee.place.name
          'tunnel_0_4'
          
          >>> gamestate.time = 5
          >>> bee.action(gamestate) # slowed twice
          >>> bee.place.name
          'tunnel_0_4'
          
          >>> gamestate.time = 6
          >>> bee.action(gamestate) # slowed once
          >>> bee.place.name
          'tunnel_0_3'
          
          >>> gamestate.time = 7
          >>> bee.action(gamestate) # status effects have worn off
          >>> bee.place.name
          'tunnel_0_2'
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> scary = ScaryThrower()
          >>> slow = SlowThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(scary)
          >>> gamestate.places["tunnel_0_1"].add_insect(slow)
          >>> gamestate.places["tunnel_0_3"].add_insect(bee)
          
          >>> slow.action(gamestate) # slow bee
          >>> scary.action(gamestate) # scare bee
          
          >>> bee.place.name
          'tunnel_0_3'
          
          >>> gamestate.time = 0
          >>> bee.action(gamestate) # scared and slowed
          >>> bee.place.name
          'tunnel_0_4'
          
          >>> gamestate.time = 1
          >>> bee.action(gamestate) # scared and slowed
          >>> bee.place.name
          'tunnel_0_4'
          
          >>> gamestate.time = 2
          >>> bee.action(gamestate) # slowed
          >>> bee.place.name
          'tunnel_0_3'
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> from ants import *
          >>> ScaryThrower.implemented
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> SlowThrower.implemented
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          """,
          'hidden': False,
          'locked': True
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      >>> beehive, layout = Hive(AssaultPlan()), dry_layout
      >>> dimensions = (1, 9)
      >>> gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
