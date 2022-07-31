#!/usr/bin/env python3

'''
Data Objects

Data.Object works like JavaScript objects.  Following creates objects with the same contents:

o = Data.Object(      k   = v)
o = Data.Object(); o['k'] = v
o = Data.Object(); o. k   = v

Data.Proxy is a generic object with needs __GET__() and __SET__() callbacks.
Data.Object is a generic object with __GET__() and __SET__() implemented in a list + dict.

Note that there is one thing:  If an array index starts with '__' and ends on `__` it is saved with an extra `_` as property.
'''

#debug = None
#
#def DEBUG(enable=True):
#	global debug
#	if enable is False:
#		debug	= lambda *a: None
#	elif enable is True:
#		debug	= lambda *a: print('DEBUG:', *a, flush=True)
#	else:
#		debug	= enable
#	return debug
#
#DEBUG(False)

class Proxy:
	def __init__(self, *a, **kw):
		for k,v in enumerate(a):
			self[k]	= v
		for k,v in kw.items():
			self[k]	= v

	def __getitem__(self, k):	return self.__GET__(k)
	def __setitem__(self, k, v):	return self.__SET__(k, v)
	def __delitem__(self, k):	return self.__DEL__(k)
	def __getattr__(self, k):	return self.__GET__(k[1:] if k.startswith('___') else k)
	def __setattr__(self, k, v):	return self.__SET__(k[1:] if k.startswith('___') else k, v)
	def __delattr__(self, k):	return self.__DEL__(k[1:] if k.startswith('___') else k)

class Object(Proxy):
	__d	= {}

	def __init__(self, *a, **kw):	super().__init__(*a, **kw)
	def __GET__(self, k):		return self.__d[k]
	def __SET__(self, k, v):	self.__d[k]	= v
	def __DEL__(self, k):		del self.__d[k]
	def __len__(self):		return len(self.__d)
	def __iter__(self):
		for k in self.__d:
			yield k

def main():
#	DEBUG(True)
	o	= Object('a','b','c', c=3, x=9, __delattr__='DEL')
	assert len(o) == 6
	assert o.___delattr__ is o['__delattr__']
	del o.___delattr__

	for a in o:	print('o', a, o[a], flush=True)
	assert len(o) == 5

	del o.c
	for a in o:	print('o', a, o[a], flush=True)
	assert len(o) == 4

	del o[1]
	for a in o:	print('o', a, o[a], flush=True)
	assert len(o) == 3

	del o.x
	for a in o:	print('o', a, o[a], flush=True)
	assert len(o) == 2

	import sys

	try:
		n = o.non
		sys.exit(1)
	except:
		pass
	assert len(o) == 2

	try:
		n = o['non']
		sys.exit(1)
	except:
		pass
	assert len(o) == 2

if __name__ == '__main__':
	main()

