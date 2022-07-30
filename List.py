#

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
'''

class Iter:
	pass

class IterAny(Iter):
	'''
	Iterate list in any direction
	'''
	def __init__(self, pos, reverse=False):
		self.__p	= pos
		self.__r	= reverse and True or False

	def __next__(self):
		ret		= self.__p
		if ret:
			ret	= ret.prev() if self.__r else ret.next()
		self.__p	= ret
		if ret:
			return ret
		raise StopIteration

	def turn(self):
		self.__r	= not self.__r
		return self

	def forward(self):
		self.__r	= False
		return self

	def reverse(self):
		self.__r	= True
		return self

	def is_reverse(self):
		return self.__r

class IterPrev(Iter):
	'''
	Iterate list in prev direction
	'''
	def __init__(self, pos):
		self.__p	= pos

	def __next__(self):
		ret		= self.__p
		if ret:
			ret	= ret.prev()
		self.__p	= ret
		if ret:
			return ret
		raise StopIteration

class IterNext(Iter):
	'''
	Iterate list in next direction
	'''
	def __init__(self, pos):
		self.__p	= pos

	def __next__(self):
		ret		= self.__p
		if ret:
			ret	= ret.next()
		self.__p	= ret
		if ret:
			return ret
		raise StopIteration

class Item:
	'''
	keep a list item
	'''
	def __init__(self, v=None, _l=None):
		self.__l	= _l		# list __l.__l == list
		self.__v	= v		# val  __l.__v == item count
		self.__p	= None		# prev __l.__p == list tail
		self.__n	= None		# next __l.__n == list head

	def get(self):
		'get item value'
		return self.__v

	def set(self, v):
		'set item value'
		self.__v	= v
		return self

	def list(self):
		'return the list'
		return self.__l.__l

	def prev(self):
		'get previous item'
		return self.__p
	def next(self):
		'get next item'
		return self.__n

	def before(self, item):
		'put this item before the given item'
		self.remove()
		item.__n			= self
		item.__p			= self.__p
		(self.__p or self.__l).__n	= item
		self.__p			= item
		self.__l.__v			+= 1
		return self

	def after(self, item):
		'put this item after the given item'
		self.remove()
		self.__l			= item.__l
		self.__l.__v			+= 1
		item.__p			= self
		item.__n			= self.__n
		(self.__n or self.__l).__p	= item
		self.__n			= item
		return self

	def remove(self):
		'remove item from list.  You can add it again later'
		if self.__l:
			# Do not optimize, as this is called for self.__l, too!
			p			= self.__p
			n			= self.__n
			self.__p		= None
			self.__n		= None
			(n or self.__l).__p	= p
			(p or self.__l).__n	= n
		self.__l	= None
		return self

	def destroy(self):
		'destroy item (freeing memory)'
		self.remove()
		self.__l	= None
		self.__v	= None

class List:
	def __init__(self):
		self.__i	= Item(0, _l=self)

	def __len__(self):
		return self.__i.get()

	def destroy(self):
		'O(1) destroy the list (and free memort)'
		self.__i.set(None)
		self.__i	= None

	def first(self):	return self.__i.next()
	def last(self):		return self.__i.prev()

	def __iter__(self):
		return IterNext(self.__i)

	def __reversed__(self):
		return IterPrev(self.__i)

	def anyiter(self, reverse=False):
		return IterAny(self.__i, reverse)

	def append(self, i):
		pass

	def prepend(self, i):
		pass

if __name__ == '__main__':
	x	= List()
	assert 0 == len(x)
	x.append(Item('hello'))
	assert 1 == len(x)
	x.append(Item('world'))
	assert 2 == len(x)
	for a in x:
		assert x == a.list()
		print(x.get())

