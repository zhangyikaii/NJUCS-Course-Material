;; Scheme ;;

(define (over-or-under a b)
  (cond 
        ((< a b) -1)
        ((= a b) 0)
        ((> a b) 1)
  )
)


;;; Tests
(over-or-under 1 2)
; expect -1
(over-or-under 2 1)
; expect 1
(over-or-under 1 1)
; expect 0

(define (filter-lst fn lst)
    (cond 
        ((null? lst) lst)
        ((fn (car lst)) (cons (car lst) (filter-lst fn (cdr lst))))
        (else (filter-lst fn (cdr lst)))
    )
)

;;; Tests
(define (even? x)
  (= (modulo x 2) 0))
(filter-lst even? '(0 1 1 2 3 5 8))
; expect (0 2 8)

(define (make-adder n)
  (lambda(x) (+ x n))
)

;;; Tests
(define adder (make-adder 5))
(adder 8)
; expect 13

(define (no-repeats s)
  (define (init lst num) 
      (cond
      ((null? lst) #f)
      ((= num (car lst)) #t)
      (else (init (cdr lst) num)))
  )
  (define memory ())
  (define (helper s memory) 
    (cond
      ((null? s) s)
      ((init memory (car s)) (helper (cdr s) memory))
      (else (define memory (cons (car s) memory)) (cons (car s) (helper (cdr s) memory)))
    )
  )
  (helper s memory)
)

(define (substitute s old new)
  (cond 
  ((null? s) s)
  ((pair? (car s)) (cons (substitute (car s) old new) (substitute (cdr s) old new)))
  (else (cons (if (eq? old (car s)) new (car s)) (substitute (cdr s) old new)))
  )
)

(define (sub-all s olds news)
  (if (null? olds) s (sub-all (substitute s (car olds) (car news)) (cdr olds) (cdr news)))
)