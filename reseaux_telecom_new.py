# -*- coding: utf-8 -*-
"""
Created on Wed May 22 21:20:27 2024

@author: Nikiema Marius
"""


class Node:
    def __init__(self, id, data=None):
        self.id = id
        self.data = data

class Edge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

import networkx as nx
import matplotlib.pyplot as plt


############################### fonction de creation du reseaux de telecomunication
def create_graph():
    nodes = []
    edges = []

    # Demander à l'utilisateur de saisir les nœuds
    nodes_str = input("Entrez les nœuds séparés par des virgules (ex: A, B, C): ")
    node_ids = [x.strip() for x in nodes_str.split(',')]
    for node_id in node_ids:
        nodes.append(node_id)

    # Demander à l'utilisateur de saisir les liaisons et les poids
    edges_str = input("Entrez les liaisons et les poids séparés par des virgules (ex: A-B-4, B-C-2): ")
    edge_info = [x.strip() for x in edges_str.split(',')]
    for info in edge_info:
        node1_id, node2_id, weight = info.split('-')
        edges.append((node1_id, node2_id, int(weight)))  # Utiliser les identifiants des nœuds

    G = nx.Graph()

    # Ajouter des nœuds au graphe
    for node in nodes:
        G.add_node(node)

    # Ajouter des arêtes au graphe
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])  # Utiliser les identifiants des nœuds

    return G

####################################################################################################



#################### fonction kruskal###################################################
def kruskal_mst(G):
    MST = nx.minimum_spanning_tree(G, algorithm='kruskal')
    return MST



#################### fonction dijkstra##################################################

def dijkstra_shortest_path(G, start, end):
    shortest_path = nx.dijkstra_path(G, source=start, target=end)
    shortest_path_length = nx.dijkstra_path_length(G, source=start, target=end)
    return shortest_path, shortest_path_length

####################################################################################################






##############fonction main (fonction principale)

if __name__ == "__main__":
    # Créer le graphe en demandant à l'utilisateur de saisir les données
    G = create_graph()

    # Dessiner le graphe
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Réseau de télécommunications")
    plt.show()

    # Calculer l'arbre couvrant minimal (Kruskal)
    MST = kruskal_mst(G)
    pos = nx.spring_layout(MST)
    edge_labels = nx.get_edge_attributes(MST, 'weight')
    nx.draw(MST, pos, with_labels=True, node_color='lightgreen', node_size=3000, font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_edge_labels(MST, pos, edge_labels=edge_labels)
    plt.title("Arbre couvrant minimal (Kruskal)")
    plt.show()

    # Demander à l'utilisateur de saisir les nœuds pour calculer le chemin le plus court
    start_node = input("Entrez le nœud de départ: ")
    end_node = input("Entrez le nœud de fin: ")
    
    # Calculer le plus court chemin entre les nœuds spécifiés
    path, length = dijkstra_shortest_path(G, start_node, end_node)

    # Afficher le résultat
    print(f"Le chemin le plus court de {start_node} à {end_node} est : {path}")
    print(f"Longueur totale du chemin : {length}")

    # Dessiner le chemin le plus court
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    plt.title(f"Chemin le plus court de {start_node} à {end_node}")
    plt.show()
