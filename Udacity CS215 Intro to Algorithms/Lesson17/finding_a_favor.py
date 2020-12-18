# Finding a Favor v2
#
# Each edge (u,v) in a social network has a weight p(u,v) that
# represents the probability that u would do a favor for v if asked.
# Note that p(v,u) != p(u,v), in general.
#
# Write a function that finds the right sequence of friends to maximize
# the probability that v1 will do a favor for v2.
#

#
# Provided are two standard versions of dijkstra's algorithm that were
# discussed in class. One uses a list and another uses a heap.
#
# You should manipulate the input graph, G, so that it works using
# the given implementations.  Based on G, you should decide which
# version (heap or list) you should use.
#

# code for heap can be found in the instructors comments below
from heap import *
from operator import itemgetter
from collections import defaultdict
from math import log, exp

def reformar_grafo(G):
	nuevo_grafo = defaultdict(dict)
	for nodo in G:
		for vecino in G[nodo]:
			nuevo_grafo[nodo][vecino] = log(G[nodo][vecino]) * -1
	return nuevo_grafo

def maximize_probability_of_favor(G, v1, v2):
	# your code here
	# call either the heap or list version of dijkstra
	# and return the path from `v1` to `v2`
	# along with the probability that v1 will do a favor
	# for v2

	def contar_aristas():
		return sum([len(G[v]) for v in G])

	G = reformar_grafo(G)

	# Theata(dijkstra_list) = Theata(n^2 + m) = Theata(n^2)
	# Theata(dijkstra_heap) = Theata(n * log(n) + m * log(n)) = Theata(m * log(n))
	numero_nodos = len(G.keys())
	numero_aristas = contar_aristas()

	if numero_aristas * log(numero_nodos) <= numero_nodos ** 2:
		dist_dict = dijkstra_heap(G, v1)
	else:
		dist_dict = dijkstra_list(G, v1)

	trayectoria = []
	nodo = v2
	while True:
		trayectoria += [nodo]
		if nodo == v1:
			break
		_, nodo = dist_dict[trayectoria[-1]]

	trayectoria = list(reversed(trayectoria))
	prob_log = dist_dict[v2][0] * -1

	return trayectoria, exp(prob_log)

#
# version of dijkstra implemented using a heap
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_heap(G, a):
	# Distance to the input node is zero, and it has
	# no parent
	primera_entrada = (0, a, None)
	heap = [primera_entrada]
	# location keeps track of items in the heap
	# so that we can update their value later
	ubicacion = {primera_entrada:0}
	distancia_actual = {a:primera_entrada}
	distancia_final = {}
	while len(distancia_actual) > 0:
		dist, node, parent = heappopmin(heap, ubicacion)
		# lock it down!
		distancia_final[node] = (dist, parent)
		del distancia_actual[node]
		for x in G[node]:
			if x in distancia_final:
				continue
			nueva_distancia = G[node][x] + distancia_final[node][0]
			nuevo_registro = (nueva_distancia, x, node)
			if x not in distancia_actual:
				# add to the heap
				insert_heap(heap, nuevo_registro, ubicacion)
				distancia_actual[x] = nuevo_registro
			elif nuevo_registro < distancia_actual[x]:
				# update heap
				decrease_val(heap, ubicacion, distancia_actual[x], nuevo_registro)
				distancia_actual[x] = nuevo_registro
	return distancia_final

#
# version of dijkstra implemented using a list
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_list(G, a):
	distancia_actual = {a:(0, None)} #keep track of the parent node
	distancia_final = {}
	while len(distancia_final) < len(G):
		node, entry = min(distancia_actual.items(), key=itemgetter(1))
		# lock it down!
		distancia_final[node] = entry
		del distancia_actual[node]
		for x in G[node]:
			if x in distancia_final:
				continue
			nueva_distancia = G[node][x] + distancia_final[node][0]
			nuevo_registro = (nueva_distancia, node)
			if x not in distancia_actual:
				distancia_actual[x] = nuevo_registro
			elif nuevo_registro < distancia_actual[x]:
				distancia_actual[x] = nuevo_registro
	return distancia_final

##########
#
# Test

def test():
	G = {'a':{'b':.9, 'e':.5},
		 'b':{'c':.9},
		 'c':{'d':.01},
		 'd':{},
		 'e':{'f':.5},
		 'f':{'d':.5}}
	path, prob = maximize_probability_of_favor(G, 'a', 'd')
	assert path == ['a', 'e', 'f', 'd']
	assert abs(prob - .5 * .5 * .5) < 0.001

if __name__ == '__main__':
	test()
	print "Test passes"