test = {
  'name': 'matchmaker',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          sqlite> SELECT * FROM matchmaker LIMIT 10;
          owl|Clair De Lune|silver/grey|dark green
          tiger|Clair De Lune|green|blue
          tiger|Clair De Lune|green|green
          tiger|Clair De Lune|green|blue
          puppy|Clair De Lune|dark blue|red
          puppy|Clair De Lune|dark blue|blue
          tiger|All I want for Christmas|violet|blue
          puppy|Clair De Lune|red|blue
          cat|Clair De Lune|pink|orange
          cat|Clair De Lune|pink|amber
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'ordered': False,
      'scored': True,
      'setup': r"""
      sqlite> .read lab09.sql
      """,
      'teardown': '',
      'type': 'sqlite'
    }
  ]
}
