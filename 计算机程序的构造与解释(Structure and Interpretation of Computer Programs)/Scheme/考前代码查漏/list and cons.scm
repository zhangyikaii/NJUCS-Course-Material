scm> (define s (cons 1 (cons 2 nil))) s scm> s (1 2) scm> (draw s) 
()21
scm> (cons 3 s) (3 1 2) scm> (draw (cons 3 s)) 
()213
scm> (cons s s) ((1 2) 1 2) 
scm> (cons 4 (cons 3 nil))
 (4 3) 
scm> (cons (cons 4 (cons 3 nil)) s) 
((4 3) 1 2) 
scm> (draw (cons (cons 4 (cons 3 nil)) s)) 
()21()34
scm> (define x (cons (cons 6 (cons 5 s)) s)) 
x 
scm> (draw x) 
()2156
scm> (list? s)
 #t 
scm> (list? ())
 #t 
scm> nil
 () 
scm> (list 1 1 4 5 1 4 1 9 1 9 8 1 0) 
(1 1 4 5 1 4 1 9 1 9 8 1 0) 
scm> (list 'h') 
ParseError: unexpected token: ) 
scm> (list "hello motherfucker") 
("hello motherfucker") 
scm> (list "hello motherfucker" 1 1 4 5 1 4) 
("hello motherfucker" 1 1 4 5 1 4) 
scm> 'a 
a 
scm> (list '(a b c d)) 
((a b c d)) 
scm> (list 'a 'b 'b 'a)
 (a b b a)
 scm> (quote a)
 a 
scm> (list 1 'a)
 (1 a) 
scm> (list 1 a) 
Traceback (most recent call last): 
0 (list 1 a) 
1 a 
Error: unknown identifier: a 
scm> '(1 2 (2 3)) (1 2 (2 3)) 
scm> '(1 2 ririsu (ririsu 1)) 
(1 2 ririsu (ririsu 1)) 
scm> (car (cdr (car (cdr '(1 (2 3) 4 ))))) 
3
scm> (cdr (cdr (car (cdr '(1 (2 3) 4 )))))
 () 
scm> (cdr (cdr (car (cdr '(a (b c) d ))))) 
() 
scm> (cdr (cdr (car (cdr '(a (b c) d1 )))))
 () 
scm> '(a (b c) d1 ) 
(a (b c) d1)
