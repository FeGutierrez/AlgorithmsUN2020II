#
# Take a weighted graph representing a social network where the weight
# between two nodes is the "love" between them.  In this "feel the
# love of a path" problem, we want to find the best path from node `i`
# and node `j` where the score for a path is the maximum love of an
# edge on this path. If there is no path from `i` to `j` return
# `None`.  The returned path doesn't need to be simple, ie it can
# contain cycles or repeated vertices.
#
# Devise and implement an algorithm for this problem.
#

import heapq
from collections import defaultdict

def feel_the_love(G, i, j):
	# return a path (a list of nodes) between `i` and `j`,
	# with `i` as the first node and `j` as the last node,
	# or None if no path exists
	path = dijkstra_path(G, i)
	if not j in path:
		return None

	nodo1, nodo2 = max_weight_edge(G, i)
	trayectoria_a = path[nodo1]
	trayectoria_b = (dijkstra_path(G, nodo2))[j]

	return trayectoria_a + trayectoria_b

def max_weight_edge(G, i):
	maximo_actual = -float('inf')
	arista       = None
	alcanzable  = dijkstra_path(G, i)
	for nodo in G:
		for vecino in G[nodo]:
			if (G[nodo])[vecino] > maximo_actual and nodo in alcanzable:
				maximo_actual = (G[nodo])[vecino]
				arista = nodo, vecino

	return arista

def dijkstra_path(HG, v):
	distancia_actual = {v: 0}
	distancia_final = {}
	trayectoria_final = defaultdict(list)
	heap = [(0, v)]
	while distancia_actual:
		(w, k) = heapq.heappop(heap)
		if k in distancia_final or (k in distancia_actual and w > distancia_actual[k]):
			continue
		else:
			del distancia_actual[k]
			distancia_final[k] = w
		for vecino in [nb for nb in HG[k] if nb not in distancia_final]:
			nw = distancia_final[k]+ HG[k][vecino]
			trayectoria_final[vecino] = trayectoria_final[k] + [k]

			if vecino not in distancia_actual or nw < distancia_actual[vecino]:
				distancia_actual[vecino] = nw
				heapq.heappush(heap, (nw, vecino))

	for nodo in trayectoria_final:
		trayectoria_final[nodo] += [nodo]
	return trayectoria_final

#########
#
# Test

def score_of_path(G, trayectoria):
	amor_maximo = -float('inf')
	for n1, n2 in zip(trayectoria[:-1], trayectoria[1:]):
		amor = G[n1][n2]
		if amor > amor_maximo:
			amor_maximo = amor
	return amor_maximo

def test():
	G = {'a':{'c':1},
		 'b':{'c':1},
		 'c':{'a':1, 'b':1, 'e':1, 'd':1},
		 'e':{'c':1, 'd':2},
		 'd':{'e':2, 'c':1},
		 'f':{}}
	trayectoria = feel_the_love(G, 'a', 'b')
	assert score_of_path(G, trayectoria) == 2

	trayectoria = feel_the_love(G, 'a', 'f')
	assert trayectoria == None

if __name__ == '__main__':
	test()
	print "Test passes"