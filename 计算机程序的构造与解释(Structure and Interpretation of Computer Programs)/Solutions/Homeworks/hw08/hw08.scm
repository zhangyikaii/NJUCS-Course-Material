
; Problem 1
(define-macro (list-of map-expr for var in lst if filter-expr)
  `(map 
    (lambda (,var) ,map-expr) 
    (filter (lambda (,var) ,filter-expr) ,lst)
  )
)

; Problem 2
(define (map-stream f s)
  (if (null? s)
    nil
    (cons-stream (f (car s)) (map-stream f (cdr-stream s)))))

(define multiples-of-three
  (cons-stream 3 (map-stream (lambda (x) (+ x 3)) multiples-of-three))
)

; Problem 3
(define (read_same s s0 cnt)
  (if (null? s)
    (list s0 cnt)
    (if (eq? (car s) s0)
      (read_same (cdr-stream s) s0 (+ cnt 1))
      (list s0 cnt))))

(define (next_diff s s0)
  (if (null? s)
    nil
    (if (eq? (car s) s0)
      (next_diff (cdr-stream s) s0)
      s)))

(define (rle s)
  (if (null? s)
    nil
    (cons-stream (read_same s (car s) 0) (rle (next_diff s (car s))))))
