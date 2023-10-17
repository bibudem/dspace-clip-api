# dspace-clip-api

API qui permet d'ajouter de la recherche sémantique d'images à [DSpace](https://dspace.lyrasis.org).

Aux bibliothèques de l'UdeM, cette API sera notamment utilisée par Calypso.

## Description

Deux principales fonctions sont assurées par l'API:

1. Pour une image, calculer ses *features* selon un modèle de langage [CLIP](https://openai.com/research/clip), et indexer ces *features* dans un moteur de recherche vectoriel ([AnnLite](https://github.com/jina-ai/annlite)).

2. Pour une chaîne de caractère ou une image, calculer ses *features* selon le même modèle de langage CLIP et effectuer une recherche dans le moteur de recherche pour identifier les images les plus proches.

Ce dépôt est organisé ainsi:

* Le dossier `server` contient différents fichiers de configuration pour démarrer un serveur [clip-as-service](https://clip-as-service.jina.ai) et un serveur AnnLite, qui offrent des services de calcul de *features* et d'indexation des vecteurs.

* Le dossier `utils` contient des scripts utilitaires pour tester les différentes fonctionnalités du serveur ou de l'API.

* Le dossier `api` contient le code de l'API telle quelle.

## Instructions

Voir le *Readme* de chaque dossier pour savoir comment utiliser ces outils.

Ces outils utilisent principalement le langage [Python](https://www.python.org). Vous devez donc avoir Python, version 3.7 ou plus, dans votre environnement.
