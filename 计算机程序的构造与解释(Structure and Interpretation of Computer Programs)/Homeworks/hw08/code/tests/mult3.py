test = {
  'name': 'mult3',
  'points': 100,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (car multiples-of-three)
          3
          scm> (list? (cdr multiples-of-three)) ; Check to make sure variable contains a stream
          #f
          scm> (list? (cdr (cdr-stream multiples-of-three))) ; Check to make sure rest of stream is a stream
          #f
          scm> (equal? (first-k multiples-of-three 5) '(3 6 9 12 15))
          #t
          scm> (equal? (first-k multiples-of-three 10) '(3 6 9 12 15 18 21 24 27 30))
          #t
          scm> (length (first-k multiples-of-three 100))
          100
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      scm> (load 'hw08)
      scm> (define (first-k s k) (if (or (null? s) (= k 0)) nil (cons (car s) (first-k (cdr-stream s) (- k 1)))))
      scm> (define (length lst) (if (null? lst) 0 (+ 1 (length (cdr lst)))))
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
