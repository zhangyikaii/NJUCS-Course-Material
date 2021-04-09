(define (map func lst)
  (if (null? lst)
      nil
      (cons (func (car lst))
            (map func (cdr lst)))))

(define (filter func lst)
  (cond ((null? lst) nil)
        ((func (car lst))
         (cons (car lst)
               (filter func (cdr lst))))
        (else (filter func (cdr lst)))))

(define (reduce func lst)
  (cond ((null? lst) nil)
        ((null? (cdr lst)) (car lst))
        (else
         (reduce func
                 (cons (func (car lst) (car (cdr lst)))
                       (cdr (cdr lst)))))))

; (define-macro (cons-stream first rest)
;   `(cons ,first (delay ,rest)))

(define (cdr-stream stream)
  (force (cdr stream)))
