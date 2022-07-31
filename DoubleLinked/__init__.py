#!/usr/bin/env python3

'''
Double Linked List for Python3 (not threadsafe)

We have tuples, lists and dequeue.  They are efficient, but not O(1) if you must insert/delete in the middle.

This here is:

- O(1) Add items at the beginning and the end
- O(1) Remove items anywhere in the list, provided you have the item
- O(1) Add items before or after any other item
- O(1) Get next or previous item
- O(1) Iterate to the first item of an iterator
- O(1) Iterate to the next item of an iterator

But:

- O(n) to randomly access items

Note that random access probably can be imroved to O(ld n) with some tweaking on top of this implementation.

This Works is placed under the terms of the Copyright Less License,
see file COPYRIGHT.CLL.  USE AT OWN RISK, ABSOLUTELY NO WARRANTY.
'''

debug = None

def DEBUG(enable=True):
	global debug

	if enable is False:
		debug	= lambda *a,**kw: None
		return debug

	if enable is True:
		enable	= lambda *s: print(' '.join(s), flush=True)

	import Data
	_	= Data.Object(N=0,S={})

	def out(*a):
		b=[]
		for x in a:
			s	= str(x)
			t	= s.replace('<', '').replace(' object at ', ' ')
			if s != t:
				if t not in _.S:
					_.N += 1
					_.S[t] = f"{{{t.split(' ',1)[0]}{_.N}}}"
				t=_.S[t]
			b.append(t.center(22))
		enable(*b)

	debug = out
	return debug

DEBUG(False)

class Iter:
	def __init__(self, pos, reverse):
		self.__p	= pos
		self.__r	= reverse

	def __next__(self):
		ret		= self.__p
		if ret is None:
			raise StopIteration
		self.__p	= self._advance(ret)
		return ret

	def set(self, p):
		'set the iterator position to another element'
		self.__p	= p

	def is_reverse(self):
		'True if it is reverse direction'
		return self.__r

	def is_forward(self):
		'True if it is forward direction'
		return not self.__r


class AnyIter(Iter):
	'''
	Iterate list in any direction
	'''
	def __init__(self, pos, reverse=False):
		super().__init__(pos, reverse)
		self.__r	= reverse and True or False

	def _advance(self, p):
		return p.prev() if self.__r else p.next()

	def turn(self):
		'''
		turn the direction

		This does not affect the next() element.
		Call .turn().next() to do a turn in-place (this might call StopIteration)
		'''
		self.__r	= not self.__r
		return self

	def forward(self):
		'''
		Set forward direction

		This does not affect the next() element.
		'''
		self.__r	= False
		return self

	def reverse(self):
		'''
		Set backward direction

		This does not affect the next() element.
		'''
		self.__r	= True
		return self

class PrevIter(Iter):
	'''
	Iterate list in prev direction
	'''
	def __init__(self, pos):
		super().__init__(pos, True)

	def _advance(self, p):
		return p.prev()

class NextIter(Iter):
	'''
	Iterate list in next direction
	'''
	def __init__(self, pos):
		super().__init__(pos, False)

	def _advance(self, p):
		return p.next()

class Generator:
	'''
	Iterate list (generator)
	'''
	def __init__(self, klass, *a, **k):
		self.__c	= klass
		self.__a	= a
		self.__k	= k

	def __iter__(self):
		return self.__c(*self.__a, **self.__k)

class AnyGenerator(Generator):
	'''
	Iterate list in any direction (generator)
	'''
	def __init__(self, *a, **k):
		super().__init__(AnyIter, *a, **k)

class PrevGenerator(Generator):
	'''
	Iterate list in prev direction (generator)
	'''
	def __init__(self, *a, **k):
		super().__init__(PrevIter, *a, **k)

class NextGenerator(Generator):
	'''
	Iterate list in next direction (generator)
	'''
	def __init__(self, *a, **k):
		super().__init__(NextIter, *a, **k)

class Item:
	'''
	A list item
	'''
	def debug(self, c):
		debug(self.__l, c, self, self.__p, self.__n, self.__v)

	def __init__(self, v=None, _l=None):
		self.__l	= _l		# list __l.__l === list
		self.__v	= v		# val  __l.__v === item count
		self.__p	= None		# prev __l.__p === list tail
		self.__n	= None		# next __l.__n === list head

	def get(self):
		'get item value'
		return self.__v

	def set(self, v):
		'set item value'
		self.__v	= v
		return self

	def list(self):
		'return the list'
		return self.__l

	def prev(self):
		'get previous item'
		return self.__p
	def next(self):
		'get next item'
		return self.__n

	def before(self, item):
		'put this item before the given item'
		self.remove()

		self.__l			= item.__l
		self.__l._head().__v	+= 1
