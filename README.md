# API de Réseau de Télécommunications

Ce projet est une API REST construite avec Flask et Flask-RESTx pour gérer un réseau de télécommunications. Elle utilise NetworkX pour les opérations sur les graphes, telles que la création de graphes, le calcul de l'arbre couvrant minimal (MST) et la recherche du chemin le plus court entre deux nœuds.

## Fonctionnalités

- Création de graphes à partir de nœuds et d'arêtes.
- Calcul de l'arbre couvrant minimal (MST) d'un graphe.
- Recherche du chemin le plus court entre deux nœuds dans un graphe.

## Installation

Pour installer et exécuter ce projet, suivez ces étapes :

1. Clonez le dépôt :
   ```
   git clone https://github.com/nikiema-marius/reseaux_telecom.git
   ```
2. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```
3. Lancez l'application :
   ```
   python flask_api.py
   ```

## Utilisation

L'API est documentée avec Swagger, accessible à l'adresse suivante après le lancement de l'application : `http://localhost:5000/`

### Endpoints

- POST `/telecom/graph` : Crée un graphe à partir des nœuds et des arêtes fournis.
- POST `/telecom/mst` : Calcule l'arbre couvrant minimal du graphe fourni.
- POST `/telecom/shortest-path/` : Calcule le chemin le plus court entre deux nœuds.

## Contribution

Les contributions à ce projet sont les bienvenues. Veuillez suivre les étapes suivantes pour contribuer :

1. Fork le dépôt.
2. Créez une nouvelle branche pour vos modifications.
3. Faites un pull request.