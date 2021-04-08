test = {
  'name': 'Problem 20 (Optional)',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (define-macro (for formal iterable body)
          ....               (list 'map (list 'lambda (list formal) body) iterable))
          for
          scm> (for i '(1 2 3)
          ....      (if (= i 1)
          ....          0
          ....          i))
          (0 2 3)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (cadr s) (car (cdr s)))
          cadr
          scm> (define (cars s) (map car s))
          cars
          scm> (define (cadrs s) (map cadr s))
          cadrs
          scm> (define-macro (leet bindings expr)
          ....               (cons (list 'lambda (cars bindings) expr)
          ....                     (cadrs bindings)))
          leet
          scm> (define (square x) (* x x))
          square
          scm> (define (hyp a b)
          ....         (leet ((a2 (square a)) (b2 (square b))) (sqrt (+ a2 b2))))
          hyp
          scm> (hyp 3 4)
          5.0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define-macro wat?)
          SchemeError
          scm> (define-macro woah okay)
          SchemeError
          scm> (define-macro (hello world))
          SchemeError
          scm> (define-macro (5) (list 1 2))
          SchemeError
          scm> (define-macro (name) (body))
          name
          scm> name
          (lambda () (body))
          scm> (name)
          SchemeError
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      scm> (define (map f lst)
      ....         (if (null? lst)
      ....             nil
      ....             (cons (f (car lst)) (map f (cdr lst)))))
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
