test = {
  'name': 'Prologue - Expr',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'answer': 'literal, name, call expression, lambda expression',
          'choices': [
            'literal, name, call expression, lambda expression',
            'number, lambda function, primitive function, string',
            'value, expression, function, number',
            'name, function, number, literal'
          ],
          'hidden': False,
          'locked': False,
          'question': 'What are all the types of expressions in PyCombinator?'
        },
        {
          'answer': 'number, lambda function, primitive function',
          'choices': [
            'number, lambda function, primitive function',
            'number, string, function',
            'name, number, lambda function',
            'number, lambda expression, primitive function'
          ],
          'hidden': False,
          'locked': False,
          'question': 'What are all the types of values in PyCombinator?'
        },
        {
          'answer': 'a Number',
          'choices': [
            'a Number',
            'a String',
            'a Function',
            'an Expression'
          ],
          'hidden': False,
          'locked': False,
          'question': 'What does a Literal evaluate to?'
        },
        {
          'answer': 'A lambda function is the result of evaluating a lambda expression',
          'choices': [
            'They are the same thing',
            'A lambda expression is the result of evaluating a lambda function',
            'A lambda function is the result of evaluating a lambda expression',
            'A lambda expression is a call to a lambda function'
          ],
          'hidden': False,
          'locked': False,
          'question': 'What is the difference between a lambda expression and a lambda function?'
        },
        {
          'answer': 'A method of Expr objects that evaluates the Expr and returns a Value',
          'choices': [
            'A method of Expr objects that evaluates the Expr and returns a Value',
            'A method of Expr objects that evaluates a call expression and returns a Number',
            'A method of LambdaExpression objects that evaluates a function call',
            'A method of Literal objects that returns a Name'
          ],
          'hidden': False,
          'locked': False,
          'question': 'Which of the following describes the eval method?'
        },
        {
          'answer': 'As dictionaries that map variable names (strings) to Value objects',
          'choices': [
            'As dictionaries that map variable names (strings) to Value objects',
            'As sequences of Frame objects',
            'As dictionaries that map Name objects to Value objects',
            'As linked lists containing dictionaries'
          ],
          'hidden': False,
          'locked': False,
          'question': 'How are environments represented in our interpreter?'
        }
      ],
      'scored': False,
      'type': 'concept'
    }
  ]
}
