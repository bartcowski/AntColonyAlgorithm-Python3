class Edge:
	def __init__(self, first_vertice, second_vertice, directionnal=False, pheromones = 0):
		self.first_node = first_node
		self.second_node = second_node
		self.directionnal = directionnal
		self.pheromones = 0
	
	def update_pheromones(self, pheromones):
		self.pheromones = pheromones



class Vertice:
	def __init__(self, name, edge_list = [])
		self.name = name
		self.edge_list = edge_list
	
	def add_edge(self, connected_vertice, directionnal = False, pheromones=0):
		edge_list.append(Edge(self, connected_vertice, directionnal, pheromones))



class Graph:
	def __init__(self, vertice_list=[]):
		self.vertice_list = vertice_list
		
	def add_vertive(self, name, edge_list=[]):
		self.vertice_list.append(Vertice(name, edge_list))
	
	def get_vertice_by_name(self, name):
		for vertice in self.vertice_list:
			if vertice.name == name:
				return vertice
		return None