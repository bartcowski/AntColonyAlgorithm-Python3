import random as rn
import numpy as np
from random import random
from DataParsing import reverse_dictionary
import time


class AntColonyAlgorithm(object):

    def __init__(self, n, distances, no_of_ants, n_best, n_iterations, pheromone_vaporization,
                 start, stop, names, q0_exploration=0.9, alpha=1, beta=1):
        """
        Args:
            n (int): the algorithm shows the shortest path and n-1 different ones - each a little bit longer
                but still decent
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            no_of_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iterations (int): Number of iterations
            pheromone_vaporization (float): Rate it which pheromone pheromone_vaporizations.
                The pheromone value is multiplied by pheromone_vaporization,
                so 0.95 will lead to pheromone_vaporization,
                0.5 to much faster pheromone_vaporization.
            alpha (int or float): exponent on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
            q0_exploration (float): between 0 and 1, if a random number is larger than the q0 parameter,
                then the algorithm will deterministically pick the next node in the path
        Example:
            ant_colony = AntColony(3, german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)
        """
        self.n = n
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.no_of_ants = no_of_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.pheromone_vaporization = pheromone_vaporization
        self.alpha = alpha
        self.beta = beta
        self.start = names[start]
        self.stop = names[stop]
        self.names = names
        self.q0_exploration = q0_exploration
        self.shortest_path = None
        self.all_generated_paths = []

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        n_paths = []

        start_time = int(round(time.time() * 1000))

        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths(self.start, self.stop)
            self.all_generated_paths.append(all_paths)
            finished_paths = []

            for path in all_paths:
                if self.stop == path[0][len(path[0])-1][1]:
                    finished_paths.append(path)

            # determining n-best paths
            finished_paths_copy = sorted(finished_paths.copy(), key=lambda x: x[1])
            fpc = []
            for path in finished_paths_copy:
                fpc.append(path[0])
            gp = self.get_grouped_paths(fpc)
            if len(gp) >= self.n:
                n_paths = sorted(gp, key=lambda x: x[1], reverse=True)
                n_paths = n_paths[0:self.n]

            self.spread_pheromone(finished_paths, self.n_best, shortest_path=shortest_path)
            if len(finished_paths) > 0:
                shortest_path = min(finished_paths, key=lambda x: x[1])
                # print("Shortest path in iteration ", i+1, " : ", shortest_path)
                if shortest_path[1] < all_time_shortest_path[1]:
                    all_time_shortest_path = shortest_path
            else:
                print("No path reaches end in iteration ", i)
            self.pheromone = self.pheromone * self.pheromone_vaporization

        # execution results
        execution_time = int(round(time.time() * 1000)) - start_time

        print("Shortest path: ", all_time_shortest_path)
        print("Found in: ", execution_time, " ms")
        if len(n_paths) == 0:
            print("But couldn't find another ", self.n - 1, " paths.")
        else:
            print("All requested shortest n-paths: ")
            for path in n_paths:
                print(path)
        self.shortest_path = all_time_shortest_path

    def translate_path_into_drawable(self, path, rev_dictionary):
        translated_path = []
        counter = 0     # used to find the last item in given path

        for tuple in path[0]:
            translated_path.append(rev_dictionary[tuple[0]])

            # without it the last city (our goal) is not included into drawable path
            if counter == len(path[0]) - 1:
                translated_path.append(rev_dictionary[tuple[1]])
            counter += 1
        return translated_path
    
    def get_drawable_paths(self):
        drawable_paths = []
        rev_dictionary = reverse_dictionary(self.names)
        for iteration_paths in self.all_generated_paths:
            drawable_iteration = []
            for path in iteration_paths:
                drawable_iteration.append(self.translate_path_into_drawable(path, rev_dictionary))

            drawable_paths.append(drawable_iteration)
        return drawable_paths
    
    def spread_pheromone(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self, start, stop):
        all_paths = []
        for i in range(self.no_of_ants):
            path = self.gen_path(start, stop)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start, stop):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        move = -1
        while move != stop: 
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            if move == -1:
                break
            path.append((prev, move))
            prev = move
            visited.add(move)
            
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)
        if row.sum() == 0:
            return -1
        norm_row = row / row.sum()
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        q = random()
        if q > self.q0_exploration:
            determ_row = pheromone * (1.0 / dist)
            determ_move = 0
            for i in range(len(determ_row)):
                if determ_row[i] > determ_row[determ_move]:
                    determ_move = i
            move = determ_move
        return move

    def get_grouped_paths(self, ants_population_paths):
        grouped_paths = []  # containing tuples of (path, number of those paths found in ants_population_paths)

        for ant_path in ants_population_paths:
            in_list = False
            for path in grouped_paths:
                if ant_path == path[0]:
                    new_size = path[1] + 1
                    grouped_paths.remove((path[0], path[1]))
                    grouped_paths.append((ant_path, new_size))
                    in_list = True
                    break
            if not in_list:
                grouped_paths.append((ant_path, 1))
        return grouped_paths
