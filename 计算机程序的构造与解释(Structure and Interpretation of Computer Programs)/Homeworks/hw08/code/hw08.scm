
; Problem 1
(define-macro (list-of map-expr for var in lst if filter-expr)
    `(map (lambda (,var) ,map-expr) (filter (lambda (,var) ,filter-expr) ,lst))
)

; Problem 2
(define (map-stream f s)
    (if (null? s)
    	nil
    	(cons-stream (f (car s)) (map-stream f (cdr-stream s)))))

(define multiples-of-three
  (cons-stream 3 (map-stream (lambda (x) (+ 3 x)) multiples-of-three))
)

; Problem 3
(define (rle s)
  (define (counter s num)
    (if (null? (cdr-stream s)) num
    (if (eq? (car s) (car (cdr-stream s)))
    (counter (cdr-stream s) (+ 1 num))
    num
    )
    )
  )
  (define (cutter s)
  (if (null? (cdr-stream s)) nil
  (if (eq? (car s) (car (cdr-stream s)))
    (cutter (cdr-stream s))
    (cdr-stream s)
  )
  )
  )
  (if (null? s)
    s
    (cons-stream (list (car s) (counter s 1)) (rle (cutter s)))
  )
)
