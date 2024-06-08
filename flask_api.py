import os
import logging
from flask import Flask, request
from flask_restx import Api, Resource, fields
import networkx as nx
from dotenv import load_dotenv
load_dotenv()
# from waitress import serve
# from flasgger import swag_from
# from networkx.readwrite import json_graph

app = Flask(__name__)

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
    'edges': fields.List(fields.Nested(edge_model), description='La liste des arêtes')
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
        mst_data = {
            'nodes': [{'id': n} for n in MST.nodes],
            'edges': [{'node1': u, 'node2': v, 'weight': d['weight']} for u, v, d in MST.edges(data=True)]
        }
        return mst_data

@ns.route('/shortest-path/')
# @api.doc(params={'start': 'Le nœud de départ', 'end': 'Le nœud de fin'})
class ShortestPathResource(Resource):
    @ns.expect(shortest_path_model)
    # @ns.marshal_with(shortest_path_model)
    def post(self):
        """
        Calcule le chemin le plus court entre deux nœuds
        """
        data = request.json
        G = nx.Graph()
        for node in data['graph']['nodes']:
            G.add_node(node['id'], data=node.get('data'))
        for edge in data['graph']['edges']:
            G.add_edge(edge['node1'], edge['node2'], weight=edge['weight'])

        shortest_path = nx.dijkstra_path(G, source=data['start'], target=data['end'])
        shortest_path_length = nx.dijkstra_path_length(G, source=data['start'], target=data['end'])
        return {
            'path': shortest_path,
            'length': shortest_path_length
        }

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.run(debug=True)