class ZDD(object):
	def __init__(self, root=None, LO=None, HI=None):
		self.root = root
		self.LO = LO
		self.HI = HI

#constructs a ZDD given the family F
#code motivated by procedure described @ https://crypto.stanford.edu/pbc/notes/zdd/construction.html
def constructZDD(F):
	assert type(F) == type(set())
	TRUE = ZDD('TRUE', None, None)
	FALSE = ZDD('FALSE', None, None)
	if not F:
		return FALSE
	elif len(F) == 1 and next(iter(F)) == frozenset(): 
		return TRUE

	smallestElem = float('inf')

	for s in F:
		for elem in s:
			if elem < smallestElem:
				smallestElem = elem
	LOFamily = {s for s in F if not smallestElem in s}
	LO = constructZDD(LOFamily)
	HIFamily = {s - set([smallestElem]) for s in F if smallestElem in s}
	HI = constructZDD(HIFamily)
	return ZDD(smallestElem, LO, HI)

def getZDDFamily(v):
	if v.root == 'FALSE':
		return set()
	elif v.root == 'TRUE':
		return set([frozenset()])
	else:
		v0 = v.LO
		v1 = v.HI 
		F0 = getZDDFamily(v0)
		F1 = getZDDFamily(v1)
		BigU = set()
		for alpha in F1:
			BigU.add(alpha | frozenset([v.root]))
		return F0 | BigU

def test():
	zdd1 = constructZDD(set([frozenset([2])]))
	print getZDDFamily(zdd1)
	zdd2 = constructZDD(set([frozenset([2, 3, 4, 5]), frozenset([1, 6, 7]), frozenset([1, 2, 3, 4, 5, 6])]))
	print getZDDFamily(zdd2)
	zdd3 = constructZDD(set([frozenset([1,2,24,25,26]), frozenset([1,3,24,25,26]), frozenset([3,4,5])]))
	print getZDDFamily(zdd3)

test()

