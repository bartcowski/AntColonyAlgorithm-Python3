from typing import List

class Edge:
	def __init__(self, first_vertice, second_vertice, pheromones = 0):
		self.first_node = first_node
		self.second_node = second_node
		self.pheromones = 0
	
	def update_pheromones(self, pheromones):
		self.pheromones = pheromones


class Vertice:
	def __init__(self, name: str, edge_list: List[Edge] = []):
		self.name = name
		self.edge_list = edge_list
	
	def add_edge(self, connected_vertice, pheromones=0):
		edge_list.append(Edge(self, connected_vertice, pheromones))
		connected_vertice.edge_list.append(Edge(connected_vertice, self, pheromones))


class Graph:
	def __init__(self, vertice_list: List[Vertice] = []):
		self.vertice_list = vertice_list
		
	def add_vertive(self, name: str, edge_list: List[Edge] = []):
		self.vertice_list.append(Vertice(name, edge_list))
	
	def get_vertice_by_name(self, name: str):
		for vertice in self.vertice_list:
			if vertice.name == name:
				return vertice
		return None
