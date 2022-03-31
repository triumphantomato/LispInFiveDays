;;;; Working through Graham's Roots of Lisp
;;;; http://www.paulgraham.com/rootsoflisp.html
;;;; @triumphantomato

;;;; This code is learning code, for the purposes of learning how to 
;;;; parse and interpret lisp. It is *not* production code and contains
;;;; extensive "breadcrumb" comments to capture learnings.

;; helper functions
(defun null. (x)
	(eq x '()))

(defun and. (x y)
	(cond (x (cond (y 't) ('t '())))
		('t '())))

(defun not. (x)
	(cond (x '()) ('t 't)))

(defun append. (x y)
	(cond ((null. x) y)
		('t (cons (car x) (append. (cdr x) y)))))

(defun pair. (x y)
	(cond ((and. (null. x) (null. y)) '())
		((and. (not. (atom x)) (not. (atom y)))
			(cons (list (car x) (car y))
				(pair. (cdr x) (cdr y))))))

(defun assoc. (x y)
	(cond ((eq (caar y) x) (cadar y))
		('t (assoc. x (cdr y)))))

;; interpreter

(defun eval. (e a)
	(cond
		((atom e) (assoc. e a)) ;find value of e in association list, a
		((atom (car e))
			(cond
				((eq (car e) 'quote) (cadr e)) ;quote
				((eq (car e) 'atom) (atom (eval. (cadr e) a))) ;atom
				((eq (car e) 'eq) (eq (eval. (cadr e) a) ;eq
									  (eval. (caddr e) a)))
				((eq (car e) 'car) (car (eval. (cadr e) a))) ;car
				((eq (car e) 'cdr) (cdr (eval. (cadr e) a))) ;cdr
				((eq (car e) 'cons) (cons (eval. (cadr e) a) ;cons
										  (eval. (caddr e) a)))
				((eq (car e) 'cond) (evcon. (cdr e) a)) ;cond
				; run a user-defined function
				; by fetching its value in the assoc list a
				; (this value should be a label or lambda expression)
				; and calling eval.() on it with its arguments (cdr e)
				('t (eval. (cons (assoc. (car e) a) 
								 (cdr e))
							a))))
		((eq (caar e) 'label)  ; why caar? b/c the first arg
							   ; to eval. contains both the 
							   ; labeled function *and* its
							   ; *own* arguments - so the first
							   ; car gives us the "label ...." 
							   ; function declaration
							   ; and caar gives us 'label
							   ; see footnote 1 to try it out
			(eval. (cons (caddar e) (cdr e)) ;combine lambda exp
											 ;w/ the args
					(cons (list (cadar e) (car e)) a))) 
					;push the expression name onto the
					;assoc list w/ the lambda expr
					;as its value


		((eq (caar e) 'lambda)
			(eval. (caddar e)
				   (append. (pair. (cadar e) (evlis. (cdr e) a))
				   			a)))))
			; if it's a lambda experssion
			; take the function body
			; and evaluate it against
			; the associaiton list, but first
			; update the association list to 
			; contain the pairs of (symbol, value)
			; from the formal arguments in the lambda
			; function declaration, and their passed-in
			; values (which are eval.'d in
			; evlis.) when the function was called.

			; Note that these pairs will be pushed
			; onto the top of the association list.

(defun evcon. (c a)
	(cond ((eval. (caar c) a) ;is my conditional expression true?
		   (eval. (cadar c) a)) ;then give me the return
		   ('t (evcon. (cdr c) a)))) ;else, recurse on the rest of it

(defun evlis. (m a) ; recursively eval. what's in list m and
					; cons the result to another list a
					; (a is the association list from eval.)
	(cond ((null. m) '())
		   ('t (cons (eval. (car m) a)
		   	         (evlis. (cdr m) a)))))


;;; footnotes

;; long statements to put into REPL to play with car caar etc.

;(eval. '((label firstatom (lambda (x) (cond ((atom x) x) ('t (firstatom (car x)))))) y) '((y ((a b) (c d)))))
;'(label subst (lambda (x y z) (cond ((atom z) (cond ((eq z y) x) ('t z))) ('t (cons (subst x y (car z)) (subst x y (cdr z)))))))

;; footnote 1
; (caar '((label firstatom (lambda (x) (cond ((atom x) x) ('t (firstatom (car x)))))) y))
; > label
; that's how we're checking to see if the first word is label for eval.
; if you took the cdr you'd get the arguments being passed to this 
; function as it's being called
; (cdr '((label firstatom (lambda (x) (cond ((atom x) x) ('t (firstatom (car x)))))) y))
; > (y)

;; footnote 2
; (lambda (x) (+ 1 x))
; 