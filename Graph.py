from typing import List


class Edge:
	def __init__(self, first_node, second_node, pheromones=0):
		self.first_node = first_node
		self.second_node = second_node
		self.pheromones = pheromones
	
	def update_pheromones(self, pheromones):
		self.pheromones = pheromones


class Vertex:
	def __init__(self, name: str, edge_list: List[Edge] = []):
		self.name = name
		self.edge_list = edge_list

	def add_edge(self, connected_vertices, pheromones=0):
		self.edge_list.append(Edge(self, connected_vertices, pheromones))
		connected_vertices.edge_list.append(Edge(connected_vertices, self, pheromones))


class Graph:
	def __init__(self, vertices_list: List[Vertex] = []):
		self.vertices_list = vertices_list
		
	def add_vertex(self, name: str, edge_list: List[Edge] = []):
		self.vertices_list.append(Vertex(name, edge_list))
	
	def get_vertex_by_name(self, name: str):
		for vertex in self.vertices_list:
			if vertex.name == name:
				return vertex
		return None
