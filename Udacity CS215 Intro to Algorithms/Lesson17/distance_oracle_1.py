#
# In the shortest-path oracle described in Andrew Goldberg's
# interview, each node has a label, which is a list of some other
# nodes in the network and their distance to these nodes. These lists
# have the property that
#
#  (1) for any pair of nodes (x,y) in the network, their lists will
#  have at least one node z in common
#
#  (2) the shortest path from x to y will go through z.
#
# Given a graph G that is a balanced binary tree, preprocess the graph to
# create such labels for each node.  Note that the size of the list in
# each label should not be larger than log n for a graph of size n.
#

#
# create_labels takes in a balanced binary tree and the root element
# and returns a dictionary, mapping each node to its label
#
# a label is a dictionary mapping another node and the distance to
# that node
#
def crear_etiquetas(binarytreeG, root):
	etiquetas = {root: {root: 0}}
	frontera = [root]
	while frontera:
		cparent = frontera.pop(0)
		for hijo in binarytreeG[cparent]:
			if hijo in etiquetas:
				continue
			etiquetas[hijo] = {hijo: 0}
			peso = binarytreeG[cparent][hijo]
			etiquetas[hijo][cparent] = peso
			for ancestor in etiquetas[cparent]:
				etiquetas[hijo][ancestor] = peso + etiquetas[cparent][ancestor]
			frontera += [hijo]
	return etiquetas

#######
# Testing
#

def obtener_distancias(G, etiquetas):
	distancias = {}
	for inicio in G:
		label_node = etiquetas[inicio]
		s_distances = {}
		for destino in G:
			mas_corto = float('inf')
			etiqueta_destino = etiquetas[destino]
			for nodo_intermedio, dist in label_node.iteritems():
				if nodo_intermedio == destino:
					mas_corto = dist
					break
				other_dist = etiqueta_destino.get(nodo_intermedio)
				if other_dist is None:
					continue
				if other_dist + dist < mas_corto:
					mas_corto = other_dist + dist
			s_distances[destino] = mas_corto
		distancias[inicio] = s_distances
	return distancias

def enlazar(G, nodo1, nodo2, peso=1):
	if nodo1 not in G:
		G[nodo1] = {}
	(G[nodo1])[nodo2] = peso
	if nodo2 not in G:
		G[nodo2] = {}
	(G[nodo2])[nodo1] = peso
	return G

def test():
	aristas = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
			 (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
	arbol = {}
	for n1, n2 in aristas:
		enlazar(arbol, n1, n2)
	etiquetas = crear_etiquetas(arbol, 1)
	distancias = obtener_distancias(arbol, etiquetas)
	assert distancias[1][2] == 1
	assert distancias[1][4] == 2

if __name__ == '__main__':
	test()
	print "Test passes"