# Projet CLIP pour DSpace

Ce projet vise à intégrer une API permettant d'ajouter de la recherche sémantique d'images à DSpace en utilisant le modèle CLIP.
La version Python utilisé est 3.10.10
## Installation

1. Installer les composants :
   pip install clip-server
   pip install clip-client
   

2. Créer un dossier pour le projet, par exemple : `projet-clip`

   La structure de ce dossier pourrait être la suivante :
   - /files
   - /workspace
   - search_flow.yml
   - search_clip.py
   - images-indexation.py
   

## Démarrage

3. Démarrer le serveur avec la commande :
   
   python -m clip_server search_flow.yml
   

4. Exécuter les scripts :
   
   python search_clip.py
   

N'hésitez pas à explorer le contenu du dossier `projet-clip` pour plus d'informations sur les fichiers et leur utilisation.

## Contribuer

Toute contribution est la bienvenue. Si vous souhaitez apporter des améliorations ou signaler des problèmes, veuillez ouvrir une issue ou soumettre une pull request.

### Utilisation des Images

Les images incluses dans ce projet sont utilisées sous licence MIT et proviennent d'une admin template Stellar-Bootstrap 4 ([Lien vers Stellar admin template](http://www.bootstrapdash.com/demo/stellar-admin-free/jquery/)). Cela autorise leur utilisation, copie, modification et distribution pour d'autres projets.
