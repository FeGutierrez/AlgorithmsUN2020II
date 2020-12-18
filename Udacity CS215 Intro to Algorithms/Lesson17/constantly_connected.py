#
# Design and implement an algorithm that can preprocess a
# graph and then answer the question "is x connected to y in the
# graph" for any x and y in constant time Theta(1).
#

#
# `process_graph` will be called only once on each graph.  If you want,
# you can store whatever information you need for `is_connected` in
# global variables
#

global_G = {}

def procesar_grafo(G):
	global global_G
	global_G = G
	for nodo in global_G:
		por_visitar = global_G[nodo].keys()

		while por_visitar:
			nuevo_nodo = por_visitar.pop()

			global_G[nodo][nuevo_nodo] = 1
			global_G[nuevo_nodo][nodo] = 1

			for x in global_G[nuevo_nodo]:
				if x not in global_G[nodo]:
					por_visitar += [x]

#
# When being graded, `is_connected` will be called
# many times so this routine needs to be quick
#
def esta_conectado(i, j):
	# your code here
	return i in global_G[j] or j in global_G[i]

#######
# Testing
#
def test():
	G = {'a':{'b':1},
		 'b':{'a':1},
		 'c':{'d':1},
		 'd':{'c':1},
		 'e':{}}
	procesar_grafo(G)
	assert esta_conectado('a', 'b') == True
	assert esta_conectado('a', 'c') == False

	G = {'a':{'b':1, 'c':1},
		 'b':{'a':1},
		 'c':{'d':1, 'a':1},
		 'd':{'c':1},
		 'e':{}}
	procesar_grafo(G)
	assert esta_conectado('a', 'b') == True
	assert esta_conectado('a', 'c') == True
	assert esta_conectado('a', 'e') == False

if __name__ == '__main__':
	test()
	print "Test passes"