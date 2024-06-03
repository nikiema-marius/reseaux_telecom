# -*- coding: utf-8 -*-
"""
Created on Wed May 22 21:20:27 2024

@author: Nikiema Marius
"""


""" class Node:
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
    
    """
    
    
import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application de réseau de télécommunications")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Étiquettes et champs de saisie pour les nœuds et les liaisons
        tk.Label(self, text="Nœuds (séparés par des virgules):").grid(row=0, column=0, sticky="w")
        self.node_entry = tk.Entry(self)
        self.node_entry.grid(row=0, column=1)

        tk.Label(self, text="Liaisons (séparées par des virgules, format: Noeud1-Noeud2-Poids):").grid(row=1, column=0, sticky="w")
        self.edge_entry = tk.Entry(self)
        self.edge_entry.grid(row=1, column=1)

        # Bouton pour créer le graphe
        self.create_graph_button = tk.Button(self, text="Créer le graphe", command=self.create_graph)
        self.create_graph_button.grid(row=2, columnspan=2)

        # Canvas pour afficher le graphe
        self.canvas = tk.Canvas(self, width=700, height=500, bg="white")
        self.canvas.grid(row=3, columnspan=2)

        # Boutons pour calculer l'arbre couvrant minimal et le plus court chemin
        self.mst_button = tk.Button(self, text="Calculer l'arbre couvrant minimal", command=self.calculate_mst)
        self.mst_button.grid(row=4, column=0)
        
        # calcule du chemin le plus court
        self.shortest_path_button = tk.Button(self, text="Calculer le plus court chemin", command=self.calculate_shortest_path)
        self.shortest_path_button.grid(row=4, column=1)

    def create_graph(self):
        # Récupérer les données saisies par l'utilisateur et suppression des separateur 
        nodes = [node.strip() for node in self.node_entry.get().split(',')]
        edges_info = [edge.strip() for edge in self.edge_entry.get().split(',')]

        # Créer le graphe avec les elements saisis
        self.G = nx.Graph()
        for node in nodes:
            self.G.add_node(node)
        for edge_info in edges_info:
            node1, node2, weight = edge_info.split('-')
            self.G.add_edge(node1, node2, weight=int(weight))

        # Dessiner le graphe sur le canvas avec les noeuds entrés 
        self.draw_graph(self.G)

        #fonction pour dessiner le graphe
    def draw_graph(self, graph):
        self.canvas.delete("all")
        pos = nx.spring_layout(graph)
        min_x = min(pos.values(), key=lambda x: x[0])[0]
        min_y = min(pos.values(), key=lambda x: x[1])[1]
        max_x = max(pos.values(), key=lambda x: x[0])[0]
        max_y = max(pos.values(), key=lambda x: x[1])[1]

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        scale_x = (width - 40) / (max_x - min_x)
        scale_y = (height - 40) / (max_y - min_y)
        scale = min(scale_x, scale_y)

        for node1, node2, data in graph.edges(data=True):
            x1, y1 = pos[node1]
            x2, y2 = pos[node2]
            self.canvas.create_line((x1 - min_x) * scale + 20, (y1 - min_y) * scale + 20, (x2 - min_x) * scale + 20, (y2 - min_y) * scale + 20, fill="gray")
            mid_x = ((x1 - min_x) * scale + 20 + (x2 - min_x) * scale + 20) / 2
            mid_y = ((y1 - min_y) * scale + 20 + (y2 - min_y) * scale + 20) / 2
            self.canvas.create_text(mid_x, mid_y, text=str(data['weight']), fill="black")
        for node, (x, y) in pos.items():
            self.canvas.create_oval((x - min_x) * scale + 15, (y - min_y) * scale + 15, (x - min_x) * scale + 25, (y - min_y) * scale + 25, fill="lightblue")
            self.canvas.create_text((x - min_x) * scale + 20, (y - min_y) * scale + 20, text=node)

     #fonction pour implementer l'algorithme de kruskal
    def calculate_mst(self):
        try:
            mst = nx.minimum_spanning_tree(self.G, algorithm='kruskal')
            self.draw_graph(mst)
        except nx.NetworkXError as e:
            messagebox.showerror("Erreur", str(e))
            
  #fonction pour implementer l'algorithme de fonction dijkstra
    def calculate_shortest_path(self):
        try:
            start_node = simpledialog.askstring("Entrée", "Entrez le nœud de départ:")
            end_node = simpledialog.askstring("Entrée", "Entrez le nœud de fin:")
            path = nx.dijkstra_path(self.G, start_node, end_node)
            length = nx.dijkstra_path_length(self.G, start_node, end_node)

            messagebox.showinfo("Plus court chemin", f"Le chemin le plus court de {start_node} à {end_node} est : {path}\nLongueur totale du chemin : {length}")

            # Dessiner le graphe avec le chemin le plus court en rouge
            self.draw_graph_with_path(self.G, path)
        except (nx.NetworkXError, ValueError) as e:
            messagebox.showerror("Erreur", str(e))

    def draw_graph_with_path(self, graph, path):
        self.canvas.delete("all")
        pos = nx.spring_layout(graph)
        min_x = min(pos.values(), key=lambda x: x[0])[0]
        min_y = min(pos.values(), key=lambda x: x[1])[1]
        max_x = max(pos.values(), key=lambda x: x[0])[0]
        max_y = max(pos.values(), key=lambda x: x[1])[1]

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        scale_x = (width - 40) / (max_x - min_x)
        scale_y = (height - 40) / (max_y - min_y)
        scale = min(scale_x, scale_y)

        for node1, node2, data in graph.edges(data=True):
            x1, y1 = pos[node1]
            x2, y2 = pos[node2]
            self.canvas.create_line((x1 - min_x) * scale + 20, (y1 - min_y) * scale + 20, (x2 - min_x) * scale + 20, (y2 - min_y) * scale + 20, fill="gray")
            mid_x = ((x1 - min_x) * scale + 20 + (x2 - min_x) * scale + 20) / 2
            mid_y = ((y1 - min_y) * scale + 20 + (y2 - min_y) * scale + 20) / 2
            self.canvas.create_text(mid_x, mid_y, text=str(data['weight']), fill="black")
        for node, (x, y) in pos.items():
            self.canvas.create_oval((x - min_x) * scale + 15, (y - min_y) * scale + 15, (x - min_x) * scale + 25, (y - min_y) * scale + 25, fill="lightblue")
            self.canvas.create_text((x - min_x) * scale + 20, (y - min_y) * scale + 20, text=node)

        path_edges = list(zip(path, path[1:]))
        for node1, node2 in path_edges:
            x1, y1 = pos[node1]
            x2, y2 = pos[node2]
            self.canvas.create_line((x1 - min_x) * scale + 20, (y1 - min_y) * scale + 20, (x2 - min_x) * scale + 20, (y2 - min_y) * scale + 20, fill="red", width=2)

if __name__ == "__main__":
    app = Application()
    app.mainloop()

    
    
