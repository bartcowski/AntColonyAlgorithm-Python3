import pygame
import math
import xml.etree.ElementTree as ET

WIN_H = 900
WIN_W = 1400
BG_COLOR = (204, 255, 204)
GRAPH_COLOR = (0, 0, 0)
NODE_RADIUS = 10
EDGE_WIDTH = 2
ANT_COLOR = (204, 0, 0)

XML_FILE = 'usca.xml'

graph_vertices = []
graph_edges = []


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Ant Colony Algorithm")
    screen.fill(BG_COLOR)

    global graph_vertices
    global graph_edges

    # graph_data = get_and_draw_graph_from_xml('usca.xml', screen)
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

    done = False
    while not done:

        screen.fill(BG_COLOR)
        draw_graph(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()


def get_vertices_from_xml(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    global graph_vertices

    # draw nodes...
    nodes = root[0][0]
    for node in nodes:
        # ugly calculations to increase space between nodes and allow them to
        # properly position on the screen at the same time
        x = int(float(node[0][0].text) + 150.0)
        x *= 25.0
        x -= 600.0
        y = int(float(node[0][1].text))
        y *= 30.0
        y -= 700.0

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


def move_ant(source_city, target_city):
    a = 0
    # TODO


if __name__ == "__main__":
    main()
