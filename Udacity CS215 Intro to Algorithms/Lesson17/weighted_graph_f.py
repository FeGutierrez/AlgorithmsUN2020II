#
# In lecture, we took the bipartite Marvel graph,
# where edges went between characters and the comics
# books they appeared in, and created a weighted graph
# with edges between characters where the weight was the
# number of comic books in which they both appeared.
#
# In this assignment, determine the weights between
# comic book characters by giving the probability
# that a randomly chosen comic book containing one of
# the characters will also contain the other
#

import itertools
from collections import defaultdict
import cPickle

marvel     = cPickle.load(open("smallG.pkl"))
characters = cPickle.load(open("smallChr.pkl"))

def create_weighted_graph(bipartiteG, personajes):
	G = defaultdict(dict)
	for personaje_a, personaje_b in itertools.combinations(personajes, 2):
		libros_a = set(bipartiteG[personaje_a])
		libros_b = set(bipartiteG[personaje_b])

		numero_libros_en_comun = float(len(libros_a.intersection(libros_b)))
		if numero_libros_en_comun == 0:
			continue

		prob = numero_libros_en_comun / (len(libros_a)+len(libros_b)-numero_libros_en_comun)
		G[personaje_a][personaje_b] = prob
		G[personaje_b][personaje_a] = prob

	return G

######
#
# Test

def test():
	bipartiteG = {'charA':{'comicB':1, 'comicC':1},
				  'charB':{'comicB':1, 'comicD':1},
				  'charC':{'comicD':1},
				  'comicB':{'charA':1, 'charB':1},
				  'comicC':{'charA':1},
				  'comicD': {'charC':1, 'charB':1}}
	G = create_weighted_graph(bipartiteG, ['charA', 'charB', 'charC'])
	# three comics contain charA or charB
	# charA and charB are together in one of them
	assert G['charA']['charB'] == 1.0 / 3
	assert G['charA'].get('charA') == None
	assert G['charA'].get('charC') == None

def test2():
	G = create_weighted_graph(marvel, characters)

if __name__ == '__main__':
	test()
	test2()
	print "Test passes"