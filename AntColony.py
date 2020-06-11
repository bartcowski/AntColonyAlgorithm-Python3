import math
import pygame
import pygame.mixer
import time
import xml.etree.ElementTree as ET
from Ant import Ant

WIN_H = 900
WIN_W = 1400
BG_COLOR = (204, 255, 204)
GRAPH_COLOR = (0, 0, 0)
NODE_RADIUS = 10
EDGE_WIDTH = 2
ANT_COLOR = (204, 0, 0)

XML_FILE = 'usca.xml'

graph_vertices = []     # would work better as dictionary (TODO)
graph_edges = []

# TEST
done_drawing = False


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

    # TEST
    print(graph_vertices)
    print(graph_edges)
    print(get_city_coords('LosAngeles'))
    print(calc_edge_length('LosAngeles', 'LasVegas'))
    # TEST

    ants_population_paths = [['Vancouver', 'Seattle', 'Portland', 'SaltLakeCity'],
                             ['SanDiego', 'Phoenix', 'LasVegas', 'SaltLakeCity', 'Calgary', 'Winnipeg', 'Minneapolis'],
                             ['Miami', 'Tampa', 'Charlotte', 'Nashville', 'Memphis'],
                             ['SanDiego', 'Phoenix', 'LasVegas', 'SaltLakeCity', 'Calgary', 'Winnipeg', 'Minneapolis'],
                             ['Phoenix', 'ElPaso', 'Dallas', 'Denver', 'KansasCity'],
                             ['Toronto', 'Montreal', 'Boston', 'NewYork', 'Philadelphia', 'WashingtonDC'],
                             ['SanDiego', 'Phoenix', 'LasVegas', 'SaltLakeCity', 'Calgary', 'Winnipeg', 'Minneapolis'],
                             ['SanDiego', 'Phoenix', 'LasVegas', 'SaltLakeCity', 'Calgary', 'Winnipeg', 'Minneapolis'],
                             ['SanDiego', 'Phoenix', 'LasVegas', 'SaltLakeCity', 'Calgary', 'Winnipeg', 'Minneapolis'],
                             ['SanDiego', 'Phoenix', 'LasVegas', 'SaltLakeCity', 'Calgary', 'Winnipeg', 'Minneapolis'],
                             ['SanDiego', 'Phoenix', 'LasVegas', 'SaltLakeCity', 'Calgary', 'Winnipeg', 'Minneapolis'],
                             ['SanDiego', 'Phoenix', 'LasVegas', 'SaltLakeCity', 'Calgary', 'Winnipeg', 'Minneapolis'],
                             ['SanDiego', 'Phoenix', 'LasVegas', 'SaltLakeCity', 'Calgary', 'Winnipeg', 'Minneapolis']]

    done = False
    while not done:
        clock.tick(fps_limit)

        screen.fill(BG_COLOR)
        draw_graph(screen)
        pygame.display.flip()

        global done_drawing
        if not done_drawing:
            move_ants(ants_population_paths, screen)

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


def move_ants(ants_population_paths, screen):
    time.sleep(1)
    global done_drawing
    ticks_per_edge = 100
    ants = []
    city_index = 0  # which city is the current source_city

    while True:
        # create one ant for every path - it travels ONE edge and gets deleted
        # another set of Ant objects needs to be created for the next one
        for ant_path in ants_population_paths:
            if city_index < len(ant_path) - 1:
                source_city = get_city_coords(ant_path[city_index])
                target_city = get_city_coords(ant_path[city_index + 1])
                x = source_city[0]
                y = source_city[1]
                dx = (target_city[0] - source_city[0]) / ticks_per_edge
                dy = (target_city[1] - source_city[1]) / ticks_per_edge
                ants.append(Ant(x, y, dx, dy))

        # if no ants were created then all movement is finished
        if not ants:
            break

        counter = 0
        while counter < ticks_per_edge:
            screen.fill(BG_COLOR)
            draw_graph(screen)
            for ant in ants:
                pygame.draw.circle(screen, ANT_COLOR, (int(ant.x), int(ant.y)), NODE_RADIUS, 0)
                ant.update_xy()
            pygame.display.flip()
            counter += 1

        city_index += 1
        ants.clear()

    done_drawing = True


if __name__ == "__main__":
    main()
