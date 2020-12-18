#
# This is the same problem as "Distance Oracle I" except that instead of
# only having to deal with binary trees, the assignment asks you to
# create labels for all tree graphs.
#
# In the shortest-path oracle described in Andrew Goldberg's
# interview, each node has a label, which is a list of some other
# nodes in the network and their distance to these nodes.  These lists
# have the property that
#
#  (1) for any pair of nodes (x,y) in the network, their lists will
#  have at least one node z in common
#
#  (2) the shortest path from x to y will go through z.
#
# Given a graph G that is a tree, preprocess the graph to
# create such labels for each node.  Note that the size of the list in
# each label should not be larger than log n for a graph of size n.
#

#
# create_labels takes in a tree and returns a dictionary, mapping each
# node to its label
#
# a label is a dictionary mapping another node and the distance to
# that node
#

def contar_nodos(treeG, node):
	# count all sub-nodes including itself
	cnts = {}
	visited = {}
	cnts[node] = contar_nodos_rec(treeG, node, cnts, visited)
	return cnts

def contar_nodos_rec(treeG, nodo, cnts, visitados):
	visitados[nodo] = True
	frontera = [nodo]
	cnts[nodo] = 1
	for v in treeG[nodo]:
		if v not in visitados:
			cnts[nodo] += contar_nodos_rec(treeG, v, cnts, visitados)
	return cnts[nodo]

def crear_etiquetas(treeG):
	# find center node via rotation
	def find_cen(treeG, tmt_root, cnts):
		if cnts[tmt_root] == 1:
			return tmt_root
		mcc, mc = max((cnts[v], v) for v in treeG[tmt_root] if v not in cens_nodes)
		# center node found!
		if cnts[tmt_root] - mcc >= mcc:
			return tmt_root
		# rotate 'tmt_root' to mc
		cnts[mc] += cnts[tmt_root] - mcc
		cnts[tmt_root] -= mcc
		return find_cen(treeG, mc, cnts)
	# recursively finding center node for each 'sub-tree'
	def etiqueta_de_arbol(tmt_root):
		cen = find_cen(treeG, tmt_root, cnts)
		label_sub(cen)
		for child in treeG[cen]:
			if child not in cens_nodes:
				etiqueta_de_arbol(child)
	# BFS routine for tagging each descendant node with its sub-center node
	def label_sub(sub_cen):
		if sub_cen not in labels:
			labels[sub_cen] = {}
		labels[sub_cen][sub_cen] = 0
		cens_nodes[sub_cen] = True
		frontier = [sub_cen]
		visitados = {}
		while frontier:
			v = frontier.pop(0)
			for vecino in treeG[v]:
				if vecino not in visitados and vecino not in cens_nodes:
					visitados[vecino] = True
					frontier += [vecino]
					if vecino not in labels:
						labels[vecino] = {vecino: 0}
					labels[vecino][sub_cen] = treeG[v][vecino] + labels[v][sub_cen]
	cens_nodes = {}
	labels = {}
	tmt_root = iter(treeG).next()
	cnts = contar_nodos(treeG, tmt_root)
	etiqueta_de_arbol(tmt_root)
	return labels

#######
# Testing
#

def obtener_distancias(G, etiquetas):
	# labels = {a:{b: distance from a to b,
	#              c: distance from a to c}}
	# create a mapping of all distances for
	# all nodes
	distancias = {}
	for inicio in G:
		# get all the labels for my starting node
		label_node = etiquetas[inicio]
		s_distances = {}
		for destino in G:
			shortest = float('inf')
			# get all the labels for the destination node
			etiquetas_destino = etiquetas[destino]
			# and then merge them together, saving the
			# shortest distance
			for nodo_intermedio, dist in label_node.iteritems():
				# see if intermediate_node is our destination
				# if it is we can stop - we know that is
				# the shortest path
				if nodo_intermedio == destino:
					shortest = dist
					break
				other_dist = etiquetas_destino.get(nodo_intermedio)
				if other_dist is None:
					continue
				if other_dist + dist < shortest:
					shortest = other_dist + dist
			s_distances[destino] = shortest
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
	tree = {}
	for n1, n2 in aristas:
		enlazar(tree, n1, n2)
	etiquetas = crear_etiquetas(tree)
	if etiquetas:
		distancias = obtener_distancias(tree, etiquetas)
	assert distancias[1][2] == 1
	assert distancias[1][4] == 2
	assert distancias[1][2] == 1
	assert distancias[1][4] == 2
	assert distancias[4][1] == 2
	assert distancias[1][4] == 2
	assert distancias[2][1] == 1
	assert distancias[1][2] == 1
	assert distancias[1][1] == 0
	assert distancias[2][2] == 0
	assert distancias[9][9] == 0
	assert distancias[2][3] == 2
	assert distancias[12][13] == 2
	assert distancias[13][8] == 6
	assert distancias[11][12] == 6
	assert distancias[1][12] == 3

def test2():
	aristas = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
			 (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13)]
	tree = {}
	for n1, n2 in aristas:
		enlazar(tree, n1, n2)
	etiquetas = crear_etiquetas(tree)
	distancias = obtener_distancias(tree, etiquetas)
	assert distancias[1][2] == 1
	assert distancias[1][3] == 2
	assert distancias[1][13] == 12
	assert distancias[6][1] == 5
	assert distancias[6][13] == 7
	assert distancias[8][3] == 5
	assert distancias[10][4] == 6

if __name__ == '__main__':
	test()
	test2()
	print "Test passes"