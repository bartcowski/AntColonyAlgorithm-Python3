from Graph import Graph, Edge, Vertice

Class AntColonyAlgorithm:
	def __init__(self, graph, start_point, end_point, no_of_ants, pheromone_vaporization, q0_exploration, alpha, beta):
		self.graph = graph
		self.start_point = start_point
		self.end_point = end_point
		self.no_of_ants = no_of_ants
		self.pheromone_vaporization = pheromone_vaporization
		self.q0_exploration = q0_exploration
		self.alpha = alpha
		self.beta = beta