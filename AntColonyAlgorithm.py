import random as rn
import numpy as np
from random import random

class AntColonyAlgorithm(object):

    def __init__(self, distances, no_of_ants, n_best, n_iterations, pheromone_vaporization, start, stop, names, q0_exploration = 0.9, alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            no_of_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            pheromone_vaporization (float): Rate it which pheromone pheromone_vaporizations. The pheromone value is multiplied by pheromone_vaporization, so 0.95 will lead to pheromone_vaporization, 0.5 to much faster pheromone_vaporization.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
            q0_exploration (float): between 0 and 1, if a random number is larger than the q0 parameter, then the algorithm will deterministically pick the next node in the path
        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.distances  = distances
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
        self.q0_exploration = q0_exploration

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths(self.start, self.stop)
            finished_paths = []
            for path in all_paths:
                if self.stop == path[0][len(path[0])-1][1]:
                    finished_paths.append(path)
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            if len(finished_paths) > 0:
                shortest_path = min(finished_paths, key=lambda x: x[1])
                print ("Shortest path in iteration ",i+1," : ",shortest_path)
                if shortest_path[1] < all_time_shortest_path[1]:
                    all_time_shortest_path = shortest_path
            else:
                print ("No path reaches end in iteration ",i)
            self.pheromone * self.pheromone_vaporization            
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best, shortest_path):
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
        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)
        if row.sum()==0:
            return -1
        norm_row = row / row.sum()
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        q = random()
        if q > self.q0_exploration:
            determ_row = pheromone * ((1.0)/dist)
            determ_move = 0
            for i in range(len(determ_row)):
                if determ_row[i] > determ_row[determ_move]:
                    determ_move = i
            move = determ_move
        return move