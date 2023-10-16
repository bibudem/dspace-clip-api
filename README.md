# dspace-clip-api
API qui permet d'ajouter de la recherche sémantique d'images à DSpace.

Cette API sera notamment utilisée dans Calypso.

## Description

Deux principales fonctions sont assurées par l'API:

1. Pour une image, calculer ses *embeddings* selon un modèle de langage CLIP, et indexer ces *embeddings* dans un moteur de recherche vectoriel (Annlite).

2. Pour une chaîne de caractère ou une image, calculer ses *embeddings* selon le même modèle de langage CLIP et effectuer une recherche dans le moteur de recherche pour identifier les images les plus proches.

Ce dépôt est organisé ainsi:

* Le dossier `server` contient différents fichiers de configuration pour démarrer un serveur clip-as-service et un serveur Annlite, qui offrent des services de calcul d'*embeddings* et d'indexation des vecteurs.

* Le dossier `utils` contient des scripts utilitaires pour tester les différentes fonctionnalités.

* Le dossier `api` contient le code de l'API telle quelle.

## Instructions

Voir le *Readme* de chaque dossier pour savoir comment utiliser ces outils. 

## Références

À faire.
