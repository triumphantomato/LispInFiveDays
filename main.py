# a python2.7 REPL for Nielsen's lisp dialect, tiddlylisp
# https://michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/
# @triumphantomato

# This code is learning code, for the purposes of learning how to 
# parse and interpret lisp. It is *not* production code and contains
# extensive "breadcrumb" comments to capture learnings.

import traceback

def repl(prompt='tiddlylisp> '):
	"A repl"
	while True:
		try:
			val = eval(parse(raw_input(prompt)))
			if val is not None: print to_string(val)
		except KeyboardInterrupt:
			print "\nExiting tiddlylisp\n"
			sys.exit()
		except:
			handle_error()

def handle_error():
	"""
	Simple error handling for both the repl and load.
	"""
	print "An error occurred. Here's the Python stack trace:\n"
	traceback.print_exc()

Symbol = str

def parse(s):
	"Parse a Lisp expression from a string."
	return read_from(tokenize(s))

def tokenize(s):
	"Convert a string s into a list of tokens."
	# print(s.replace('(',' ( ').replace(')',' ) ').split())
	return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from(tokens):
	"Read an expression from a sequence of tokens."
	#print("in read_from()") #debug
	#print(tokens) #debug
	if len(tokens) == 0:
		raise SyntaxError('unexpected EOF while reading')
	token = tokens.pop(0)
	#print(token) #debug
	if '(' == token:
		L = []
		while tokens[0] != ')':
			L.append(read_from(tokens))
		tokens.pop(0) # pop off ')'
		#print(L) #debug
		return L
	elif ')' == token:
		raise SyntaxError('unexpected )')
	else: 
		return atom(token)

def atom(token):
	"Numbers become ints or floats; every other token is a symbol."
	try: return int(token)
	except ValueError:
		try: return float(token)
		except ValueError:
			return Symbol(token)

isa = isinstance

def to_string(exp):
	"Convert a Python object back into a Lisp-readable string."
	if not isa(exp, list):
		return str(exp)
	else:
		return ('('+' '.join(map(to_string, exp))+')') 
'''
# it's a bit of a brain bender how to_string calls itself to
# undo the parsing and yield back a valid Lisp expression
# i think what's happening is that first to_string decides
# whether it has a list. If no, then just give me str(exp).
# If yes, then we need to unpack the list. 
# Consider ["*", ["+", 7, 12]] as your parsed list, which
# you now want to unparse with to_string - work through it
# and you'll see it works.

It's helpful to know that map(func, iterable) iterates over each
item in iterable and applies func to it. Since to_string is 
recursive and base case is a stringified singleton this works out.
'''

class Env(dict):
	"An environmenet: a dict of {'var':val} pairs, with an outer Env."

	def __init__(self, params=(), args=(), outer=None):
		self.update(zip(params, args))
		self.outer = outer

	def find(self, var):
		"Find the innermost Env where var appears."
		return self if var in self else self.outer.find(var)

def add_globals(env):
	"Add built-in procedures and variables to the environment."
	import operator
	import math
	def add(*args):
		sum = 0
		for item in args:
			sum += item
		return sum
	env.update(
		{'+': add,
		'-': operator.sub,
		'*': operator.mul,
		'/': operator.div,
		'>': operator.gt,
		'<': operator.lt,
		'>=': operator.ge,
		'<=': operator.le,
		'=': operator.eq,
		'sqrt': math.sqrt
		})
	env.update({'True': True, 'False': False})

	return env

global_env = add_globals(Env())

