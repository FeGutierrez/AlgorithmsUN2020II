#
# Write a function, `bipartite` that
# takes as input a graph, `G` and tries
# to divide G into two sets where
# there are no edges between elements of the
# the same set - only between elements in
# different sets.
# If two sets exists, return one of them
# or `None` otherwise
# Assume G is connected
#

def bipartite(G):
	revisado = {}

	def revisar_v(nodo, side):
		if nodo in revisado:
			return
		revisado[nodo] = side
		for vecino in G[nodo]:
			revisar_v(vecino, not side)

	for node in G:
		revisar_v(node, True)

	def valido(subconjunto):
		for node in subconjunto:
			for vecino in G[node]:
				if vecino in subconjunto:
					return False
		return True

	conjunto_izquierdo  = set(filter(lambda x: revisado[x], revisado))
	conjunto_derecho = set(G.keys()) - conjunto_izquierdo

	if valido(conjunto_izquierdo) and valido(conjunto_derecho):
		return conjunto_izquierdo

########
#
# Test

def enlazar(G, nodo1, nodo2, peso=1):
	if nodo1 not in G:
		G[nodo1] = {}
	(G[nodo1])[nodo2] = peso
	if nodo2 not in G:
		G[nodo2] = {}
	(G[nodo2])[nodo1] = peso
	return G

def test():
	aristas = [(1, 2), (2, 3), (1, 4), (2, 5),
			 (3, 8), (5, 6)]
	G = {}
	for n1, n2 in aristas:
		enlazar(G, n1, n2)
	g1 = bipartite(G)
	assert (g1 == set([1, 3, 5]) or
			g1 == set([2, 4, 6, 8]))
	aristas = [(1, 2), (1, 3), (2, 3)]
	G = {}
	for n1, n2 in aristas:
		enlazar(G, n1, n2)
	g1 = bipartite(G)
	assert g1 == None

if __name__ == '__main__':
	test()
	print "Test passes"