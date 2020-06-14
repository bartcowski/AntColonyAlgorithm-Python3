import xml.etree.ElementTree as ET
import numpy as np

def get_network_distances(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    nodes = root[0][0]
    links = root[0][1]
    no_of_nodes = len(nodes.getchildren())
    distances_array = np.full((no_of_nodes, no_of_nodes), np.inf)
    nam_dict = get_network_node_dictionary(filename)
    for i in range(no_of_nodes):
        distances_array[i][i] = np.inf
    for link in links:
        start = link[0].text
        end = link[1].text
        distance = float(link[2][0][1].text)
        distances_array[nam_dict[start]][nam_dict[end]] = distance
    return distances_array

def get_network_node_dictionary(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    nodes = root[0][0]
    i = 0
    names_dict = {}
    for node in nodes:
        names_dict[node.attrib['id']] = i
        i+=1
    return names_dict

def reverse_dictionary(dictionary):
    rev_dictionary = {v: k for k, v in dictionary.items()}
    return rev_dictionary

def translate_path_names(path, rev_dictionary):
    translated_path = ([], path[1])
    for tuple in path[0]:
        translated_path[0].append((rev_dictionary[tuple[0]], rev_dictionary[tuple[1]]))
    return translated_path