def eval(x, env=global_env):
	"Evaluate an expression in an environment."
	# print("in eval") #debug
	if isa(x, Symbol): # variable reference 
		# print("am in Symbol") #debug
		return env.find(x)[x]
	elif not isa(x, list): # literal constant (like an int)
		return x
	elif x[0] == 'quote' or x[0] == 'q':  #(quote exp) or (q exp)
		(_, exp) = x
		return exp
	elif x[0] == 'atom?': # (atom? exp)
		(_, exp) = x
		return not isa(eval(exp, env), list)
	elif x[0] == 'eq?': # (eq? exp1 exp2)
		(_, exp1, exp2) = x
		v1, v2 = eval(exp1, env), eval(exp2, env)
		return (not isa(v1, list)) and (v1 == v2)
	elif x[0] == 'car':
		(_, exp) = x
		return eval(exp, env)[0]
	elif x[0] == 'cdr':
		(_, exp) = x
		return eval(exp, env)[1:]
	elif x[0] == 'cons':
		(_, exp1, exp2) = x
		return [eval(exp1, env)] + eval(exp2, env)
	elif x[0] == 'cond': # (cond (p1 e1) ... (pn en))
		for (p, e) in x[1:]:
			if eval(p, env):
				return eval(e, env)
	elif x[0] == 'null?': 
		(_, exp) = x
		return eval(exp, env) == []
	elif x[0] == 'if': # (if test conseq alt)
		(_, test, conseq, alt) = x
		if eval(test, env):
			return eval(conseq, env)
		return eval(alt, env)
		# nielsen does it this way:
		# return eval((conseq if eval(test, env) else alt), env)
	elif x[0] == 'set!': # (set! var exp)
		(_, var, exp) = x
		env.find(var)[var] = eval(exp, env)
	elif x[0] == 'define': # (define var exp)
		(_, var, exp) = x
		env[var] = eval(exp, env)
	elif x[0] == 'lambda': # (lambda (var*) exp)
		'''
		my attempt:
		(_, *args, exp) = x
		for arg in *args:
			env[arg[0]] = eval(arg[1], env) # this is wrong
			# b/c you're adding to the existing env, instead
			# of creating a new Env that is sub-nested w/i current env
		return eval(exp, env)
		'''
		(_, vars, exp) = x
		return lambda *args: eval(exp, Env(vars, args, env))
		'''
		this line is genius. it creates an anonymous *python*
		lambda function that takes a variable number of arguments
		as *args. the definition of this python function is the
		evaluation of the procedure definition from the anonymous 
		Lisp lambda expression.

		to evaluate this it takes the Lisp lambda procedure definition
		and passes it to eval() along with creating a *new* 
		sub-environment that is nested within the *current* environment
		as its outer environment

		additionally, this new sub-environment is updated upon
		initialization with the dict [key]:[value] pairs of vars
		that were declared in the original Lisp expression as the keys
		and the input-supplied args as the values!

		this was _so_ tricky to reason about because of the mixing of 
		python and Lisp! at times we're thinking about parts of a Lisp
		expression (exp) and at times we're thinking about inputs that
		are being handled by python functions (args)
		'''
	elif x[0] == 'begin': # (begin exp*)
		for exp in x[1:]:
			val = eval(exp, env)
		return val

	else: 				# (proc exp*)
		exps = [eval(exp, env) for exp in x]
		proc = exps.pop(0) # get the procedure - should match
						   # a defined proc, e.g. from global_env

		return proc(*exps) # call the python proc on the expanded
						   # args

import sys

def load(filename):
	'''
	Load the tiddylisp program in filename, execute it, and start the
	repl. If an error occurs, execution stops, and we are left in the
	repl. The function load copes with multi-line tiddlylisp code by
	merging lines until the number of opening and closing parens
	match.
	'''
	print("Loading and executing")
	f = open(filename, 'r')
	program = f.readlines()
	f.close()
	rps = running_paren_sums(program)
	full_line = ''
	for (paren_sum, program_line) in zip(rps, program):
		program_line = program_line.strip()
		full_line += program_line + " "
		if paren_sum == 0 and full_line.strip() != '':
			try:
				val = eval(parse(full_line))
				if val is not None: print_to_string(val)
			except:
				handle_error()
				print("\nThe line in which the error occurred:\n")
				break
			full_line = ''
		repl()

def running_paren_sums(program):
	'''
	Map the lines in the list program to a list whose entries contain
	a running sum of the per-line difference between the number of '('
	parentheses and the number of ')' parentheses.
	'''
	count_net_parens = lambda line: line.count('(') - line.count(')')
	paren_counts = map(count_net_parens, program)
	rps = []
	total = 0
	for paren_count in paren_counts:
		total += paren_count
		rps.append(total)
	return rps

if __name__ == "__main__":
	if len(sys.argv) > 1:
		load(sys.argv[1])
	else:
		repl()


