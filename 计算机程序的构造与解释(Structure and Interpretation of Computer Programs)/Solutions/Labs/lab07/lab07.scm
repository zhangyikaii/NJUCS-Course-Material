
(define (over-or-under a b)
  (cond 
    ((< a b) -1)
    ((= a b) 0)
    (else    1)))


(define (filter-lst fn lst)
  (cond 
    ((null? lst)
     nil)
    ((fn (car lst))
     (cons (car lst) (filter-lst fn (cdr lst))))
    (else
     (filter-lst fn (cdr lst)))))


(define (make-adder n)
  (lambda (k) (+ n k)))


(define (no-repeats s)
  (if (null? s)
    nil
    (cons (car s)
      (no-repeats
      (filter-lst 
        (lambda (x) (not (eq? x (car s))))
        (cdr s))))))


(define (substitute s old new)
  (if (null? s)
    nil
    (cons 
      (cond 
        ((pair? (car s))   
         (substitute (car s) old new))
        ((eq? (car s) old) 
         new)
        (else
         (car s)))
      (substitute (cdr s) old new))))


(define (sub-all s olds news)
  (if (null? olds)
    s
    (sub-all (substitute s (car olds) (car news))
      (cdr olds)
      (cdr news))))
