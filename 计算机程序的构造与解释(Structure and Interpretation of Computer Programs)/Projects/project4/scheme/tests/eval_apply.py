test = {
  'name': 'Understanding scheme.py',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'answer': '894f36490989bdbb7f0e397e9c74a9da',
          'choices': [
            'Call expressions and special forms',
            'Only call expressions',
            'Only special forms',
            'All expressions are represented as Pairs'
          ],
          'hidden': False,
          'locked': True,
          'question': 'What types of expressions are represented as Pairs?'
        },
        {
          'answer': 'f9007bdc473e42efc27b7ee858aff42e',
          'choices': [
            'env.find(name)',
            'scheme_symbolp(expr)',
            'env.lookup(expr)',
            'SPECIAL_FORMS[first](rest, env)'
          ],
          'hidden': False,
          'locked': True,
          'question': 'What expression in the body of scheme_eval finds the value of a name?'
        },
        {
          'answer': 'be44f46671dafd5aa02dcb249280afc6',
          'choices': [
            r"""
            Check if the first element in the list is a symbol and that the
            symbol is in the dictionary SPECIAL_FORMS
            """,
            'Check if the first element in the list is a symbol',
            'Check if the expression is in the dictionary SPECIAL_FORMS'
          ],
          'hidden': False,
          'locked': True,
          'question': 'How do we know if a given combination is a special form?'
        },
        {
          'answer': '8d0ead155e250bd28be8ad8e84e92982',
          'choices': [
            r"""
            Whenever a primitive or user-defined procedure is called; we use
            the apply method in subclasses of Procedure
            """,
            r"""
            Whenever a new procedure is defined; we use the make_child_frame
            method in Frame
            """,
            r"""
            Whenever a user-defined procedure is called; we use the
            make_call_frame method of LambdaProcedure
            """,
            r"""
            Whenever a primitive or user-defined procedure is called; we use
            the make_call_frame method of LambdaProcedure
            """
          ],
          'hidden': False,
          'locked': True,
          'question': 'When and how do we create new Frames?'
        },
        {
          'answer': '25f454d6138d3e164c66ab40237676c8',
          'choices': [
            'I only',
            'II only',
            'III only',
            'I and II',
            'I and III',
            'II and III',
            'I, II and III'
          ],
          'hidden': False,
          'locked': True,
          'question': r"""
          What is the difference between applying builtins and applying user-defined procedures?
          (Choose all that apply)
          
          I.   User-defined procedures open a new frame; builtins do not
          II.  Builtins simply execute a predefined function; user-defined
               procedures must evaluate additional expressions in the body
          III. Builtins have a fixed number of arguments; user-defined procedures do not
          
          ---
          """
        },
        {
          'answer': '9257b8821d358e91004e461beaadc82b',
          'choices': [
            'SchemeError("malformed list: (1)")',
            'SchemeError("1 is not callable")',
            'AssertionError',
            'SchemeError("unknown identifier: 1")'
          ],
          'hidden': False,
          'locked': True,
          'question': 'What exception should be raised for the expression (1)?'
        }
      ],
      'scored': False,
      'type': 'concept'
    }
  ]
}
