import random
import time
import matplotlib.pyplot as plt
import sys
import utils
from utils import total_size
import numpy

sys.setrecursionlimit(100000)

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

def Union(A, B):
	if (not A or A.root == 'FALSE') and (not B or B.root == 'FALSE'):
		return ZDD('FALSE', None, None)
	elif (A.root == 'TRUE' and B.root == 'FALSE') or (A.root == 'FALSE' and B.root == 'TRUE'):
		return ZDD('TRUE', None, None)
	elif B.root == 'TRUE' and not A.root == 'FALSE' and not A.root == 'TRUE':
		LOestNode = A
		while LOestNode.LO != None and LOestNode.LO.root != 'TRUE':
			LOestNode = LOestNode.LO
		if not LOestNode.LO or LOestNode.LO.root != 'TRUE':
			LOestNode.LO = ZDD('TRUE', None, None)
		return A
	elif A.root == 'TRUE' and not B.root == 'FALSE' and not B.root == 'TRUE':
		LOestNode = B
		TRUE = ZDD('TRUE', None, None)
		while LOestNode.LO != None and LOestNode.LO.root != 'TRUE':
			LOestNode = LOestNode.LO
		if LOestNode.LO.root != 'TRUE':
			LOestNode.LO = ZDD('TRUE', None, None)
		return B
	elif A.root == B.root:
		return ZDD(A.root, Union(A.LO, B.LO), Union(A.HI, B.HI))
	else:
		v = A.root
		w = B.root
		if v < w:
			C = Union(A.LO, B)
			return ZDD(v, C, A.HI)
		else:
			C = Union(B.LO, A)
			return ZDD(w, C, B.HI)

def countSets(A):
	if A.root == 'FALSE':
		return 0
	elif A.root == 'TRUE':
		return 1
	return countSets(A.LO) + countSets(A.HI)

def testDictionary():
	allWords = set()
	for line in open('sgb-words.txt'):
		wordSet = set()
		word = str(line.strip())
		for index, c in enumerate(word):
			wordSet.add(index * 26 + ord(c)%32)
		wordSet = frozenset(wordSet)
		allWords.add(wordSet)
	zddDictionary = constructZDD(allWords)
	return zddDictionary

def test():
	#basic construction and representation 
	zdd1 = constructZDD(set([frozenset([2])]))
	print getZDDFamily(zdd1)
	print countSets(zdd1)
	zdd2 = constructZDD(set([frozenset([2, 3, 4, 5]), frozenset([1, 6, 7]), frozenset([1, 2, 3, 4, 5, 6])]))
	print getZDDFamily(zdd2)
	print countSets(zdd2)
	zdd3 = constructZDD(set([frozenset([1, 3, 4, 5]), frozenset([1, 6, 7]), frozenset([1, 2, 3, 4, 5, 6]), frozenset([1, 2, 3, 6]), frozenset([1, 2, 5, ]), frozenset([1, 9, 10]), frozenset([69])]))
	print getZDDFamily(zdd3)
	print countSets(zdd3)
	#code demonstrating the Union function
	'''
	zdd1 = constructZDD(set([frozenset([1, 2]), frozenset([3]), frozenset([4])])) 
	zdd2 = constructZDD(set([frozenset([1, 2]), frozenset([1, 3]), frozenset([4]), frozenset([4, 5])]))
	zdd3 = Union(zdd1, zdd2)
	print getZDDFamily(zdd3)
	'''

	#time complexity testing code
	'''
	numTestPoints = 100
	maxElement = 100
	maxFSize = 100000
	x = []
	y = []
	for i in range(numTestPoints):
		n = 5
		F_size = random.randint(1, maxFSize)
		zddF = set()
		for i in range(F_size):
			zddF.add(frozenset(random.sample([i for i in range(1, maxElement)], n)))
		time1 = time.time()
		constructZDD(zddF)
		runningTime = time.time() - time1
		x.append(F_size)
		y.append(runningTime)
	plt.plot(x, y, 'ro')
	plt.xlabel('|F| (given a constant |n|)')
	plt.ylabel('Running Time')
	plt.title('ZDD Construction Running Time vs. Number of Sets in Family |F|')
	plt.savefig("zdd_f_complexity_v3.png")
	plt.plot(x, y)
	'''
	'''
	numTestPoints = 1000
	maxElement = 10000
	F_size = 3
	maxN = 1000
	x = []
	y = []
	for i in range(numTestPoints):
		n = random.randint(1, maxN)
		zddF = set()
		for i in range(F_size):
			zddF.add(frozenset(random.sample([i for i in range(1, maxElement)], n)))
		time1 = time.time()
		constructZDD(zddF)
		runningTime = time.time() - time1
		x.append(n)
		y.append(runningTime)
	plt.plot(x, y, 'ro')
	plt.xlabel('|n| (given a constant |F|)')
	plt.ylabel('Running Time')
	plt.title('ZDD Construction Running Time vs. Size of Set |n| in a Family')
	plt.savefig("zdd_n_complexity.png")
	plt.plot(x, y)
	'''
	'''
	maxBElement = 2000
	x = []
	y = []
	x2 = []
	y2 = []
	for i in range(1, maxBElement, 5):
		A = constructZDD(set([frozenset([i + maxBElement for i in range(i)])]))
		B = constructZDD(set([frozenset([i for i in range(i)])]))
		time1 = time.time()
		C = Union(A, B)
		runningTime = time.time() - time1

		x.append(i)
		y.append(runningTime)
	plt.plot(x, y, 'ro')
	plt.xlabel("Number of Nodes in A and B")
	plt.ylabel('Running Time')
	plt.title('ZDD Union(A, B) Running Time vs. Number of Nodes in A and B')
	#plt.plot(x, y)
	#plt.plot(x, numpy.poly1d(numpy.polyfit(x, y, 1))(x))
	plt.savefig("zdd_union_complexity.png")
	'''
	'''
	plt.plot(x, y, 'ro')
	plt.xlabel("Number of Nodes in ZDD")
	plt.ylabel('Running Time')
	plt.title('ZDD Node Count Running Time vs. Number of Nodes in B')
	plt.plot(x, y)
	#plt.plot(x, numpy.poly1d(numpy.polyfit(x, y, 1))(x))
	plt.savefig("zdd_count_complexity.png")
	'''

	'''
	plt.plot(x, y, 'ro')
	plt.xlabel("Number of Nodes in B\'s ZDD")
	plt.ylabel('Running Time')
	plt.title('ZDD Counting Sets Running Time vs. Number of Nodes')
	plt.plot(x, y)
	#plt.plot(x, numpy.poly1d(numpy.polyfit(x, y, 1))(x))
	plt.savefig("zdd_count_complexity.png")
	'''

test()
#zddDictionary = testDictionary()
#print getZDDFamily(zddDictionary)

