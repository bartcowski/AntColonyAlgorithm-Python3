import math
import pygame
import pygame.mixer
import time
import xml.etree.ElementTree as ET
from Ant import Ant
from AntColonyAlgorithm import AntColonyAlgorithm
from DataParsing import get_network_distances, get_network_node_dictionary, reverse_dictionary, translate_path_names
import numpy as np


WIN_H = 900
WIN_W = 1400
BG_COLOR = (204, 255, 204)
GRAPH_COLOR = (0, 0, 0)
NODE_RADIUS = 10
ANT_RADIUS = 5
EDGE_WIDTH = 2
ANT_COLOR = (204, 0, 0)

XML_FILE = 'usca.xml'

graph_vertices = []     # would work better as dictionary (TODO)
graph_edges = []

done_drawing = False    # prevents from drawing everything again


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Ant Colony Algorithm")
    screen.fill(BG_COLOR)

    clock = pygame.time.Clock()
    fps_limit = 30

    global graph_vertices
    global graph_edges

    get_vertices_from_xml(XML_FILE)
    get_edges_from_xml(XML_FILE)
    draw_graph(screen)
    pygame.display.flip()

    n = 5
    no_of_ants = 50
    n_best = 10
    n_iterations = 100
    pheromone_vaporization = 0.7
    distances = get_network_distances('usca.xml')
    dictionary = get_network_node_dictionary('usca.xml')
    ant_colony = AntColonyAlgorithm(n, distances, no_of_ants, n_best, n_iterations, pheromone_vaporization,
                                    start='Vancouver', stop='NewYork', names=dictionary,
                                    q0_exploration=0.95, alpha=1, beta=0.0001)
    ant_colony.run()
    drawable_paths = ant_colony.get_drawable_paths()

    done = False
    while not done:
        global done_drawing
        clock.tick(fps_limit)

        screen.fill(BG_COLOR)
        draw_graph(screen)
        pygame.display.flip()

        if not done_drawing:
            population_counter = 0  # used to draw only some populations for faster visualisation of progress
            for ants_population in drawable_paths:
                if population_counter % 5 == 0:
                    move_ants(ants_population, screen)
                population_counter += 1

        done_drawing = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()


def get_vertices_from_xml(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    global graph_vertices

    # get nodes...
    nodes = root[0][0]
    for node in nodes:
        # ugly calculations to increase space between nodes and allow them to
        # properly position on the screen at the same time
        x = int(float(node[0][0].text) + 150.0)
        x *= 25.0
        x -= 600.0
        y = int(WIN_H - float(node[0][1].text))
        y *= 30.0
        y -= 25370.0

        # graph_data stored in one list as city-x-y-city-x-y-...
        graph_vertices.append(node.attrib['id'])
        graph_vertices.append(x)
        graph_vertices.append(y)


def get_edges_from_xml(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    global graph_edges

    links = root[0][1]
    for link in links:
        # graph_edges stored in one list as source-target-source-...
        graph_edges.append(link[0].text)
        graph_edges.append(link[1].text)


def draw_graph(screen):
    i = 0
    while i < len(graph_vertices):
        pygame.draw.circle(screen, GRAPH_COLOR, (int(graph_vertices[i + 1]), int(graph_vertices[i + 2])), NODE_RADIUS, 0)
        i += 3

    e = 0
    source_coord = (0, 0)
    target_coord = (0, 0)
    while e < len(graph_edges):
        i = 0
        while i < len(graph_vertices):
            if graph_vertices[i] == graph_edges[e]:
                source_coord = (int(graph_vertices[i + 1]), int(graph_vertices[i + 2]))
            elif graph_vertices[i] == graph_edges[e + 1]:
                target_coord = (int(graph_vertices[i + 1]), int(graph_vertices[i + 2]))
            i += 3
        pygame.draw.line(screen, GRAPH_COLOR, source_coord, target_coord, EDGE_WIDTH)
        e += 2


def calc_edge_length(source_city, target_city):
    global graph_vertices
    source_coord = get_city_coords(source_city)
    target_coord = get_city_coords(target_city)

    return math.sqrt(((target_coord[0] - source_coord[0]) ** 2) + ((target_coord[1] - source_coord[1]) ** 2))


def get_city_coords(city):
    global graph_vertices
    x = (0, 0)
    y = (0, 0)

    i = 0
    while i < len(graph_vertices):
        if graph_vertices[i] == city:
            x = graph_vertices[i + 1]
            y = graph_vertices[i + 2]
        i += 3

    return x, y


def get_grouped_paths(ants_population_paths):
    grouped_paths = []   # containing tuples of (path, number of those paths found in ants_population_paths)

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


def move_ants(ants_population_paths, screen):
    time.sleep(1)
    global done_drawing
    ticks_per_edge = 50
    ants = []
    city_index = 0  # which city is the current source_city

    grouped_paths = get_grouped_paths(ants_population_paths)
    while True:
        # create one ant for every path - it travels ONE edge and gets deleted
        # another set of Ant objects needs to be created for the next one
        for ant_path in grouped_paths:
            if city_index < len(ant_path[0]) - 1:
                source_city = get_city_coords(ant_path[0][city_index])
                target_city = get_city_coords(ant_path[0][city_index + 1])
                x = source_city[0]
                y = source_city[1]
                dx = (target_city[0] - source_city[0]) / ticks_per_edge
                dy = (target_city[1] - source_city[1]) / ticks_per_edge
                size = ANT_RADIUS + ant_path[1]
                ants.append(Ant(x, y, dx, dy, size))

        # if no ants were created then all movement is finished
        if not ants:
            break

        counter = 0
        while counter < ticks_per_edge:
            screen.fill(BG_COLOR)
            draw_graph(screen)
            for ant in ants:
                pygame.draw.circle(screen, ANT_COLOR, (int(ant.x), int(ant.y)), ant.size, 0)
                ant.update_xy()
            pygame.display.flip()
            counter += 1

        city_index += 1
        ants.clear()

    done_drawing = True


if __name__ == "__main__":
    main()
