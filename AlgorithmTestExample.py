from AntColonyAlgorithm import AntColonyAlgorithm
import numpy as np
from DataParsing import get_network_distances, get_network_node_dictionary, reverse_dictionary, translate_path_names

distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])
                      
distances = get_network_distances('usca.xml')
dictionary = get_network_node_dictionary('usca.xml')
rev_dictionary = reverse_dictionary(dictionary)

ant_colony = AntColonyAlgorithm(distances, 10, 1, 100, 0.95, start = 'Vancouver', stop = 'Miami', names = dictionary, alpha=1, beta=1)
shortest_path = ant_colony.run()
translated_path = translate_path_names(ant_colony.shortest_path, rev_dictionary)
print ("Shortest path: {}".format(translated_path))