#		print('b', self.__l._head().__v)

		self.__p			= item.__p
		self.__n			= item
		(self.__p or self.__l).__n	= self
		item.__p			= self

		self.debug('<')
		return self

	def after(self, item):
		'put this item after the given item'
		item.debug(':')

		self.remove()

		self.__l			= item.__l
		self.__l._head().__v		+= 1
#		print('a', self.__l._head().__v)

		self.__p			= item
		self.__n			= item.__n
		(self.__n or self.__l).__p	= self
		item.__n			= self

		self.debug('>')
		item.debug('=')
		return self

	def remove(self):
		'remove item from list.  You can add it again later'
		self.debug('x')
		if self.__l is not None:
			self.__l._head().__v	-= 1
			# Do not optimize, as this is called for self.__l, too!
			p			= self.__p
			n			= self.__n
			(n or self.__l).__p	= p
			(p or self.__l).__n	= n
			self.__p		= None
			self.__n		= None
		self.__l	= None
		return self

	def destroy(self):
		'destroy item (freeing memory), returns value like .get()'
		self.remove()
		self.__l	= None
		v		= self.__v
		self.__v	= None
		return v

	def _before(self, item):
		item.debug('h')
		self.before(item)
		if item.__n is None:
			item.__n	= self
		self.__n	= None
		item.debug('H')
		return self

	def _after(self, item):
		item.debug('h')
		self.after(item)
		if item.__p is None:
			item.__p	= self
		self.__p	= None
		item.debug('H')
		return self

	def _validate(self, verbose=None):
		verbose	= (lambda i,c: i is not None and i.debug(c)) if verbose is True else (verbose or (lambda x: None))
		p	= self
		l	= None
		cnt	= 0
		verbose(self, cnt)
		while p.__n:
			n	= p.__n
			cnt += 1
			verbose(n, cnt)
			assert n.__p is l
			assert n.__l is self.__l
			p	= n
			l	= n
		verbose(l, -1)
		assert self.__p is l

	def __iter__(self):
		'iterate next, starting with the current element'
		return NextIter(self)

	def __reversed__(self):
		'iterate prev, starting with the current element'
		return PrevGenerator(self)

	def any(self, reverse=False):
		'iterate any, starting with the current element'
		return AnyGenerator(self, reverse)

class List:
	def __init__(self):
		self.__i	= Item(0, _l=self)

	def __len__(self):
		return self.__i.get()

	def destroy(self):
		'O(1) destroy the list (and free memory)'
		self.__i.set(None)
		self.__i	= None

	def first(self):	return self.__i.next()
	def last(self):		return self.__i.prev()
	def _head(self):	return self.__i

	def __iter__(self):
		return NextIter(self.__i.next())

	def __reversed__(self):
		return PrevGenerator(self.__i.prev())

	def any(self, reverse=False):
		return AnyGenerator(self.__i.prev() if reverse else self.__i.next(), reverse)

	def push(self, v):
		'push a value to the end of list, return Item'
		return Item(v)._before(self.__i)

	def pop(self, v):
		'pop a value from the end of list'
		i	= self.last()
		return i.destroy() if i is not None else None

	def unshift(self, i):
		'push a value to the head of list, return Item'
		return Item(v)._after(self.__i)

	def shift(self, i):
		'pop a value from the head of list'
		i	= self.first()
		return i.destroy() if i is not None else None

	def _validate(self, verbose=False):
		self.__i._validate(verbose)

def main():
	x	= List()
	assert 0 == len(x), len(x)
	x._validate(True)

	x.push('hello')
	assert 1 == len(x), len(x)
	x._validate(True)

	x.push(' ')
	assert 2 == len(x)
	x._validate(True)

	x.push('world')
	assert 3 == len(x)
	x._validate(True)

	v	= []
	for a in x:
		assert x is a.list()
		v.append(a.get())
	assert ['hello',' ','world'] == v

	x.first().next().remove()
	assert 2 == len(x)
	x._validate(True)

	v	= []
	for a in x:
		assert x is a.list()
		v.append(a.get())
	assert ['hello','world'] == v

	v	= []
	for a in reversed(x):
		assert x is a.list()
		v.append(a.get())
	assert ['world','hello'] == v

if __name__ == '__main__':
	main()

