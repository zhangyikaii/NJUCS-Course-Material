test = {
  'name': 'lets-count',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          sqlite> SELECT * from sicp20favpets;
          dog|46
          cat|20
          tiger|17
          panda|10
          koala|8
          monkey|8
          penguin|7
          lion|6
          bear|5
          capybara|5
          sqlite> SELECT * from sicp20dog;
          dog|46
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
