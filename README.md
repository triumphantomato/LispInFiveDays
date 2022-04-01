# Lisp in Five Days
Let's learn about Lisp!

![Screen Shot 2022-03-31 at 4 48 09 PM](https://user-images.githubusercontent.com/91909240/161167439-ccb6b9c0-dca7-4505-bd63-e383c3603c87.jpg)

### Audience
You'll get the most out of this course if you:
* Have tried a couple programming languages
* Are comfortable in python
* Haven't worked much with compilers or interpreters before

You will learn:
* How interpreters work, practically (including developing an intuition for abstract syntax trees)
* What makes Lisp special, and beautiful
* Some ways to think about programming languages

For the curious, my own attempts at implementing a basic Lisp interpeter can be found at `main.py` (in python) and `main.lisp` (in lisp), following Nielsen and Graham respectively.

---

### Day Zero - Python Refresher
**How to learn:**
1. Use the Python REPL to experiment with things, *then* check StackOverflow to confirm your understanding
2. Run the code. Type every example out and run it. Modify the examples. Once you get the hang of it, try to complete the function or write the sub-routine before looking at the example. Understand why the example is different and what you got wrong, or what different choices you made.

**Review:**
* List comprehensions
* `.zip()`
* `.map()`
* List manipulations: `.pop()`, `.strip()`, `.join()`
* The role of `_` (to ignore an input)
* Assignment operator - it assigns RH to LH, so `(_, exp) = x` where x is a list with exactly two values is legit
* The unpacking operator `*` and how `*args` works

**Exercises**

These exercises review some helpful python concepts. The learning purpose of each exercise is listed below it.

_Ex 1._ Write a python program that takes a plaintext file as a command line argument and prints its contents to screen without any spaces.
* `.strip()`
* loading an external file via command line

_Ex 2._ Write a python program to sum a variable amount of arguments together.
* `*args`

_Ex 3._ Modify your program from _Ex 1._ to split the input file's text into two lists, each containing every other word. So listOne contains all odd words (word 1, word 3, word 5...) and listTwo contains all even words. Then use zip() and join() to reprint the text file in order, two words at a time.
* `zip()`
* `join()`

_Ex 4._ Use map() to modify your program from _Ex 3._ to print each word reversed.
* `map()`

---

### Day One - LISP Intro
* Watch a talk on LISP history -  [Let's LISP like it's 1959](https://www.youtube.com/watch?v=hGY3uBHVVr4) - _Kristoffer Grönlund, 2019_
* Skim to see what's special about Lisp - [A Road to Common Lisp](https://stevelosh.com/blog/2018/08/a-road-to-common-lisp/) - _Steve Losh, 2018_
* * do enough to get `rlwrap sbcl` functioning and play around in the REPL a bit but don't invest too much time in Common Lisp tooling
* Main Text - [Lisp as the Maxwell's Equations of Software](https://michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/)- _Michael Nielsen, 2012_
	* Work until section titled: _A nontrivial example: square roots using only elementary arithmetic_

**Some questions for reading**
1. How is programming in Lisp the same or different from your favorite language? 
2. Can a program written today in `$your_language` run without edits 20 years later? Is it common for a library to be "done" and not need updates for years afterwards?
3. Who is Phyllis Fox? (See Grönlund's video on Lisp history)
4. What was Lisp invented for, and why was it not intended to be a programming language? (See again Grönlund's video)
---
### Day Two - Lisp in Python
* Main Text - [Lisp as the Maxwell's Equations of Software](https://michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/)- _Michael Nielsen, 2012_
	* Continue until section titled: _An interpreter for Lisp_
* Read about Lisp vs. C - [Worse is Better](https://www.dreamsongs.com/RiseOfWorseIsBetter.html) - _Richard Gabriel_
* Read about the death of Lisp in college curricula - [Lisp and Smalltalk are dead: It's C all the way down](https://computinged.wordpress.com/2009/08/14/lisp-and-smalltalk-are-dead-its-c-all-the-way-down/) - _Mark Guzdial, 2009_

**Some questions for reading**
1. What are the pros/cons of valuing interface simplicity over implementation cost (as in Lisp), or vice versa (as in C/UNIX)?
2. What happens to the barrier to entry to programming depending on which paradigm you value more?
---
### Day Three - Lisp in Python
* Main Text - [Lisp as the Maxwell's Equations of Software](https://michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/)- _Michael Nielsen, 2012_
	* Work through entirety of section titled _An interpreter for Lisp_
* Read about why you should learn compilers -
[Rich programmer food](http://steve-yegge.blogspot.com/2007/06/rich-programmer-food.html) - _Steve Yegge, 2007_
* Read about Lisp interpreter innards - 
[How to write a lisp interpreter in python](http://norvig.com/lispy.html) - _Peter Norvig_

**Some questions for reading**
1. Norvig - Pay special attention to syntax vs. semantics in Norvig. Don't worry if you don't understand all his code immediately.
2. Yegge - Enjoy his wit. Consider the problems he poses and their real-world applicability. Consider determinism vs. stoachsticism. Can you give examples of each approach? Which do you think will be more successful? Does it vary by field?

---
### Day Four - Lisp in Lisp:
* Bounce between the Graham and Nielsen as appropriate - Graham is a more "axiomatic" derivation of Lisp in Lisp, and is beautiful for that reason, while Nielsen does a good job explaining the semantics of `eval`.
* Read [The Roots of Lisp](https://raw.githubusercontent.com/triumphantomato/LispInFiveDays/main/paul_graham_lisp_essay.ps) (Postscript - right-click -> save as) - _Paul Graham, 2002_
* [Lisp as the Maxwell's Equations of Software](https://michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/) - _Michael Nielsen, 2012_
	* Work from section titled _Lisp in Lisp_ through end, finish tomorrow if needed

**Reading Notes:**
1. Graham - you should be well equipped to move through this text with some speed now. You can use your `rlwrap sbcl` Common Lisp environment from the Losh article to implement what you would like. - I recommend reading this before doing the Nielsen _Lisp in Lisp_ work. I find Graham's explanation clearer.

---

### Day Five - Some Beautiful Lisp:
* Read Paul Graham's [Beating the Averages](http://www.paulgraham.com/avg.html) for a fun view on Lisp as a competitive advantage, and Patrick Collison on [Stripe choosing Ruby](https://www.quora.com/Why-did-Stripe-choose-to-use-Ruby-for-its-backend-language) for some counterpoint _(N.B.: Patrick helped Paul with his latest Lisp-dialect, Bel)_
* Work through [The Y Combinator](https://mvanier.livejournal.com/2897.html) - _Mike Vanier_ - to understand footnote 3 from Graham's essay on _The Roots of Lisp_

**Reading Notes:**

Vanier - this is a beautiful text. You'll walk away understanding:
* Lazy vs. strict evaluation languages
* Weak vs. strong typing in languages
	* And how this is different from dynamic vs. static typing
* How to use the Y combinator to implement recursion without a recursive function call (to be frank, I'm still working through this myself!)

---
### Go Beyond

* Read about practical applications of the Y Combinator - [Y in Practical Programs](http://www.dsi.uniroma1.it/~labella/absMcAdam.ps) - _Bruce McAdam, 2001_ (Postscript - right-click -> save as)
* Read about how to successively grow the Lisp interpreter Graham explains into a language with practical numbers, side-effects, and sequential execution (and to understand those concepts) [The Art of the Interpreter](https://dspace.mit.edu/bitstream/handle/1721.1/6094/AIM-453.pdf) - _Guy Lewis Steele Jr. and Gerald Jay Sussman, 1978_
* Watch Compiler innards _(in Ruby)_ [*Compiler From Scratch*](https://www.destroyallsoftware.com/screencasts/catalog/a-compiler-from-scratch) - _Gary Bernhardt, 2017_
 * Build your own Lisp with this end-to-end tour _(in C)_
[BuildYourOwnLisp](http://www.buildyourownlisp.com/contents)
* Watch [Growing a Language](https://www.youtube.com/watch?v=_ahvzDzKdB0) - _Guy L Steele Jr., OOPSLA Keynote, 1998_
