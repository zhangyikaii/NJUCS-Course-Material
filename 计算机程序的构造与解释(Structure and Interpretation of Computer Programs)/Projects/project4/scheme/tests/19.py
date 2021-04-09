test = {
  'name': 'Problem 19 (Optional)',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (define (sum n total)
          ....   (if (zero? n)
          ....       total
          ....       (sum (- n 1) (+ n total))))
          sum
          scm> (sum 1001 0)
          501501
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (sum n total)
          ....   (if (zero? n)
          ....       total
          ....       (if #f 42 (sum (- n 1) (+ n total)))))
          sum
          scm> (sum 1001 0)
          501501
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (sum n total)
          ....   (cond ((zero? n) total)
          ....         ((zero? 0) (sum (- n 1) (+ n total)))
          ....         (else 42)))
          sum
          scm> (sum 1001 0)
          501501
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (sum n total)
          ....   (if (zero? n)
          ....       total
          ....       (add n (+ n total))))
          sum
          scm> (define add (lambda (x+1 y) (sum (- x+1 1) y)))
          add
          scm> (sum 1001 0)
          501501
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (sum n total)
          ....   (if (zero? n)
          ....       total
          ....       (let ((n-1 (- n 1)))
          ....            (sum n-1 (+ n total)))))
          sum
          scm> (sum 1001 0)
          501501
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (sum n total)
          ....   (or (and (zero? n) total)
          ....       (add n (+ n total))))
          sum
          scm> (define add (lambda (x+1 y) (sum (- x+1 1) y)))
          add
          scm> (sum 1001 0)
          501501
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (sum n total)
          ....   (define add (lambda (x+1 y) (sum (- x+1 1) y)))
          ....   (or (and (zero? n) total)
          ....       (add n (+ n total))))
          sum
          scm> (sum 1001 0)
          501501
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          scm> (define (sum n total)
          ....   (begin
          ....      (define add (lambda (x+1 y) (sum (- x+1 1) y)))
          ....      (or (and (zero? n) total)
          ....          (add n (+ n total)))))
          sum
          scm> (sum 1001 0)
          501501
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
