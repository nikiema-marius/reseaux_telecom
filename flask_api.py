import io
import logging
from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import networkx as nx
from matplotlib import pyplot as plt
import base64
import numpy as np
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

api = Api(app, version='1.0', title='API de Réseau de Télécommunications',
          description='Une API simple pour gérer un réseau de télécommunications')

ns = api.namespace('telecom', description='Opérations de télécommunications')

node_model = api.model('Node', {
    'id': fields.String(required=True, description='L\'identifiant du nœud'),
    'data': fields.String(description='Les données associées au nœud')
})

edge_model = api.model('Edge', {
    'node1': fields.String(required=True, description='Le premier nœud de l\'arête'),
    'node2': fields.String(required=True, description='Le second nœud de l\'arête'),
    'weight': fields.Integer(required=True, description='Le poids de l\'arête')
})

graph_model = api.model('Graph', {
    'nodes': fields.List(fields.Nested(node_model), description='La liste des nœuds'),
    'edges': fields.List(fields.Nested(edge_model), description='La liste des arêtes'),
    'pos': fields.Raw(required=False, description='Position des noeuds du graphe'),
    'plot_url': fields.String(required=True, description='Le lien du graphe')
})

shortest_path_model = api.model('ShortestPath', {
    'graph': fields.Nested(graph_model, description='Le graphe', required=True),
    'start': fields.String(required=True, description='Le nœud de depart'),
    'end': fields.String(required=True, description='Le nœud d\'arrive')
})

@ns.route('/graph')
class GraphResource(Resource):
    @ns.expect(graph_model)
    @ns.marshal_with(graph_model)
    def post(self):
        """Crée un graphe à partir des nœuds et des arêtes fournis"""
        data = request.json
        G = nx.Graph()
        for node in data['nodes']:
            G.add_node(node['id'], data=node.get('data'))
        for edge in data['edges']:
            G.add_edge(edge['node1'], edge['node2'], weight=edge['weight'])
        
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx_labels(G, pos)
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        data['plot_url'] = plot_url
        pos_json_ready = {k: v.tolist() for k, v in pos.items()}
        data['pos'] = pos_json_ready
        return data

@ns.route('/mst')
class MSTResource(Resource):
    @ns.expect(graph_model)
    @ns.marshal_with(graph_model)
    def post(self):
        """Calcule l'arbre couvrant minimal du graphe fourni"""
        data = request.json
        G = nx.Graph()
        for node in data['nodes']:
            G.add_node(node['id'], data=node.get('data'))
        for edge in data['edges']:
            G.add_edge(edge['node1'], edge['node2'], weight=edge['weight'])
        MST = nx.minimum_spanning_tree(G, algorithm='kruskal')
        pos = nx.spring_layout(MST)
        nx.draw_networkx(MST, pos)
        # edge_labels = nx.get_edge_attributes(G, 'weight')
        # nx.draw_networkx_edge_labels(MST, pos, edge_labels=edge_labels)
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plt.close()
        plot_url = base64.b64encode(img.getvalue()).decode()
        mst_data = {
            'nodes': [{'id': n} for n in MST.nodes],
            'edges': [{'node1': u, 'node2': v, 'weight': d['weight']} for u, v, d in MST.edges(data=True)],
            'plot_url': plot_url
        }
        return mst_data

@ns.route('/shortest-path/')
class ShortestPathResource(Resource):
    @ns.expect(shortest_path_model)
    def post(self):
        """Calcule le chemin le plus court entre deux nœuds"""
        data = request.json
        G = nx.Graph()
        for node in data['graph']['nodes']:
            G.add_node(node['id'], data=node.get('data'))
        for edge in data['graph']['edges']:
            G.add_edge(edge['node1'], edge['node2'], weight=edge['weight'])

        shortest_path = nx.dijkstra_path(G, source=data['start'], target=data['end'])
        shortest_path_length = nx.dijkstra_path_length(G, source=data['start'], target=data['end'])
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        pos_dict = data['graph']['pos']
        pos = {k: np.array(v) for k, v in pos_dict.items()}
        nx.draw_networkx(G, pos)
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='red')
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plt.close()
        plot_url = base64.b64encode(img.getvalue()).decode()
        return {
            'path': shortest_path,
            'length': shortest_path_length,
            'plot_url': plot_url
        }

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

elif __name__ == '__main__':
    app.run(debug=True)